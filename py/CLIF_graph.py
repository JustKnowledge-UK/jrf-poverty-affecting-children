import os
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter 


# 1. Specify the url that downloads the data
url = 'https://assets.publishing.service.gov.uk/media/67dc2c58c5528de3aa6711f9/children-in-low-income-families-local-area-statistics-2014-to-2024.ods'
# For definitions, see 'Guidance' page of the spreadsheet

# Ensure the 'data' folder exists
os.makedirs('../data', exist_ok=True)

# 2. Specify folder name as the final part of the url after it's been split on '/' and specify relative path
file = url.split('/')[-1]
path = os.path.join('../data', file)

# 3. If the path doesn't exist, download the data. If it does exist, skip this step.
if not os.path.exists(path):
    req = requests.get(url)
    with open(path, 'wb') as output_file:
        output_file.write(req.content)
else:
    print('Data already downloaded. Loading')

# Convert excel file for local authority data into pandas dataframe.
la_df = pd.read_excel(path, 
                   sheet_name='3_Relative_Local_Authority', skiprows=8)
# For absolute poverty measures, substitute '4_Absolute_Local_Authority' as the sheet_name

# Convert excel file for ward data into pandas dataframe.
ward_df = pd.read_excel(path, 
                   sheet_name='7_Relative_Ward', skiprows=9)
# For absolute poverty measures, substitute '8_Absolute_Ward' as the sheet_name


# Only include the percentages, not the absolute numbers of, children in low income families. 
pc_low_income = la_df.iloc[:, np.r_[0:2, -10:-1]]
ward_pc_low_income = ward_df.iloc[:, np.r_[0:4,-10:-1]]

# Assign the percentages for the UK, Haringey and Northumberland Park ward respectively.
uk_pc_low_income = pc_low_income[pc_low_income['Local Authority [note 2]'] == 'United Kingdom [note 4]']
haringey_pc_low_income = pc_low_income[pc_low_income['Local Authority [note 2]'] == 'Haringey']
numpark_pc_low_income = ward_pc_low_income[ward_pc_low_income['Ward [note 2]'] == 'Northumberland Park']

# Transpose the arrays so they can be processed correctly.
uk_pc_low_income = uk_pc_low_income.iloc[:, 2:].T
haringey_pc_low_income = haringey_pc_low_income.iloc[:, 2:].T
numpark_pc_low_income = numpark_pc_low_income.iloc[:, 4:].T

# Convert decimal values into percentages.
uk_pc_low_income[0] = uk_pc_low_income[0]*100
haringey_pc_low_income[177] = haringey_pc_low_income[177]*100
numpark_pc_low_income[4150] = numpark_pc_low_income[4150] * 100

# Create list of years from 2014 to 2023.
year_range=[]
for i in range(2014, 2023):
    year_range.append(str())





# The graph itself

sns.set_theme()
sns.set_context("poster")
sns.set_style("whitegrid")

fig, ax = plt.subplots(figsize=(10, 5), dpi=800)

# Add lines for UK, Haringey and Northumberland Park respectively.
sns.lineplot(x=list(range(2014, 2023)), y=uk_pc_low_income[0], lw=5, ax=ax, label='Line A', legend=False)
sns.lineplot(x=list(range(2014, 2023)), y=haringey_pc_low_income[177], lw=5, ax=ax, label='Line B', legend=False)
sns.lineplot(x=list(range(2014, 2023)), y=numpark_pc_low_income[4150], lw=5, ax=ax, label='Line C', legend=False)

# Style the grid.
ax.grid(True, linestyle='--', linewidth=0.8)
ax.xaxis.grid(False)

# Add labels for each line.
ax.text(2022.1, uk_pc_low_income[0][-1], 'UK', va='center')
ax.text(2022.1, haringey_pc_low_income[177][-1], 'Haringey', va='center')
ax.text(2022.1, numpark_pc_low_income[4150][-1], 'Northumberland\nPark', va='center')

# Add axis labels.
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}/{str(int(x)+1)[-2:]}'))
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))
plt.ylim(10, 30)
plt.ylabel('')
plt.xlim(2014, 2022)
plt.xticks(rotation=20)  # Optional: rotate labels for readability

# Add lines.
line = ax.lines[0]
line.set_solid_capstyle('round')

plt.title("Percentage of Children in Low Income Families")


# Saves the graph into the filename and path given. Saves into current directory if no path is given.
plt.savefig('../outputs/UK_Haringey_NP_CLIF.png', dpi=800, bbox_inches='tight')

plt.close()