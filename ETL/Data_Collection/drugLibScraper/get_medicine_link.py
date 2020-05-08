from bs4 import BeautifulSoup
import pandas as pd
import string

prefix = 'http://www.druglib.com'
drug_list = []

for letter in string.ascii_lowercase:

    with open('./drug_web_content/druglist_' + letter + '.html') as file:
        content = file.read()

    html_soup = BeautifulSoup(content, 'html.parser')
    drugs_link = html_soup.find_all('a')

    for link in drugs_link:
        drug_url = link.get('href')

        if drug_url.startswith('/ratingsreviews'):
            link = prefix + drug_url
            drug_list.append(link)





drug_set = set(drug_list)
unique_list = (list(drug_set))
unique_list.sort()
print(unique_list)
df = pd.DataFrame(list(zip(unique_list)), columns=['url'])
df.to_csv('all_drug_link.csv', index=False)
