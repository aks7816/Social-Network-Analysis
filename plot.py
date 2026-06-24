# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Load your data
# data = {
#     "Year": [2017,2018,2019,2020,2021,2022,2023,2024],
#     "Num Clusters": [2,18,23,44,39,53,54,39],
#     "Avg Cluster Size": [39,77.9,195.6,208.3,369.1,275.9,464.6,402.3],
#     "Gini Coefficient": [0.38,0.49,0.39,0.56,0.55,0.53,0.52,0.48]
# }
# df = pd.DataFrame(data)

# # ----- 1. Average Cluster Size -----
# plt.figure(figsize=(7,4))
# plt.plot(df['Year'], df['Avg Cluster Size'], marker='o', color='blue', label='Avg Cluster Size')
# # Trend line
# z = np.polyfit(df['Year'], df['Avg Cluster Size'], 1)
# p = np.poly1d(z)
# plt.plot(df['Year'], p(df['Year']), linestyle='--', color='blue')

# plt.xlabel("Year")
# plt.ylabel("Average Cluster Size")

# plt.show()

# # ----- 2. Number of Clusters -----
# plt.figure(figsize=(7,4))
# plt.plot(df['Year'], df['Num Clusters'], marker='o', color='purple', label='Num Clusters')
# # Trend line
# z = np.polyfit(df['Year'], df['Num Clusters'], 1)
# p = np.poly1d(z)
# plt.plot(df['Year'], p(df['Year']), linestyle='--', color='purple')

# plt.xlabel("Year")
# plt.ylabel("Number of Clusters")

# plt.show()

# # ----- 3. Gini Coefficient -----
# plt.figure(figsize=(7,4))
# plt.plot(df['Year'], df['Gini Coefficient'], marker='o', color='red', label='Gini Coefficient')
# # Trend line
# z = np.polyfit(df['Year'], df['Gini Coefficient'], 1)
# p = np.poly1d(z)
# plt.plot(df['Year'], p(df['Year']), linestyle='--', color='red')

# plt.xlabel("Year")
# plt.ylabel("Gini Coefficient Value")
# plt.ylim(0,1)
# plt.show()



# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Load your data
# data = {
#     "Year": [2017,2018,2019,2020,2021,2022,2023,2024],
#     "Num Clusters": [2,18,23,44,39,53,54,39],
#     "Avg Cluster Size": [39,77.9,195.6,208.3,369.1,275.9,464.6,402.3],
#     "Gini Coefficient": [0.38,0.49,0.39,0.56,0.55,0.53,0.52,0.48]
# }
# df = pd.DataFrame(data)

# # Helper to compute R²
# def compute_r2(x, y, p):
#     y_pred = p(x)
#     ss_res = np.sum((y - y_pred) ** 2)
#     ss_tot = np.sum((y - np.mean(y)) ** 2)
#     return 1 - (ss_res / ss_tot)

# # ----- 1. Average Cluster Size -----
# plt.figure(figsize=(7,4))
# plt.plot(df['Year'], df['Avg Cluster Size'], marker='o', color='blue', label='Avg Cluster Size')
# z = np.polyfit(df['Year'], df['Avg Cluster Size'], 1)
# p = np.poly1d(z)
# plt.plot(df['Year'], p(df['Year']), linestyle='--', color='blue')

# # R² calculation & display
# r2 = compute_r2(df['Year'], df['Avg Cluster Size'], p)
# plt.text(df['Year'].min(), max(df['Avg Cluster Size']), f"$R^2$ = {r2:.2f}", color='blue', fontsize=12)

# plt.xlabel("Year")
# plt.ylabel("Average Cluster Size")
# plt.grid(alpha=0.3)
# plt.show()

# # ----- 2. Number of Clusters -----
# plt.figure(figsize=(7,4))
# plt.plot(df['Year'], df['Num Clusters'], marker='o', color='purple', label='Num Clusters')
# z = np.polyfit(df['Year'], df['Num Clusters'], 1)
# p = np.poly1d(z)
# plt.plot(df['Year'], p(df['Year']), linestyle='--', color='purple')

# r2 = compute_r2(df['Year'], df['Num Clusters'], p)
# plt.text(df['Year'].min(), max(df['Num Clusters']), f"$R^2$ = {r2:.2f}", color='purple', fontsize=12)

# plt.xlabel("Year")
# plt.ylabel("Number of Clusters")
# plt.grid(alpha=0.3)
# plt.show()

# # ----- 3. Gini Coefficient -----
# plt.figure(figsize=(7,4))
# plt.plot(df['Year'], df['Gini Coefficient'], marker='o', color='red', label='Gini Coefficient')
# z = np.polyfit(df['Year'], df['Gini Coefficient'], 1)
# p = np.poly1d(z)
# plt.plot(df['Year'], p(df['Year']), linestyle='--', color='red')

# r2 = compute_r2(df['Year'], df['Gini Coefficient'], p)
# plt.text(df['Year'].min(), 0.95, f"$R^2$ = {r2:.2f}", color='red', fontsize=12)

# plt.xlabel("Year")
# plt.ylabel("Gini Coefficient Value")
# plt.ylim(0,1)
# plt.grid(alpha=0.3)
# plt.show()








import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
data = {
    "Year": [2017,2018,2019,2020,2021,2022,2023,2024],
    "Num Clusters": [2,18,23,44,39,53,54,39],
    "Avg Cluster Size": [39,77.9,195.6,208.3,369.1,275.9,464.6,402.3],
    "Gini Coefficient": [0.38,0.49,0.39,0.56,0.55,0.53,0.52,0.48]
}
df = pd.DataFrame(data)

# Helper to compute R²
def pearson_r(x, y):
    return np.corrcoef(np.asarray(x), np.asarray(y))[0, 1]

# ----- 1. Average Cluster Size -----

x = df['Year']
y = df['Avg Cluster Size']
r = pearson_r(x, y)

plt.figure(figsize=(7,4))
plt.plot(x, y, marker='o', color='blue', label='Avg Cluster Size')
z = np.polyfit(x, y, 1); p = np.poly1d(z)
plt.plot(x, p(x), linestyle='--', color='blue')
plt.text(x.min(), y.max(), f"r = {r:.2f}", color='blue', fontsize=12)
plt.xlabel("Year"); plt.ylabel("Average Cluster Size"); plt.grid(alpha=0.3)
plt.show()

# ----- 2. Number of Clusters -----
x = df['Year']
y = df['Num Clusters']
r = pearson_r(x, y)

plt.figure(figsize=(7,4))
plt.plot(x, y, marker='o', color='purple', label='Num Clusters')
z = np.polyfit(x, y, 1); p = np.poly1d(z)
plt.plot(x, p(x), linestyle='--', color='purple')
plt.text(x.min(), y.max(), f"r = {r:.2f}", color='purple', fontsize=12)
plt.xlabel("Year"); plt.ylabel("Number of Clusters"); plt.grid(alpha=0.3)
plt.show()

# ----- 3. Gini Coefficient -----
x = df['Year']
y = df['Gini Coefficient']
r = pearson_r(x, y)

plt.figure(figsize=(7,4))
plt.plot(x, y, marker='o', color='red', label='Gini Coefficient')
z = np.polyfit(x, y, 1); p = np.poly1d(z)
plt.plot(x, p(x), linestyle='--', color='red')
plt.text(x.min(), 0.95, f"r = {r:.2f}", color='red', fontsize=12)
plt.xlabel("Year"); plt.ylabel("Gini Coefficient Value"); plt.ylim(0,1)
plt.grid(alpha=0.3)
plt.show()