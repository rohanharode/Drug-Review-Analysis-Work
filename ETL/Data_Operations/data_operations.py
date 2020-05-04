from ETL.Data_Preprocessing.data_cleaning_and_filtering import cleaning_and_filtering
from ETL.Data_Transformation.drug_conditions_grouped import group_conditions
from ETL.Data_Transformation.jaccard_similarity import apply_jaccard_similarity
from ETL.Data_Transformation.drug_conditions_fuzzy_matching import fuzzy_matching
from ETL.Data_Transformation.updating_conditions import updating_conditions
from ETL.Data_Transformation.dataset_final_conditions import site_level_final_condition
from ETL.Data_Transformation.drug_final_dataset import site_level_datasets_creation
from ETL.Data_Aggregation.full_merge import final_dataset_creation

def all_data_operations():

    # Task1: Data Preprocessing
    cleaning_and_filtering()

    # Task2: Condition grouping
    group_conditions()

    # Task3: Apply Jaccard similarity on condition and drugname
    apply_jaccard_similarity()

    # Task4: Fuzzy matching conditions
    fuzzy_matching()

    # Task5: Fuzzy matching conditions
    updating_conditions()

    # Task6: Finalizing site level conditions
    site_level_final_condition()

    # Task7: Creating site level datasets
    site_level_datasets_creation()

    # Task8: Creating final aggregated dataset (combining webmd, drugs.com, druglib
    final_dataset_creation()
    print('All Data Operations completed, processed data in full_merge.csv')

all_data_operations()