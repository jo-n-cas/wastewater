from data_analysis import N20_to_CO2, CH4_to_CO2
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import sqlite3
import seaborn as sns
# This file is used to generate the web graphs for the data analysis

# Connect to the SQLite database
conn = sqlite3.connect('static/wastewater.db')
################################################################
#Bar graph to show the percentage of safely treated wastewater by country
################################################################

query_safely_treated="""
                        SELECT STWW_PCT,country
                        FROM wastewater_data
                        """
safely_treated_df = pd.read_sql_query(query_safely_treated, conn)
print(safely_treated_df)

# Close the connection
conn.close()

code_to_name = {'usa': 'United States',
                'can': 'Canada',
                'mex': 'Mexico'}
# Convert the country codes to names
safely_treated_df['country'] = safely_treated_df['country'].map(code_to_name)

# Order the dataframe by the percentage of safely treated wastewater
safely_treated_df = safely_treated_df.sort_values(by='STWW_PCT', ascending=False)

print(safely_treated_df)

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

plt.rcParams['font.family'] = 'sans-serif' 
# Barplot using seaborn, but on a matplotlib axis
sns.barplot(x='country', y='STWW_PCT', data=safely_treated_df, palette="mako", ax=ax)

# Set labels and title
ax.set_title('Percentage of Safely Treated Wastewater by Country')
ax.set_xlabel('Country')
ax.set_ylabel('Percentage of Safely Treated Wastewater')

# Match the gridline style
ax.grid(axis='y', alpha=0.6)
ax.set_axisbelow(True)

# Remove all spines
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()

# Save the figure
output_path = 'images/safely_treated_wastewater.png'
if not os.path.exists(output_path):
   plt.savefig(output_path, dpi=300, bbox_inches='tight')




##################################################################
# Bar graph of N2O and CH4 emissions equivelance to CO2 by country
################################################################


N20_to_CO2= N20_to_CO2*10**(-3) # Convert from Gg to Tg
CH4_to_CO2 = CH4_to_CO2*10**(-3) # Convert from Gg to Tg
print("N2O to CO2 emissions (Tg CO2/yr):")
print(N20_to_CO2)
print("CH4 to CO2 emissions (Tg CO2/yr):")
print(CH4_to_CO2)
# Ensure both sources use the same order
labels = N20_to_CO2.index.tolist()
x = np.arange(len(labels))  # the label locations

plt.rcParams['font.family'] = 'sans-serif'
# Heights
N2O_values = N20_to_CO2.iloc[:, 0].reindex(labels).values
CH4_values = CH4_to_CO2.iloc[:, 0].reindex(labels).values


fig, ax = plt.subplots()
bars1 = ax.bar(x, N2O_values, bottom=CH4_values, label='N2O', color='#b6d0eb')
bars2 = ax.bar(x, CH4_values, label='CH4', color='#9cce9b',)

for spine in ax.spines.values():
    spine.set_visible(False)


# Labels and formatting
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Equivalance to CO2 emissions (Tg CO2/yr)')
ax.set_title('CH4 and N2O Emissions by Country')
ax.legend()

ax.grid(axis='y', alpha=0.6)
ax.set_axisbelow(True)
plt.tight_layout()
# Save the figure
output_path = 'images/CH4_N2O_emissions.png'
if not os.path.exists(output_path):
    plt.savefig(output_path, dpi=300, bbox_inches='tight')


