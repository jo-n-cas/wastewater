import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("static/wastewater.db")
relevant_countries = ['can', 'usa', 'mex'] #sort countries  
j=["SEW_PCT","SEP_PCT","OTHIMP_PCT","UNIMP_PCT"]
j_mcf=["Centralised, aerobic treatment plant","Septic tank","Anaerobic reactor (e.g., upflow anaerobic sludge blanket digestion (UASB))","Latrine"]
j_N_REM=["Secondary (biological)","Septic tank","Primary (mechanical)","Latrine"]
j_ef=["Centralised, aerobic treatment plant","Septic tank","Anaerobic reactor","Latrine"]

B_max= 0.6 # Maximum CH4 production capacity (kg CH4/kg BOD)



###################################################################
#CH4 EMISSIONS Calculation
###################################################################

def TOW_calc(countries):
    """
    Calculate the TOTAL ORGANICALLY DEGRADABLE MATERIAL (TOW) for a given country.

    Parameters:
    List of countries  (str): The name of the country.

    #P= Population served by wastewater treatment
    #BOD= Biochemical oxygen demand per capita 
    #Equation:
    #TOW= P * BOD * 0.01 *365

    Returns:
    list of Floats: Total organics in wastewater (TOW_c) in kg BOD/year for each country.
    """
    TOW_c= []
    for country in countries:
    # Query the database for popultation
        P= f"""
            SELECT POP
            FROM wastewater_data
            WHERE country = '{country}'
            """
    # Query the database for BOD
        BOD = f"""
            SELECT bod5_g_per_day
            FROM estimated_bod
            WHERE country = '{country}'
            """
    
    # Read the data into a DataFrame
        P_df = pd.read_sql_query(P, conn)
        BOD_df= pd.read_sql_query(BOD, conn)
    

    
        P = P_df['POP'].values[0]
        BOD =BOD_df['bod5_g_per_day'].values[0]  

    # Calculate TOW
        TOW = P*1000 * BOD * 365* 0.01  # Convert to kg/year
        TOW_c.append(TOW)

    return TOW_c

# Calculate TOW for relevant countries
TOW = TOW_calc(relevant_countries)

print("Total organics in wastewater (TOW) for each country:")
for country, tow in zip(relevant_countries, TOW):
    print(f"{country}: {tow} kg BOD/year")


def TOW_j_calc(countries, TOW_c, j):
    """
    Calculate total organics in wastewater in inventory year, kg BOD/yr, for treatment/discharge system, j.

    Parameters:
    countries (list of str): Country codes .
    TOW_c (list of float): Corresponding total TOW values per country.

    #j= type of treatment/discharge system {sewer, septic, other-imporved, other-unimproved}
    #TOW=total organics in wastewater
    #Prop_j= proportion of population served by treatment/discharge system j
    #Equation:
    #TOW_j= TOW * Prop_j

    Returns:
    dict: Keys are country codes, values are lists with TOW_j values for each system [sewer, septic, other_improved, unimproved].
    """
    TOW_j_results= {}
    
    for country, total_tow in zip(countries, TOW_c):
        # Query proportions of population using each system type
        query = f"""
            SELECT {', '.join(j)}
            FROM wastewater_data
            WHERE country = '{country}'
            """
        proportions_df = pd.read_sql_query(query, conn)

        # Get proportions
        proportions = proportions_df.iloc[0].values / 100  # Convert percentages to fractions

        # Calculate TOW_j for each system
        tow_j = [total_tow * prop for prop in proportions]

        # Store result
        TOW_j_results[country] = tow_j

    return TOW_j_results

# Calculate TOW_j for each country
TOW_j = TOW_j_calc(relevant_countries, TOW, j)
print("\nTotal organics in wastewater (TOW_j) for each country and system type:")
for country, tow_j in TOW_j.items():
    print(f"{country}: {tow_j} kg BOD/year")


