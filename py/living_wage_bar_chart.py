import os
import requests
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 1. Specify the url that downloads the data
url = 'https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/numberandproportionofemployeejobswithhourlypaybelowthelivingwage/2024provisional/lwf2024provisional.zip'

# Ensure the 'data' folder exists
os.makedirs('../data', exist_ok=True)

# 2. Specify folder name as the final part of the url after it's been split on '/' and specify relative path
folder = url.split('/')[-1]
path = os.path.join('../data', folder)

# 3. If the path doesn't exist, download the data. If it does exist, skip this step.
if not os.path.exists(path):
    req = requests.get(url)
    with open(path, 'wb') as output_file:
        output_file.write(req.content)
else:
    print('Data already downloaded. Loading')

# 4. Unzip the folder
## i. Define outpath as same as in path minus .zip
out_path = os.path.splitext(path)[0]  # This removes the .zip extension

## ii. Create the extraction directory if it doesn't exist
if not os.path.exists(out_path):
    os.makedirs(out_path)

## iii. Unzip to extraction directory
with zipfile.ZipFile(path, 'r') as zip_ref:
    zip_ref.extractall(out_path)

# 5. Identify the file in the directory you want to read and read it
filepath = os.path.join(out_path, 'Work PC LWF Table 9 LWF.1a   lwfmgx 2024.xlsx')

# Convert excel file into pandas dataframe.
blw_2024 = pd.read_excel(filepath,
                        sheet_name='All', skiprows=4, skipfooter=5)

# Tidy up dataframe.
blw_2024 = blw_2024.drop(columns=["Unnamed: 4"])
blw_2024 = blw_2024.rename(columns={'Description': 'Constituency', 'Unnamed: 3': 'Percentage'})

# List the parliamentary constituencies.
categories = ['Tottenham', 'Walthamstow', 'Hackney North and Stoke Newington', 'Hampstead and Highgate', 
              'Hornsey and Friern Barnet', 'Southgate and Wood Green', 'Edmonton and Winchmore Hill', 
              'Chingford and Woodford Green']

# Loop through the percentages for each parliamentary constituency.
values = [blw_2024[blw_2024['Constituency'] == category].values[0][-1] for category in categories]

# Create colours for the bars of the bar chart; blue for Tottenham and green for the rest.
colors = ['#66c2a5'] * len(values)
colors[0] = '#3288bd'

# Create horizontal bar chart
plt.figure(dpi=800)
plt.barh(categories, values, color=colors)

# Add labels and title
plt.xlabel('Percentage')
plt.title('Jobs Paid Below Living Wage')

# Display the chart
plt.tight_layout()

# Saves the graph into the filename and path given. Saves into current directory if no path is given.
plt.savefig('../outputs/living_wage_vs_tottenham_bar_chart.png', dpi=800, bbox_inches='tight')

plt.close()