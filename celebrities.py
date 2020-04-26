from bs4 import BeautifulSoup
import requests
import json

# we may add more links here and iterate but for the sake of simplicity just go with one 
link = "https://www.imdb.com/list/ls068010962/"
source = requests.get(link).text 

soup = BeautifulSoup(source,'html.parser')

d = {
    "data": []
}
# print(soup.prettify())
f = soup.find_all('div',class_= 'lister-item mode-detail')

for list in f:
    # print(list.prettify())
    name = list.find('h3', class_='lister-item-header').text
    name = name.split('\n')
    name = name[2].strip()
    # print("----------------")
    about = list.find_all('p')
    about = about[1].text.strip()
    # print('---------------------')
    img = " ".join([img.get('src') for img in list.find_all('img')])
    
    d['data'].append(
        {
        
        'name':name,
        'about':about,
        'img' :img
        }
        )
    

# json_data = json.dumps(d,sort_keys=False,indent=4)
# print(json_data)

print(d)


# After scraping  we get 
# - Name
# - About 
# - Image Link

# Database Connection 
# - PyMongo

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#Make Database as celebrities 
mydb = myclient["celebrities"]
mycol = mydb['data_']
#data insertion into Database 
insert = mycol.insert_many(d['data'])
#Print inserted Data
print(insert.inserted_ids)
#Check for the values 
for x in mycol.find():
    print(x)
# here i have chosen "amzad khan"  as instance we can choose any  
for x in mycol.find({ "name": 'Amjad Khan' }):
    name = x['name']
    about =x['about']
    img = x['img']
    
print(name)
print(about)
print(img)
