import asyncio
import aiohttp
import requests
import time
import random
import pandas as pd
from collections import deque
from concurrent.futures import ThreadPoolExecutor


##scrapping well
apikey =  
retry = 5
timeout = 30
maxRequest = 10 

Ttpex = ThreadPoolExecutor(max_workers=8) 


def detailedinfo(alexid):
    try: 
        link =  f"https://api.openalex.org/works/{alexid}"
        retries = 0

        while retries <= retry:
            try:
                apiresult = requests.get(link, timeout=timeout)

                if apiresult.status_code == 200:
                    jsonresult = apiresult.json()

                    title = jsonresult.get("title", "unknown")
                    alexid = jsonresult.get("id", "unknown")
                    if alexid != "unknown":
                        alexid = alexid.split("/")[-1]
                    doi = jsonresult.get("doi", "unknown")
                    year = jsonresult.get("publication_year", "unknown")
                    authors = jsonresult.get("authorships", [])

                    authorlist = []
                    afflist = []
                    countrylist = []

                    for author in authors:
                        aname = author.get("author", {}).get("display_name", "unknown")
                        authorlist.append(aname)
                        affiliations = author.get("institutions", [])

                        for affiliation in affiliations:
                            afflist.append(affiliation.get("display_name", "unknown"))
                            countrycode = affiliation.get("country_code", "unknown")
                            if countrycode != "unknown":
                                countrylist.append(countrycode)
                    return {
                        "Title": title,
                        "Link": link,
                        "DOI": doi,
                        "AlexID": alexid,
                        "Year": year,
                        "Authors": authorlist,
                        "Affiliations": afflist,
                        "Affiliated Country/Countries": countrylist,
                    }
                
                elif apiresult.status_code == 429:
                    print(f"facing issues with 429")
                    time.sleep(60*(retries))
                
                else:
                    return None
            except Exception as e:
                print(f"There was an error wait 10 sec")
                time.sleep(10)
            retries += 1

        return None
    
    except Exception as e:
        print(f"There was an error in {alexid}. It is {e}")
        return None

    

async def retrying(session, link):
    retries = 0

    while retries <= retry:
        try:
            async with session.get(link, timeout = timeout) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    await asyncio.sleep(60*retries)
                else:
                    print(f"Access to {link} failed...retrying")
        except Exception as e:
            print(f"Access to {link} failed...retrying")

        retries += 1
        await asyncio.sleep(20)

    
    return None


def detailedinfo_sync(paper):
    return detailedinfo(paper)


async def processpaperasync(parent, paper, extractedpapers, thedeque, count):
    
    alexid = paper["id"].split("/")[-1]

    detaileddict = await asyncio.get_running_loop().run_in_executor(Ttpex,detailedinfo_sync, alexid )

    if detaileddict:
        detaileddict["ParentID"] = parent["AlexID"]
        extractedpapers.append(detaileddict)
        thedeque.append(alexid)
        count[0] += 1


async def processparentasync(session, currentAID, extractedpapers, analyzedparents, thedeque, count):

    parent = await asyncio.get_running_loop().run_in_executor(Ttpex, detailedinfo_sync, currentAID)
    if not parent:
        print(f"we are skipping {currentAID}...")
        return

    analyzedparents.add(currentAID)
    extractedpapers.append(parent)

    link = f"https://api.scraperapi.com/?api_key={apikey}&url=https://api.openalex.org/works?filter=cites:{currentAID}&per-page=200"

    while link:
        
        data = await retrying(session, link)
        if not data:
            break

        papersciting = data.get("results", [])
        if not papersciting:
            print(f"There were no citations found for {currentAID}")
            break

        allatonce = [processpaperasync(parent, paper, extractedpapers, thedeque, count) for paper in papersciting]

        await asyncio.gather(*allatonce)

        link = data.get("next_page")
        if link:
            link = f"https://api.scraperapi.com/?api_key={apikey}&premium=true&url={link}"




async def geteverything(alexidslist, max = 250000):

    thedeque = deque(alexidslist)
    extractedpapers = []
    analyzedparents = set()
    count = [0]

    async with aiohttp.ClientSession() as session:
        while thedeque and count[0] <= max:
            print(f"count is {count[0]}")
            await asyncio.sleep(random.uniform(6, 12))

            currentAID = thedeque.popleft()
            if currentAID in analyzedparents:
                continue

            await processparentasync(session, currentAID, extractedpapers, analyzedparents, thedeque, count)

    if extractedpapers:
        df = pd.DataFrame(extractedpapers)
        df.to_csv("GlobalAIData.csv")
        print("its done go look at csv")
    else:
        print("fail at turning to csv")

    


alexidslist = ["W4385245566"]
asyncio.run(geteverything(alexidslist))
