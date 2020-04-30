import pandas as pd

def select_best_condition(condition, new_condition, Fuzz_ratio):
    if Fuzz_ratio == 0:
        value = new_condition
    elif Fuzz_ratio < 63:
        value = condition
    else:
        value = new_condition
    return value


def get_updated_conditions(df, column, name):

    df1 = df.groupby(['id2', column[0], column[1], column[2]], sort=False)[column[3]].max().reset_index()

    df2 = df1.groupby(['id2'], sort=False)['Fuzz_ratio'].max().reset_index()

    merged_dataframe = df2.merge(df1, how='inner', left_on=['id2', 'Fuzz_ratio'], right_on=['id2', 'Fuzz_ratio'])

    merged_dataframe['final_condition'] = merged_dataframe.apply(lambda x: select_best_condition(x[column[1]], x[column[2]], x[column[3]]), axis=1)

    if name == 'webmd':
        print('Saving webmd file')
        merged_dataframe.to_csv('./../../dataset/webmd/webmd_v05_updated_conditions.csv', index=False)
    elif name == 'druglib':
        print('Saving druglib file')
        merged_dataframe.to_csv('./../../dataset/druglib/druglib_v05_updated_conditions.csv', index=False)


def updating_conditions():
    """
        Update webmd conditions
        Update druglib conditions
    """

    df_webMD = pd.read_csv("./../../dataset/webmd/webmd_v04_fuzzy_on_conditions.csv")
    webmd_col_list = ['WebMD_drugname', 'WebMD_condition', 'WebMD_New_Condition', 'Fuzz_ratio']
    get_updated_conditions(df_webMD, webmd_col_list, 'webmd')
    print('Done with webmd')

    df_drugLib = pd.read_csv('./../../dataset/druglib/druglib_v04_fuzzy_on_conditions.csv')
    druglib_col_list = ['DrugLib_drugname', 'DrugLib_condition', 'DrugLib_New_Condition', 'Fuzz_ratio']
    get_updated_conditions(df_drugLib, druglib_col_list, 'druglib')
    print('Done with druglib')