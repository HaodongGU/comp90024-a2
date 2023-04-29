import pandas as pd

df = pd.read_csv('datasource-AU_Govt_DJSB-UoM_AURIN_DB_djsb_population_by_labour_force_status_sa4_2018.csv')

df.drop('wkb_geometry', axis=1, inplace=True)
df.to_csv('employment_brief.csv')