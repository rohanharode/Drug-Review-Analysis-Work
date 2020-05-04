def set_age_range(x):
    if 0 <= x.Age <= 2:
        value = "0-2"
    elif 3 <= x.Age <= 6:
        value = "3-6"
    elif 7 <= x.Age <= 12:
        value = "7-12"
    elif 13 <= x.Age <= 18:
        value = "13-18"
    elif 19 <= x.Age <= 24:
        value = "19-24"
    elif 25 <= x.Age <= 34:
        value = "25-34"
    elif 35 <= x.Age <= 44:
        value = "35-44"
    elif 45 <= x.Age <= 54:
        value = "45-54"
    elif 55 <= x.Age <= 64:
        value = "55-64"
    elif 65 <= x.Age <= 74:
        value = "65-74"
    elif 75 <= x.Age:
        value = "75 or over"
    return value


def webmd_rating_average(df):
    df['Rating'] = ((df['EaseofUse'] + df['Effectiveness'] + df['Satisfaction']) / 3) * 2
    df['Rating'] = df['Rating'].round(0).astype(int)
    df = df[['Age', 'Condition', 'Date', 'Drug', 'DrugId', 'Rating', 'Reviews', 'Sex', 'Sides', 'UsefulCount']]
    df = df[df['Rating'] <= 10]
    return df
