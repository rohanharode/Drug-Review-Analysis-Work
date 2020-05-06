import psycopg2
import sqlalchemy
import pandas as pd


def postgres_table():
    engine = sqlalchemy.create_engine('postgresql://Shubham:@localhost:5432/draw')

    side_effect_df = pd.read_csv('../../side_effects.csv')

    side_effect_df.to_sql(
        name='drug_side_effects',
        con=engine,
        index=False,
        if_exists='replace'
    )
    print('side effect table created')
    full_merge_model_predictions_df = pd.read_csv('../../full_merge_model_predictions.csv')

    full_merge_model_predictions_df.to_sql(
        name='full_merge',
        con=engine,
        index=False,
        if_exists='replace'
    )
    print('final merge table created')
    print('end')

postgres_table()
