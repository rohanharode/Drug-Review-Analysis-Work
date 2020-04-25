import inflect
import pandas as pd

custom_stopwords = ['etc','etc.','may', 'occur', 'far', 'see','drug', 'product', 'change', 'extremely', 'extreme', 'dose', 'much',
                    'really', 'felt', 'early', 'give', 'began', 'stop', 'stopped', 'feel', 'feeling', 'go', 'going',
                    'even', 'pill', 'capsule', 'able', 'along', 'easily', 'seemed', 'started', 'made', 'got',
                    'need', 'help', 'helped', 'one', 'two', 'three', 'put', 'experience', 'experienced', 'am', 'pm',
                    'hour', 'hours', 'hr', 'hrs', 'less', 'more', 'lot', 'use', 'around', 'gets', 'taken',
                    'medication', 'medicine', 'taking', 'adjusts', 'body', 'tell', 'still', 'side', 'effects',
                    'became', 'become', 'terrible', 'worse', 'caused', 'cause', 'problems', 'problem', 'none',
                    'n\'t', 'mg', 'mgs', 'amount', 'involved', 'Name', 'dtype', 'object', 'series', 'Word',
                    'occured', 'noticed', 'doctor', 'pharmacist', 'promptly', 'incident', 'effect', 'effected',
                    'affected', 'time', 'take', 'first', 'last', '\'ve', 'every', 'initially', 'gradually', 'usually', 'using',
                    'next', 'day', 'days', 'week', 'weeks', 'month', 'months', 'very', 'treatment', 'affect',
                    'within','must','issue','especially','happen','didn\'t','didnt','till','perhaps','say','associated','start','symptoms',
                    'seem','related','found','besides','often','typically','used','makes','causing','typical','realize',
                    'realized','happening','actually','needed','need','beginning']

df = pd.DataFrame(custom_stopwords, columns =['stopwords'])
df.to_csv('custom_stopwords.csv',index=False)

