import requests
import re
import time
def genTitles(lastNode): 
    print(lastNode)
    response = requests.Session().get( 
        url="https://en.wikipedia.org/w/api.php", 
        params={ 
            "utf8": 1, 
            "action": "query", 
            "list": "allpages", 
            "format": "json",
            "aplimit": "max", 
            "apcontinue" : lastNode,
        } 
    ) 
    data = response.json()
    titles = data['query']['allpages']
    for title in titles: 
        titleFormatted = re.sub('\"','\\\"', re.sub('\'','\\\'', title['title']))
        with open('wikinodelist.tsv', 'at', encoding='utf-8') as nodeList:
            nodeList.write(f'{titleFormatted}\n')
    return data['continue']['apcontinue']
i = 0
x = genTitles()
while x and i < 15500:
    x = genTitles(x)
    time.sleep(0.005)
print(i)

