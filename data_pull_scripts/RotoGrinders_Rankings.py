from bs4 import BeautifulSoup
import urllib
import pandas as pd

data =[]

#Adjust number of pages to pull
for p in range(1,50):
    soup = BeautifulSoup(urllib.request.urlopen('https://rotogrinders.com/rankings?page='+str(p)).read(),'html.parser')
    tableStats = soup.find('table', attrs={'class':'tbl rankings grinders'})
    for row in tableStats.findAll('tr')[1:-1]:
        col = row.findAll('td')
        row_data=[]
        for i in range(len(col)):
            if i in [0,2,4]:
                if i == 2:
                    row_data.append(col[i].a.string.strip())
                else:
                    row_data.append(col[i].string.strip())
        data.append(row_data)

df = pd.DataFrame(data,columns =['Rank', 'Name', 'Points'])
df.to_csv('../data/RotoGrinders Rankings.csv',sep=",")