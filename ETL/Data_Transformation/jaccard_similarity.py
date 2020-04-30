# similarity_join.py
import pandas as pd
import re

# Tokenizer method
def string_to_token(val):
    # Splitting string into tokens
    words = re.split(r'\W+', str(val))
    word_list = []
    for word in words:
        # Converting words to lower case
        word_lowered = word.lower()
        word_list.append(word_lowered)
    while "" in word_list:
        word_list.remove("")

    return word_list


# Jaccard function to calculate Jaccard similarity for each pair
def jaccard(key1, key2):
    # Taking intersection of the two sets in numerator
    num = len(set(key1).intersection(set(key2)))

    # Taking union of the two sets in denominator
    den = len(set(key1).union(set(key2)))

    return float(num / den)


class SimilarityJoin:
    def __init__(self, data_file1, data_file2):
        self.df1 = pd.read_csv(data_file1)
        self.df2 = pd.read_csv(data_file2)

    def preprocess_df(self, df, cols):

        # Concatenate the columns
        df["joinKey"] = df[cols[0]].fillna('') + " " + df[cols[1]].fillna('')

        # Calling string_to_token function to apply tokenizer to concatenated string
        df["joinKey"] = df["joinKey"].apply(lambda x: string_to_token(x))

        return df

    def filtering(self, df1, df2):

        # Flatting the list in df1's joinKey (Amazon)
        df1_flat = df1.explode('joinKey')
        df1_flat = df1_flat[['id', 'joinKey']]
        df1_flat.columns = ['id1', 'joinKey1']

        # Flatting the list in df2's joinKey (Google)
        df2_flat = df2.explode('joinKey')
        df2_flat = df2_flat[['id', 'joinKey']]
        df2_flat.columns = ['id2', 'joinKey2']

        # Merging or joining 2 df's on joinKey to see if the 2 joinKey share at least one token
        df_merge = pd.merge(df1_flat, df2_flat, left_on='joinKey1', right_on='joinKey2')

        # Dropping duplicates
        cand_df = df_merge[['id1', 'id2']].drop_duplicates()

        # Joining df with the original df1 and df2 on id's
        cand_df = pd.merge(cand_df, df1, left_on='id1', right_on='id')
        cand_df = pd.merge(cand_df, df2, left_on='id2', right_on='id')
        cand_df = cand_df[['id1', 'joinKey_x', 'id2', 'joinKey_y']]
        cand_df.columns = ['id1', 'joinKey1', 'id2', 'joinKey2']

        return cand_df

    def verification(self, cand_df, threshold):

        # Called jaccard function to calculate  Jaccard similarity value and store in the new column
        cand_df["jaccardSimilarity"] = cand_df.apply(lambda x: jaccard(x.joinKey1, x.joinKey2), axis=1)

        # Taking values which are above or equal to threshold
        cand_df = cand_df[cand_df["jaccardSimilarity"] >= threshold]

        return cand_df

    def jaccard_join(self, cols1, cols2, threshold):
        new_df1 = self.preprocess_df(self.df1, cols1)
        new_df2 = self.preprocess_df(self.df2, cols2)

        print("Before filtering: %d pairs in total" %(self.df1.shape[0] *self.df2.shape[0]))

        cand_df = self.filtering(new_df1, new_df2)
        print("After Filtering: %d pairs left" %(cand_df.shape[0]))

        result_df = self.verification(cand_df, threshold)
        print("After Verification: %d similar pairs" %(result_df.shape[0]))

        return result_df


def apply_jaccard_similarity():

    er = SimilarityJoin("./../../dataset/drugs_com/drug_com_v02_conditions_grouped.csv", "./../../dataset/webmd/webmd_v02_conditions_grouped.csv")

    drugs_cols = ["drug", "condition"]
    wedmd_cols = ["Drug", "Condition"]
    result_webmd_df = er.jaccard_join(drugs_cols, wedmd_cols, 0.5)

    result_webmd_df.to_csv('./../../dataset/webmd/webmd_v03_drugs_com_jaccard.csv', index=False)

    er = SimilarityJoin("./../../dataset/drugs_com/drug_com_v02_conditions_grouped.csv", "./../../dataset/druglib/druglib_v02_conditions_grouped.csv")

    drugs_cols = ["drug", "condition"]
    druglib_cols = ["Drug", "Condition"]
    result_druglib_df = er.jaccard_join(drugs_cols, druglib_cols, 0.5)

    result_druglib_df.to_csv('./../../dataset/druglib/druglib_v03_drugs_com_jaccard.csv', index=False)