def CH4_ef (B,j):
    """
    Calculate the methane emission factor (EF) for each system type.

    Parameters:
    B (float): Maximun CH4 production capacity (kg CH4/kg BOD).
    j (list of str): List of treatment/discharge system types.

    #B= Biochemical oxygen demand per capita 
    #j= type of treatment/discharge system {sewer, septic, other-imporved, other-unimproved}
    #MCF= methane conversion factor(fraction)
    #EF= methane emission factor
    #Equation:
    #EF= BOD * MCF 

    Returns:
    CH4_ef_results (List): EF values for each system [sewer, septic, other_improved, unimproved].

    Equivelance of type of treatment and discharge pathway or system of MCF data with wasterwater data:
    Sewer(SEW_PCT) = "Centralised, aerobic treatment plant"
    Septic(SEP_PCT) = "Septic tank"
    Other-improved(OTHIMP_PCT) = "Anaerobic reactor (e.g., upflow anaerobic sludge blanket digestion (UASB))"
    Other-unimproved(UNIMP_PCT) = "Latrine"
    """
    CH4_ef_results = []
    for system_name in j :
        # Query proportions of population using each system type
        query = f"""
            SELECT MCF
            FROM estimated_mcf
            WHERE system = '{system_name}'
            """
        df = pd.read_sql_query(query, conn)
        MCF = df["mcf"].iloc[0]
        EF = B * MCF 
        CH4_ef_results.append(EF)
    return CH4_ef_results

# Calculate CH4 EF for each system type 
CH4_ef_value = CH4_ef(B_max, j_mcf)
print("\nMethane emission factor (EF) for each system type:")
for system, ef in zip(j_mcf, CH4_ef_value):
    print(f"{system}: {ef}")
        

def CH4_emissions(countries,TOW_j_results, CH4_ef_results):
    """
    Calculate the methane emissions for each system type.

    Parameters:
    TOW_j_results (dict): Total organics in wastewater for each country and system type. Keys are country codes, values are lists with TOW_j values for each system [sewer, septic, other_improved, unimproved].
    CH4_ef_results (list): Methane emission factors for each system type.
    countries (list of str): Country codes.

    #TOW_j= total organics in wastewater
    #EF= methane emission factor
    #Rj= amount of recovered CH4 (default 0)
    #Equation:
    #CH4_emissions= TOW_j * EF- Rj

    Returns:
    dict: Keys are country codes, values are lists with CH4 emissions for each system [sewer, septic, other_improved, unimproved].
    """
    CH4_emissions_results = {}
    for country in countries:
        # Get the TOW_j values for this country
        tow_values = TOW_j_results[country]

        # Calculate CH4 emissions for each system: CH4 = TOW_j * EF (Rj is assumed 0)
        ch4_emissions = [tow * ef for tow, ef in zip(tow_values, CH4_ef_results)]

        # Store result
        CH4_emissions_results[country] = ch4_emissions

    return CH4_emissions_results

# Calculate CH4 emissions for each country
CH4_emissions_j = CH4_emissions(relevant_countries,TOW_j, CH4_ef_value)
print("\nMethane emissions for each country and system type:")
for country, emissions in CH4_emissions_j.items():
    print(f"{country}: {emissions} kg CH4/year")

def CH4_emissions_total(CH4_emissions_j):
    """
    Calculate the total methane emissions for each country.

    Parameters:
    CH4_emissions_j (dict): Methane emissions for each country and system type. Keys are country codes, values are lists with CH4 emissions for each system [sewer, septic, other_improved, unimproved].

    CH4= methane emissions
    #Equation:
    CH4_total= sum(CH4_emissions)

    Returns:
    dict: Keys are country codes, values are total methane emissions.
    """
    CH4_emissions_total_results = {}
    
    for country, emissions in CH4_emissions_j.items():
        total_emissions = sum(emissions) * 10**(-6) # Convert to kg to Gg
        CH4_emissions_total_results[country] = total_emissions
        

    return CH4_emissions_total_results

