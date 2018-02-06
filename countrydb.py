import sqlite3
import pandas as pd
import math


conn = sqlite3.connect('ghi.db')

conn.execute(''' DROP TABLE IF EXISTS country2010 ''')
conn.execute(''' DROP TABLE IF EXISTS country2013 ''')
conn.execute(''' DROP TABLE IF EXISTS countryp2010 ''')
conn.execute(''' DROP TABLE IF EXISTS countryp2013 ''')

conn.execute(''' CREATE TABLE country2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, lf real) ''')
conn.execute(''' CREATE TABLE country2013 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')

conn.execute(''' CREATE TABLE countryp2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, lf real) ''')
conn.execute(''' CREATE TABLE countryp2013 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')


url = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=0&single=true&output=csv'
#url = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=0&single=true&output=csv'
##url = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/edit#gid=0&single=true&output=csv'
#url = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/edit?ts=5a0b7217#gid=0
url2 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=0&single=true&output=csv'
df = pd.read_csv(url, skiprows=1)
#df2 = pd.read_csv(
print("Inside countryDB file !!!!!!!!!!!!!!!!!!")
def cleanfloat(var):
        if var == '#REF!':
            var = 0
        if var == '#DIV/0!':
            var = 0
        if type(var) != float and type(var) != int:
            var = float(var.replace(',','').replace('%','').replace(' ','').replace('-','0'))
        if var != var:
            var = 0
        return var

countrydata = []
mapp = []
for i in range(3, 220):
    print("in range")
    print(df.iloc[i,0])
    print(df.iloc[i,7])
    print(df.iloc[i,34])
    print(df.iloc[i,47])
    print(df.iloc[i,66])
    # print(df.iloc[i,68])
    # print(df.iloc[i,76])
    # print(df.iloc[i,80])

    country = df.iloc[i,0]
    tb = cleanfloat(df.iloc[i,7])
    malaria = cleanfloat(df.iloc[i,34])
    hiv = cleanfloat(df.iloc[i,47])
    roundworm = cleanfloat(df.iloc[i,66])
    hookworm = cleanfloat(df.iloc[i,67])
    whipworm = cleanfloat(df.iloc[i,68])
    schistosomiasis = cleanfloat(df.iloc[i,76])
    lf = cleanfloat(df.iloc[i,80])
    total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + lf
    print(total)
    row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf]
    countrydata.append(row)
    #print(row)

sortedlist = sorted(countrydata, key=lambda xy: xy[1], reverse=True) # sorted descending on total
maxrow = sortedlist[0] # Country which has max total
maxval = maxrow[1] # max total
# i think it's like percentile
for j in sortedlist:
    country = j[0]
    total = (j[1]/maxval) *  100
    tb = (j[2]/maxval) *  100
    malaria = (j[3]/maxval) *  100
    hiv = (j[4]/maxval) *  100
    roundworm = (j[5]/maxval) *  100
    hookworm = (j[6]/maxval) *  100
    whipworm = (j[7]/maxval) *  100
    schistosomiasis = (j[8]/maxval) *  100
    lf = (j[9]/maxval) *  100
    row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf]
    mapp.append(row)
    #print(row)

for k in countrydata:
    conn.execute(''' INSERT INTO country2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', k)

for l in mapp:
    conn.execute(''' INSERT INTO countryp2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', l) # this is for bar chart

countrydata2 = []
mapp2 = []
for i in range(3, 220):
    country = df.iloc[i,83]
    #print(country)
    tb = cleanfloat(df.iloc[i,90])
    malaria = cleanfloat(df.iloc[i,120])
    hiv = cleanfloat(df.iloc[i,131])
    roundworm = cleanfloat(df.iloc[i,150])
    hookworm = cleanfloat(df.iloc[i,151])
    whipworm = cleanfloat(df.iloc[i,152])
    schistosomiasis = cleanfloat(df.iloc[i,160])
    onchoceriasis = cleanfloat(df.iloc[i,165])
    lf = cleanfloat(df.iloc[i,169])
    total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchoceriasis + lf
    row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
    countrydata2.append(row)

sortedlist2 = sorted(countrydata2, key=lambda xy: xy[1], reverse=True)
maxrow = sortedlist2[0]
maxval = maxrow[1]
for j in sortedlist2:
    country = j[0]
    total = (j[1]/maxval) *  100
    tb = (j[2]/maxval) *  100
    malaria = (j[3]/maxval) *  100
    hiv = (j[4]/maxval) *  100
    roundworm = (j[5]/maxval) *  100
    hookworm = (j[6]/maxval) *  100
    whipworm = (j[7]/maxval) *  100
    schistosomiasis = (j[8]/maxval) *  100
    onchoceriasis = (j[9]/maxval) * 100
    lf = (j[10]/maxval) *  100
    row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
    mapp2.append(row)

#print(countrydata2)
for k in countrydata2:
    conn.execute(''' INSERT INTO country2013 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', k)

for l in mapp2:
    conn.execute(''' INSERT INTO countryp2013 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', l)

conn.commit()