import pandas as pd
import ast
from fuzzywuzzy import fuzz


def merge_df(df_drugs_dot_com, merge_with_df,df_name):
    if df_name == 'WebMD':
        jaccard_df = pd.read_csv('./../../dataset/webmd/webmd_v03_drugs_com_jaccard.csv')
    if df_name == 'DrugLib':
        jaccard_df = pd.read_csv('./../../dataset/druglib/druglib_v03_drugs_com_jaccard.csv')

    count_unique_conditions(jaccard_df, merge_with_df,df_name)

    df_merge1 = pd.merge(jaccard_df, df_drugs_dot_com, left_on='id1', right_on='id')
    df_merge2 = pd.merge(df_merge1, merge_with_df, left_on='id2', right_on='id')
    df_merge = df_merge2[['id1', 'joinKey1', 'id2', 'joinKey2', 'drug', 'condition', 'Drug', 'Condition']].rename(
        columns={'drug': 'DrugsCom_drugname', 'condition': 'DrugsCom_condition', 'Condition': df_name + '_condition', 'Drug':df_name + '_drugname'})

    df_merge[df_name + '_New_Condition'] = df_merge.apply(lambda row: ' ', axis=1)
    df_merge['Fuzz_ratio'] = df_merge.apply(lambda row: ' ', axis=1)

    for i in range(len(df_merge)):
        if ast.literal_eval(str(df_merge['joinKey1'][i]))[0] == ast.literal_eval(str(df_merge['joinKey2'][i]))[0]:
            df_merge[df_name + '_New_Condition'][i] = df_merge['DrugsCom_condition'][i]
            df_merge['Fuzz_ratio'][i] = fuzz.ratio(df_merge[df_name + '_condition'][i].lower(),
                                                   df_merge[df_name + '_New_Condition'][i].lower())
        else:
            df_merge[df_name + '_New_Condition'][i] = df_merge[df_name + '_condition'][i]
            df_merge['Fuzz_ratio'][i] = fuzz.ratio(df_merge[df_name + '_condition'][i].lower(), df_merge[df_name + '_New_Condition'][i].lower())

    return df_merge

def count_unique_conditions(jaccard_df,merge_with_df,df_name):
    unique_drugs = set()

    for i in range(len(jaccard_df)):
        if ast.literal_eval(str(jaccard_df['joinKey1'][i]))[0] == ast.literal_eval(str(jaccard_df['joinKey2'][i]))[0]:
            unique_drugs.add(ast.literal_eval(str(jaccard_df['joinKey1'][i]))[0])

    print('No. of unique matching drugs in jaccard of drugs.com and ' + df_name + ": ", len(unique_drugs))
    print(len(merge_with_df))
    count = 0
    condition_list = set()
    for j in range(len(merge_with_df)):
        drug = str(merge_with_df['Drug'][j])
        if drug.split(" ")[0] in list(unique_drugs):
            condition_list.add(merge_with_df['Condition'][j])
            count = count + 1

    print('No. of unique matching conditions in jaccard of drugs.com and ' + df_name + ": ",len(condition_list))


def fuzzy_matching():
    """
        Merge webmd with drugs_dot_com
        Merge druglib with drugs_dot_com
    """

    df_drugs_dot_com = pd.read_csv('./../../dataset/drugs_com/drug_com_v02_conditions_grouped.csv')
    df_webMD = pd.read_csv('./../../dataset/webmd/webmd_v02_conditions_grouped.csv')
    df_drugLib = pd.read_csv('./../../dataset/druglib/druglib_v02_conditions_grouped.csv')

    df_webmd_drugsCom = merge_df(df_drugs_dot_com, df_webMD, "WebMD")
    df_webmd_drugsCom.to_csv('./../../dataset/webmd/webmd_v04_fuzzy_on_conditions.csv', index=False)

    df_druglib_drugs_com = merge_df(df_drugs_dot_com, df_drugLib, "DrugLib")
    df_druglib_drugs_com.to_csv('./../../dataset/druglib/druglib_v04_fuzzy_on_conditions.csv', index=False)