# Calculate total CH4 emissions for each country
CH4_total = CH4_emissions_total(CH4_emissions_j)
#print("\nTotal methane emissions for each country based on wastewater treatment:")
#for country, total_emissions in CH4_total.items():
    #print(f"{country}: {total_emissions} Gg CH4/year")


###################################################################
#N2O EMISSIONS Calculation
###################################################################

def calc_TN_dom_j (j,countries,N_HH=1.1,F_NPR=0.16):
    """
    TOTAL NITROGEN IN DOMESTIC WASTEWATER BY TREATMENT PATHWAY 

    Parameters:
    j (list): type of treatment/discharge system {sewer, septic, other-imporved, other-unimproved}
    countries (list of str): Country codes.


    #Equation:
    #TN_dom_j= P_treatmenmt_j * (Protein * F_NPR + (F_NON_CON * N_HH) + N_HH)
    P_treatmenmt_j= (list) population served by treatment pathway j
    Protein= annual per capita protein consumption, kg protein/person/yr
    F_NPR=fraction of nitrogen in protein, default = 0.16 kg N/kg protein
    F_NON_CON= factor for nitrogen in non-consumed protein disposed in sewer system, kg N/kg N
    N_HH = additional nitrogen from household products added to the wastewater, default is 1.1


    Returns:
    TN_dom_j (dict): total annual amount of nitrogen in domestic wastewater for treatment pathway j, kg N/yr
    """
    TN_dom_j = {}
    for country in countries:
        # Query the database for population served by treatment pathway j
        query_j_prop = f"""
            SELECT {', '.join(j)}
            FROM wastewater_data
            WHERE country = '{country}'
            """
        proportions_df = pd.read_sql_query(query_j_prop, conn)
        proportions = proportions_df.iloc[0].values / 100  # Convert percentages to fractions
        P= f"""
            SELECT POP
            FROM wastewater_data
            WHERE country = '{country}'
            """
        # Query the database for population
        P_df = pd.read_sql_query(P, conn)
        P = P_df['POP'].values[0]*1000
        # Calculate population served by treatment pathway j
        P_treatmenmt_j = [P * prop for prop in proportions]
    

        # Query the database for protein consumption
        query_protein = f"""
            SELECT protein
            FROM protein_factors
            WHERE region = 'North America and Oceania'
            """
        protein_df = pd.read_sql_query(query_protein, conn)
        protein = protein_df['protein'].values[0]

        # Query the database for F_NON_CON
        query_f_non_con = f"""
            SELECT f_non_con
            FROM protein_factors
            WHERE region = 'North America and Oceania'
            """
        f_non_con_df = pd.read_sql_query(query_f_non_con, conn)
        f_non_con = f_non_con_df['f_non_con'].values[0]


        # Calculate TN_dom_j for each system
        tn_dom_j_values = []
        for prop in P_treatmenmt_j:
            tn_dom_j_value = prop * (protein * F_NPR *f_non_con * N_HH)  # kg N/yr
            tn_dom_j_values.append(tn_dom_j_value)

        TN_dom_j[country] = tn_dom_j_values

    return TN_dom_j


# Calculate TN_dom_j for each country
TN_dom_j = calc_TN_dom_j(j, relevant_countries)
print("\nTotal nitrogen in domestic wastewater (TN_dom_j) for each country and system type:")
for country, tn_j in TN_dom_j.items():
    print(f"{country}: {tn_j} kg N/yr")

