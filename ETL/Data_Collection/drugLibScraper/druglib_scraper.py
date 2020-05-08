import pandas as pd
import pathlib
import re
import requests
from bs4 import BeautifulSoup

errors_names = []
df = pd.read_csv("all_drug_link.csv")

drug_link = df.url.values


link_list = []
drug_list = []
age_list = []
sex_list = []
condition_list = []
rating_list = []
reviews_list = []
side_effect_list = []


for link in drug_link:
    req = requests.get(link)
    print(req.status_code)
    print(req.text)
    if req.status_code != 200:
        print("Could not connect to " + link)
        print("Response : " + str(req.status_code))
        errors_names.append(link)

    bs = BeautifulSoup(req.text, 'html.parser')

    all_reviews = []
    source = []

    try:
        source = bs.findAll("table", {"cellspacing": 4, "border": 0})

    except Exception as e:
        print(e)

    for i in range(len(source)):
        link_list.append(link)
        drug = link.split('/')[-2]
        drug_list.append(drug)
        review = {}
        author = source[i].find("h2").getText()
        review["author"] = author
        review['age'] = re.findall(r'\d+', review["author"])[0]
        age_list.append(review['age'])
        if author.find('female') == -1:
            review['Sex'] = 'Male'
        else:
            review['Sex'] = 'Female'
        sex_list.append(review['Sex'])

        test = source[i].findAll("td", {"class" :  "review3"})
        rating = len(test[0].findAll("img", {"src": "/img/red_star.gif"}))
        rating_list.append(rating)
        review["rating"] = rating
        review["Condition"] = test[3].getText()
        condition_list.append(review["Condition"])
        review["Side effects"] = test[8].getText()
        side_effect_list.append(review["Side effects"])
        review["Comments"] = test[9].getText()
        reviews_list.append(review['Comments'])
        all_reviews.append(review)


df = pd.DataFrame(list(zip(link_list, drug_list, condition_list, sex_list, age_list, rating_list, reviews_list, side_effect_list)),
                  columns=['URL', 'Drug', 'Condition', 'Sex', 'Age', 'Rating', 'Reviews', 'Side Effect'])

pathlib.Path('./../../../dataset').mkdir(exist_ok=True)
pathlib.Path('./../../../dataset/druglib').mkdir(exist_ok=True)

df.to_csv('./../../../dataset/druglib/druglib.csv', index=False)

print("Saved data in drug_lib.csv")

