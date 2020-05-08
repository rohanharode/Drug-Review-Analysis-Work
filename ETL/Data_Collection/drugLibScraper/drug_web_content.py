import pathlib
import string

from requests import get

pathlib.Path('./drug_web_content').mkdir(exist_ok=True)

for letter in string.ascii_lowercase:
    url = 'http://www.druglib.com/drugindex/rating/'+letter+'/'
    response = get(url)
    path = pathlib.Path().absolute()


    with open('./drug_web_content/druglist_' + letter + '.html', 'w') as file:
        file.write(response.text)
        file.close()
