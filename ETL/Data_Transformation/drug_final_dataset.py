import pandas as pd

def site_level_datasets_creation():
    # Drugs.com
    df_drugs = pd.read_csv("./../../dataset/drugs_com/drugs_com_v01_processed.csv")
    df_webmd_altered = pd.read_csv("./../../dataset/webmd/webmd_v04_fuzzy_on_conditions.csv")
    df1 = df_webmd_altered.groupby(['DrugsCom_drugname', 'DrugsCom_condition'], sort=False).size().reset_index()
    merged_dataframe = df_drugs.merge(df1, how='inner', left_on=['drug', 'condition'], right_on=['DrugsCom_drugname', 'DrugsCom_condition'])
    merged_dataframe['website'] = 'drugs.com'
    merged_dataframe = merged_dataframe[['user_id', 'drug', 'condition', 'review', 'rating', 'date', 'useful_count', 'website']]
    merged_dataframe.to_csv('./../../dataset/drugs_com/drugs_com_v07_final_dataset.csv', index=False)
    print('Drugs.com dataset created')


    # Webmd
    df_webmd = pd.read_csv("./../../dataset/webmd/webmd_v06_final_conditions.csv")
    df_webmd['Website'] = 'webmd'
    df_webmd = df_webmd[['Drug', 'final_condition', 'Rating', 'Date', 'Age', 'Sex', 'Reviews', 'Sides', 'Website']]
    df_webmd = df_webmd.rename(columns={'final_condition': 'Condition', 'Sides': 'Side_Effects'})
    df_webmd.to_csv('./../../dataset/webmd/webmd_v07_final_dataset.csv', index=False)
    print('Webmd dataset created')


    # Druglib
    df_druglib = pd.read_csv("./../../dataset/druglib/druglib_v06_final_conditions.csv")
    df_druglib['Website'] = 'druglib'
    df_druglib = df_druglib[['Drug', 'final_condition', 'Rating', 'Age_Group', 'Sex', 'Reviews', 'Side Effect', 'Website']]
    df_druglib = df_druglib.rename(columns={'final_condition': 'Condition', 'Side Effect': 'Side_Effects', 'Age_Group': 'Age'})
    df_druglib.to_csv('./../../dataset/druglib/druglib_v07_final_dataset.csv', index=False)
    print('Druglib dataset created')
