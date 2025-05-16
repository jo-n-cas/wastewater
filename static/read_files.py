import pandas as pd
import sqlite3 
import os
# Connect to SQLite database
conn = sqlite3.connect('static/wastewater.db')
# Create a cursor object
cursor = conn.cursor()


# List of files
files = ['data/canada_can_sdg631_2023.xlsx', 'data/mexico_mex_sdg631_2023.xlsx', 'data/unitedstatesofamerica_usa_sdg631_2023.xlsx']  # add all your files here

def read_correctly(files):
    for file in files:
        # Check if the file exists
        if not os.path.isfile(file):
            print(f"File {file} not found. Skipping.")
            continue
        # Read the Excel file
        #df = pd.read_excel(file, sheet_name='Data inputs (all)')
        df = pd.read_excel(file, sheet_name='Sheet1')
        df['Value'] = df['Value'].astype(str).str.replace(',', '.').astype(float)
        country= file.split('_')[1]  # get country name from filename
        year = file.split('_')[3].replace('.xlsx', '')
        year = int(year)
        # Pivot the table
        variables = df.set_index('Variable code')['Value'].to_dict()
        #print(variables)

    # Build one row
        row = {
            'country': country,
            'year': year,
            'POP': variables.get('POP', None),
            'POP_WATON_PCT': variables.get('POP_WATON_PCT', None),
            'POP_WATOFF_PCT': variables.get('POP_WATOFF_PCT', None),
            'USE_WATON_AVG': variables.get('USE_WATON_AVG', None),
            'USE_WATOFF_AVG': variables.get('USE_WATOFF_AVG', None),
            'USE_VOL': variables.get('USE_VOL', None),
            'USE_TO_WW_PCT': variables.get('USE_TO_WW_PCT', None),
            'GEN_VOL': variables.get('GEN_VOL', None),
            'SEW_PCT': variables.get('SEW_PCT', None),
            'SEP_PCT': variables.get('SEP_PCT', None),
            'OTHIMP_PCT': variables.get('OTHIMP_PCT', None),
            'UNIMP_PCT': variables.get('UNIMP_PCT', None),
            'OD_PCT': variables.get('OD_PCT', None),
            'SEW_VOL': variables.get('SEW_VOL', None),
            'SEP_VOL': variables.get('SEP_VOL', None),
            'OTHIMP_VOL': variables.get('OTHIMP_VOL', None),
            'UNIMP_VOL': variables.get('UNIMP_VOL', None),
            'OD_VOL': variables.get('OD_VOL', None),
            'SEW_DEL_WWTP_PCT': variables.get('SEW_DEL_WWTP_PCT', None),
            'SEW_ST_WWTP_CMP_PCT': variables.get('SEW_ST_WWTP_CMP_PCT', None),
            'SEW_ST_WWTP_TCH_PCT': variables.get('SEW_ST_WWTP_TCH_PCT', None),
            'SEP_CONT_PCT': variables.get('SEP_CONT_PCT', None),
            'SEP_ON_BUR_PCT': variables.get('SEP_ON_BUR_PCT', None),
            'SEP_LOCAL_PCT': variables.get('SEP_LOCAL_PCT', None),
            'SEP_OFF_EMPT_PCT': variables.get('SEP_OFF_EMPT_PCT', None),
            'SEP_ON_NOEMPT_PCT': variables.get('SEP_ON_NOEMPT_PCT', None),
            'SEP_OFF_DEL_WWTP_PCT': variables.get('SEP_OFF_DEL_WWTP_PCT', None),
            'SEP_OFF_ST_WWTP_PCT': variables.get('SEP_OFF_ST_WWTP_PCT', None),
            'SEW_DEL_TRT_VOL': variables.get('SEW_DEL_TRT_VOL', None),
            'SEP_OFF_DEL_TRT_VOL': variables.get('SEP_OFF_DEL_TRT_VOL', None),
            'SEP_ON_DEL_TRT_VOL': variables.get('SEP_ON_DEL_TRT_VOL', None),
            'DEL_TRT_VOL': variables.get('DEL_TRT_VOL', None),
            'SEW_STWW_VOL': variables.get('SEW_STWW_VOL', None),
            'SEP_OFF_STWW_VOL': variables.get('SEP_OFF_STWW_VOL', None),
            'SEP_ON_STWW_VOL': variables.get('SEP_ON_STWW_VOL', None),
            'STWW_VOL': variables.get('STWW_VOL', None),
            'SEW_STWW_PCT': variables.get('SEW_STWW_PCT', None),
            'SEP_OFF_STWW_PCT': variables.get('SEP_OFF_STWW_PCT', None),
            'SEP_ON_STWW_PCT': variables.get('SEP_ON_STWW_PCT', None),
            'STWW_PCT': variables.get('STWW_PCT', None)
        }   
        # Insert into database
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['?'] * len(row))
        values = list(row.values())
        # Check if the record already exists
        cursor.execute("SELECT 1 FROM wastewater_data WHERE country = ? AND year = ?", (country, year))
        if cursor.fetchone():
            print(f"Record for {country} in {year} already exists. Skipping.")
        else:
            # Insert the new record if it doesn't exist
            sql = f"INSERT INTO wastewater_data ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            conn.commit()  # Save after each insert

       


