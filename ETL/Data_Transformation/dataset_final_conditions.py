import pandas as pd


def select_final_condition(df1, df2, column, name):
    df2 = df2[[column[0], column[1], column[2]]]
    print(df2.shape)
    df2 = df2.drop_duplicates()
    print(df2.shape)
    merged_dataframe = df2.merge(df1, how='inner', left_on=[column[0], column[1]], right_on=['Drug', 'Condition'])
    print(df1.shape)
    print(merged_dataframe.shape)
    if name == 'webmd':
        merged_dataframe.to_csv("./../../dataset/webmd/webmd_v06_final_conditions.csv", index=False)
    elif name == 'druglib':
        merged_dataframe.to_csv("./../../dataset/druglib/druglib_v06_final_conditions.csv", index=False)


def site_level_final_condition():
    """
        Select webmd final conditions
        Select druglib final conditions
    """

    df_webmd = pd.read_csv("./../../dataset/webmd/webmd_v01_processed.csv")
    df_webmd_updated_condition = pd.read_csv("./../../dataset/webmd/webmd_v05_updated_conditions.csv")
    webmd_cols = ['WebMD_drugname', 'WebMD_condition', 'final_condition']
    select_final_condition(df_webmd, df_webmd_updated_condition, webmd_cols, 'webmd')
    print('Done with webmd')

    df_druglib = pd.read_csv("./../../dataset/druglib/druglib_v01_processed.csv")
    df_druglib_updated_condition = pd.read_csv("./../../dataset/druglib/druglib_v05_updated_conditions.csv")
    druglib_cols = ['DrugLib_drugname', 'DrugLib_condition', 'final_condition']
    select_final_condition(df_druglib, df_druglib_updated_condition, druglib_cols, 'druglib')
    print('Done with druglib')
