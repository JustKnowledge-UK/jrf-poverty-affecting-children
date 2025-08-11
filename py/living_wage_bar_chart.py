import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Download the file https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/numberandproportionofemployeejobswithhourlypaybelowthelivingwage/2024provisional/lwf2024provisional.zip
# and unzip.

# Convert excel file into pandas dataframe.
blw_2024 = pd.read_excel('Enter the path to the file/lwf2024provisional/Work PC LWF Table 9 LWF.1a   lwfmgx 2024.xlsx',
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
plt.savefig('living_wage_vs_tottenham_bar_chart.png', dpi=800, bbox_inches='tight')

plt.close()