# Ensure the table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS wastewater_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    year INTEGER NOT NULL,
    POP FLOAT,
    POP_WATON_PCT FLOAT,
    POP_WATOFF_PCT FLOAT,
    USE_WATON_AVG FLOAT,
    USE_WATOFF_AVG FLOAT,
    USE_VOL FLOAT,
    USE_TO_WW_PCT FLOAT,
    GEN_VOL FLOAT,
    SEW_PCT FLOAT,
    SEP_PCT FLOAT,
    OTHIMP_PCT FLOAT,
    UNIMP_PCT FLOAT,
    OD_PCT FLOAT,
    SEW_VOL FLOAT,
    SEP_VOL FLOAT,
    OTHIMP_VOL FLOAT,
    UNIMP_VOL FLOAT,
    OD_VOL FLOAT,
    SEW_DEL_WWTP_PCT FLOAT,
    SEW_ST_WWTP_CMP_PCT FLOAT,
    SEW_ST_WWTP_TCH_PCT FLOAT,
    SEP_CONT_PCT FLOAT,
    SEP_ON_BUR_PCT FLOAT,
    SEP_LOCAL_PCT FLOAT,
    SEP_OFF_EMPT_PCT FLOAT,
    SEP_ON_NOEMPT_PCT FLOAT,
    SEP_OFF_DEL_WWTP_PCT FLOAT,
    SEP_OFF_ST_WWTP_PCT FLOAT,
    SEW_DEL_TRT_VOL FLOAT,
    SEP_OFF_DEL_TRT_VOL FLOAT,
    SEP_ON_DEL_TRT_VOL FLOAT,
    DEL_TRT_VOL FLOAT,
    SEW_STWW_VOL FLOAT,
    SEP_OFF_STWW_VOL FLOAT,
    SEP_ON_STWW_VOL FLOAT,
    STWW_VOL FLOAT,
    SEW_STWW_PCT FLOAT,
    SEP_OFF_STWW_PCT FLOAT,
    SEP_ON_STWW_PCT FLOAT,
    STWW_PCT FLOAT
)
''')


# Run the function

read_correctly(files)

##################################################

# Load CSV with the estimated BOD data

bod_df = pd.read_csv("data/estimated_BOD.csv", delimiter="\t", on_bad_lines="warn")

# Mapping of country/region names to abbreviations
abbreviations = {
    "Africa": "afr",
    "Egypt": "egy",
    "Asia, Middle East, Latin America": "asia_me_la",
    "India": "ind",
    "West Bank and Gaza Strip (Palestine)": "ps",
    "Japan": "jpn",
    "Brazil": "bra",
    "Mexico": "mex",
    "Canada, Europe, Russia, Oceania": "can",
    "Denmark": "dnk",
    "Germany": "deu",
    "Greece": "grc",
    "Italy": "ita",
    "Sweden": "swe",
    "Turkey": "tur",
    "United States": "usa"
}

# Replace country/region names with abbreviations
bod_df["Country/Region"] = bod_df["Country/Region"].map(abbreviations)

# Rename columns for SQL compatibility
bod_df.columns = ["country", "bod5_g_per_day", "range", "reference"]

cursor.execute("""
CREATE TABLE IF NOT EXISTS estimated_bod (
    country TEXT PRIMARY KEY,
    bod5_g_per_day REAL,
    range TEXT,
    reference INTEGER
);
""")

# Insert BOD data into SQL table
bod_df.to_sql("estimated_bod", conn, if_exists="replace", index=False)


##################################################

# Load CSV for MCF data
mcf_df = pd.read_csv("data/mcf.csv")

# Rename columns 
mcf_df.columns = ['system', 'mcf', 'mcf_range', 'ef_bod', 'ef_cod']

# Clean whitespace
mcf_df['system'] = mcf_df['system'].str.strip()
mcf_df['mcf_range'] = mcf_df['mcf_range'].str.strip(" ()")


# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS estimated_mcf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system TEXT NOT NULL,
    mcf FLOAT NOT NULL,
    mcf_range TEXT,
    ef_bod FLOAT,
    ef_cod FLOAT
);
""")




# Insert MCF data into SQL table
for _, row in mcf_df.iterrows():
    cursor.execute("""
        INSERT INTO estimated_mcf (system, mcf, mcf_range, ef_bod, ef_cod)
        VALUES (?, ?, ?, ?, ?)
    """, (
        row['system'],
        float(row['mcf']),
        row['mcf_range'],
        float(row['ef_bod']) if not pd.isna(row['ef_bod']) else None,
        float(row['ef_cod']) if not pd.isna(row['ef_cod']) else None
    ))




##################################################
# Load csv file for Protein factors 
protein_df = pd.read_csv("data/protein_factors.csv")


cursor.execute("""
CREATE TABLE IF NOT EXISTS protein_factors (
    region TEXT PRIMARY KEY,
    protein FLOAT NOT NULL,
    f_non_con FLOAT NOT NULL,
    add_N TEXT
);
""")
insert_query = """
INSERT OR REPLACE INTO protein_factors (region, protein, f_non_con, add_N)
VALUES (?, ?, ?, ?)
"""
data_to_insert = protein_df[['Region','Protein (fraction of protein supply)','F_NON_CON' ,"Additional N from households’ chemicals"]].values.tolist()
cursor.executemany(insert_query, data_to_insert)
##################################################
nitrogen_df = pd.read_csv("data/nitrogen_rem_fac.csv")


cursor.execute("""
CREATE TABLE IF NOT EXISTS nitrogen_rem_fac(
    treatment_type TEXT PRIMARY KEY,
    default_rem FLOAT NOT NULL,
    range TEXT
);
""")
insert_query_rem_fac = """
    INSERT OR REPLACE INTO nitrogen_rem_fac (treatment_type, default_rem, range)
    VALUES (?, ?, ?)
"""
to_insert = nitrogen_df[["Treatment Type","Default","Range"]].values.tolist()
cursor.executemany(insert_query_rem_fac, to_insert)

##################################################

n20_df = pd.read_csv("data/n2o_emissions_wastewater.csv")


# Rename columns for SQL compatibility
n20_df.columns = ["type", "ef", "range"]

cursor.execute("""
CREATE TABLE IF NOT EXISTS ef_n20_data (
    type TEXT PRIMARY KEY,
    ef FLOAT,
    range TEXT
);
""")

# Insert data into SQL table
n20_df.to_sql("ef_n20_data", conn, if_exists="replace", index=False)



##################################################
# Print the first 5 rows of the table
df = pd.read_sql_query("SELECT * FROM wastewater_data", conn)
print(df.head(5))
bod= pd.read_sql_query("SELECT * FROM estimated_bod", conn)
print(bod.head(10))
mcf= pd.read_sql_query("SELECT * FROM estimated_mcf", conn)
print(mcf.head(5))
protein= pd.read_sql_query("SELECT * FROM protein_factors", conn)
print(protein.head(5))
nitrogen= pd.read_sql_query("SELECT * FROM nitrogen_rem_fac", conn)
print(nitrogen.head(5))
n20= pd.read_sql_query("SELECT * FROM ef_n20_data", conn)
print(n20.head(5))
# Commit the changes
conn.commit()
# Close the connection
conn.close()