# Calculate the total nitrogen in domestic wastewater effluent (N_ef_dom) for each country 
def calc_N_ef_dom(j_rem,TN_dom_j,j,):
    """
    Calculate the TOTAL NITROGEN IN DOMESTIC WASTEWATER EFFLUENT
    Parameters:
    - j_rem (list): List of treatment types corresponding to systems [sewer, septic, other_improved, unimproved].
    - TN_dom_j (dict): Total nitrogen in domestic wastewater per country per system type, kg N/year.
    - j (list): List of treatment types corresponding to systems [sewer, septic, other_improved, unimproved].

    TN_DOM_j(dict of list)= total nitrogen in domestic wastewater in inventory year, kg N/yr.
    T_j(list)= degree of utilisation of treatment system j in inventory year
    N_REM(list)= fraction of total wastewater nitrogen removed during wastewater treatment per
    treatment type j.

    #Equation:
    N_ef_dom= sum[(TN_DOM_j * T_j)*(1-N_REM)]

    Returns:
    N_ef_results (dictionary): where key are countries and the values are thetotal nitrogen in the wastewater effluent discharged to aquatic environments in
    inventory year in each country, kg N/yr
    

    Equivelance of type of treatment and discharge pathway or system of Nitrogen REM factor data with wasterwater data:
    Sewer(SEW_PCT) = "Secondary (biological)"
    Septic(SEP_PCT) = "Septic tank"
    Other-improved(OTHIMP_PCT) = "Primary (mechanical)"
    Other-unimproved(UNIMP_PCT) = "Latrine"
    """
    query_j_prop = f"""
            SELECT {', '.join(j)}
            FROM wastewater_data
            WHERE country = '{country}'
            """
    proportions_df = pd.read_sql_query(query_j_prop, conn)/100

    query_rem = f"""
                SELECT default_rem, treatment_type
                FROM nitrogen_rem_fac
                """
    n_rem_df = pd.read_sql_query(query_rem, conn)
    query_n20= f"""
                SELECT ef, type
                FROM ef_n20_data
                """
    n20_df = pd.read_sql_query(query_n20, conn)
    n20_df = n20_df[n20_df['type'].isin(j_ef)]
    n20_df['order'] = n20_df['type'].apply(lambda x: j_ef.index(x))
    n20_df = n20_df.sort_values(by='order').drop(columns=['order'])
    print(n20_df)

    TN_df = pd.DataFrame(TN_dom_j)
    sorted_n_rem_df = n_rem_df[n_rem_df['treatment_type'].isin(j_rem)]
    sorted_n_rem_df['order'] = sorted_n_rem_df['treatment_type'].apply(lambda x: j_rem.index(x))
    sorted_n_rem_df = sorted_n_rem_df.sort_values(by='order').drop(columns=['order'])

    second_term= (1-sorted_n_rem_df["default_rem"]).to_numpy().reshape(4,1)
    whole= TN_df* proportions_df.to_numpy().transpose()* second_term
    N_ef_results = whole.sum(axis=0)
    return N_ef_results 


# Calculate N_ef_dom for each country
N_ef_dom= calc_N_ef_dom(j_N_REM, TN_dom_j, j)
print("\nTotal nitrogen in domestic wastewater effluent (N_ef_dom) for each country and system type:")
for country, n_ef in zip(relevant_countries, N_ef_dom):
    print(f"{country}: {n_ef} kg N/yr")



def calc_N20_total(N_ef_results,factor=(44/28)):
    """
    Calculate the total N2O emissions for each country based on wastewater treatment.
    Parameters:
    N_ef_results (dict): Total nitrogen in domestic wastewater effluent per country, kg N/yr.
    countries (list of str): Country codes.
    factor (float): Conversion factor from kg N to kg N2O (default is 44/28).
    #Equation:
    #N2O_emissions= N_ef* factor
    Returns:
    dict: Total N2O emissions for each country, kg N2O/yr.
    """
    N_ef_results_df = pd.DataFrame(N_ef_results)
    N20_emissions_results = N_ef_results_df * factor * 10**(-6) # Convert to Gg N2O/yr


    return N20_emissions_results #fix
    
N20_total= calc_N20_total(N_ef_dom)

def calc_conversion_to_C02(N20_total,CH4_total):
    CH4_df = pd.DataFrame.from_dict(CH4_total,orient="index")
    N20_to_CO2 = N20_total * 298
    CH4_to_CO2 = CH4_df * 25
    return N20_to_CO2, CH4_to_CO2

N20_to_CO2, CH4_to_CO2 = calc_conversion_to_C02(N20_total,CH4_total)

#close the database connection
conn.close()





