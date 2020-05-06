import pandas as pd


def final_dataset_creation():
    df_drugs = pd.read_csv("./../../dataset/drugs_com/drugs_com_v07_final_dataset.csv")
    df_drugs = df_drugs[['drug', 'condition', 'review', 'rating', 'website']]
    df_drugs = df_drugs.rename(
        columns={'drug': 'Drug', 'condition': 'Condition', 'review': 'Reviews', 'rating': 'Rating',
                 'website': 'Website'})
    df_drugs["Condition"] = df_drugs["Condition"].str.lower()

    df_druglib = pd.read_csv("./../../dataset/druglib/druglib_v07_final_dataset.csv")
    df_druglib = df_druglib[['Drug', 'Condition', 'Reviews', 'Rating', 'Website']]
    df_druglib["Condition"] = df_druglib["Condition"].str.lower()

    df_webmd = pd.read_csv("./../../dataset/webmd/webmd_v07_final_dataset.csv")
    df_webmd = df_webmd[['Drug', 'Condition', 'Reviews', 'Rating', 'Website']]
    df_webmd["Condition"] = df_webmd["Condition"].str.lower()

    pdList = [df_drugs, df_druglib, df_webmd]
    new_df = pd.concat(pdList)
    new_df = new_df[new_df['Reviews'] != ' ']
    new_df = new_df.drop_duplicates()

    ## Unique condition check
    # df1 = new_df.groupby(['Condition'], sort=False).size().reset_index()
    # print(df1.shape)
    new_df = new_df.dropna()
    new_df.to_csv('./../../full_merge.csv', index=False)
    print('Final dataset created')
