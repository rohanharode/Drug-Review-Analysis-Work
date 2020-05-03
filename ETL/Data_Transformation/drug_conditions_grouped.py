import pandas as pd

def group_conditions():
    # Reading drugs.com csv
    df_drugs_com = pd.read_csv("./../../dataset/drugs_com/drugs_com_v01_processed.csv")

    # Reading webMD csv
    df_webmd = pd.read_csv("./../../dataset/webmd/webmd_v01_processed.csv")

    # Read drug lib csv
    df_druglib = pd.read_csv("./../../dataset/druglib/druglib_v01_processed.csv")

    # Taking only drug and condition from all Data Frames
    df_drugs_com = df_drugs_com[['drug', 'condition']]
    df_webmd = df_webmd[['Drug', 'Condition']]
    df_druglib = df_druglib[['Drug', 'Condition']]

    # Finding unique combination of drug and condition of drugs.com
    series_drugs_com = df_drugs_com.groupby(['drug', 'condition']).size()
    drugs_com = pd.DataFrame(series_drugs_com).reset_index()
    drugs_com = drugs_com[drugs_com.condition.str.contains("span") == False]
    drugs_com = drugs_com[drugs_com.condition.str.contains("Not Listed") == False]

    # Finding unique combination of drug and condition of webMD
    series_webmd = df_webmd.groupby(['Drug', 'Condition']).size()
    webmd = pd.DataFrame(series_webmd).reset_index()
    webmd = webmd[webmd['Condition'] != "Other"]

    # Finding unique combination of drug and condition of webMD
    series_druglib = df_druglib.groupby(['Drug', 'Condition']).size()
    druglib = pd.DataFrame(series_druglib).reset_index()

    print('drugs_com.shape ',drugs_com.shape)
    print('webmd.shape ',webmd.shape)
    print('druglib.shape ',druglib.shape)

    # Creating unique id for drugs.com
    drugs_com['id'] = range(0, 0+len(drugs_com))
    drugs_com['id'] = 'drugs_' + drugs_com['id'].astype(str)
    drugs_com = drugs_com[['id', 'drug', 'condition']]

    # Creating unique id for webMD
    webmd['id'] = range(0, 0+len(webmd))
    webmd['id'] = 'webMD_' + webmd['id'].astype(str)
    webmd = webmd[['id', 'Drug', 'Condition']]

    # Creating unique id for drug lib
    druglib['id'] = range(0, 0+len(druglib))
    druglib['id'] = 'drugLib_' + druglib['id'].astype(str)
    druglib = druglib[['id', 'Drug', 'Condition']]

    drugs_com.to_csv('./../../dataset/drugs_com/drug_com_v02_conditions_grouped.csv', index=False)
    webmd.to_csv('./../../dataset/webmd/webmd_v02_conditions_grouped.csv', index=False)
    druglib.to_csv('./../../dataset/druglib/druglib_v02_conditions_grouped.csv', index=False)
