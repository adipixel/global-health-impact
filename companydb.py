import sqlite3
import pandas as pd
import math
conn = sqlite3.connect('ghi.db')



conn.execute('''DROP TABLE IF EXISTS manudis''')
conn.execute('''DROP TABLE IF EXISTS manutot''')
conn.execute('''DROP TABLE IF EXISTS company2015''')
#conn.execute('''DROP TABLE IF EXISTS company2010''')

conn.execute('''DROP TABLE IF EXISTS patent2010''')
conn.execute('''DROP TABLE IF EXISTS patent2013''')

#conn.execute('''DROP TABLE IF EXISTS manudis''')
conn.execute('''CREATE TABLE manudis
             (company text, disease text, daly2010 real, daly2013 real, color text)''')

conn.execute('''CREATE TABLE manutot
             (company text, daly2010 real, daly2013 real,  color text)''')

conn.execute('''CREATE TABLE company2015
             (company text, disease text, daly2010 real, daly2015 real, color text)''')

conn.execute('''CREATE TABLE patent2010
            (company text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchocerciasis real, lf real, total real, color text)''')
conn.execute('''CREATE TABLE patent2013
            (company text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchocerciasis real, lf real, total real, color text)''')

datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
datasrc2015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv'

df = pd.read_csv(datasrc, skiprows=1)
df2 = pd.read_csv(datasrc2015, skiprows=1)
print(df)
i = 0;
colorlist = []
colors = ['FFB31C','0083CA','EF3E2E','003452','86AAB9','CAEEFD','546675','8A5575','305516','B78988','BAE2DA','B1345D','5B75A7','906F76','C0E188','DE9C2A','F15A22','8F918B','F2C2B7','F7C406','B83F98','548A9B','D86375','F1DBC6','0083CA','7A80A3','CA8566','A3516E','1DF533','510B95','DFF352','F2C883','E3744D','26B2BE','5006BA','B99BCF','DC2A5A','D3D472','2A9DC4','C25C90','65A007','FE3289','C6DAB5','DDF6AC','B7E038','1ADBBD','3BC6D5','0ACD57','22419F','D47C5B']
for x in colors:
    y = '#'+x
    colorlist.append(y)
print(colorlist)
manudata = []
manutotal = []

print('==========bug==========')
print(df.iloc[13,96])
tb2013=0
tb2010=0

for k in range(8,10):
    print(df.iloc[k,96])
    tb2013 += float(df.iloc[k,96].replace('-','0').replace(',',''))
    tb2010 += float(df.iloc[k,45].replace('-','0').replace(',',''))



hiv2013 = float(df.iloc[13,96].replace('-','0').replace(',',''))
hiv2010 = float(df.iloc[13,45].replace('-','0').replace(',',''))

total2013 =tb2013 + hiv2013
total2010 =tb2010 + hiv2010

color= colors[0]
print("tb2010")
print(tb2010)

#--------------Jing Add excel alleviated Burden ---------------------
sumtb2015 = 0
summar2015 = 0
sumhiv2015 = 0

sumtb2010 = 0
summar2010 = 0
sumhiv2010 = 0

for k in range(7,10):

    sumtb2015 += float(df2.iloc[k,96].replace('-','0').replace(',',''))
    sumtb2010 += float(df2.iloc[k,45].replace('-','0').replace(',',''))

for k in range(10,12):
    print("==========new stroage========")
    print(df2.iloc[k,45])
    summar2015 += float(df2.iloc[k,96].replace('-','0').replace(',',''))
    summar2010 += float(df2.iloc[k,45].replace('-','0').replace(',',''))

sumhiv2015 = float(df2.iloc[12,96].replace('-','0').replace(',',''))
sumhiv2010 = float(df2.iloc[12,45].replace('-','0').replace(',',''))

sumtotal2015 =sumtb2015 + summar2015 + sumhiv2015
sumtotal2010 =sumtb2010 + summar2010 + sumhiv2010

#print('2015====++=========')
#print(sumhiv2015)

#--------------Jing-----------------
unalle = 'Unalleviated Burden'
disease1 = 'tb'
row = [unalle,disease1,tb2010,tb2013,color]
manudata.append(row)
conn.execute('insert into manudis values (?,?,?,?,?)', row)
#unalle = 'Unalleviated Burden'


disease2 = 'hiv'
row = [unalle,disease2,hiv2010,hiv2013,color]
manudata.append(row)
conn.execute('insert into manudis (company,disease,daly2010,daly2013,color) values (?,?,?,?,?)',row)

disease3 = 'all'

row = [unalle,disease3,total2010,total2013,color]
manudata.append(row)
conn.execute('insert into manudis (company,disease,daly2010,daly2013,color)  values (?,?,?,?,?)', row)


#--------Jing---------end---------
#=========add 2015 to database========Jing====
i=0
print("2015=================")
disease = 'tb'
row = [unalle,disease,sumtb2010,sumtb2015,color]
conn.execute('insert into company2015 (company,disease,daly2010,daly2015,color) values (?,?,?,?,?)', row)
disease='malaria'
row = [unalle,disease,summar2010,summar2015,color]
conn.execute('insert into company2015 (company,disease,daly2010,daly2015,color) values (?,?,?,?,?)', row)
disease='hiv'
row = [unalle,disease,sumhiv2010,sumhiv2015,color]
conn.execute('insert into company2015 (company,disease,daly2010,daly2015,color) values (?,?,?,?,?)', row)
disease='all'
row = [unalle,disease,sumtotal2010,sumtotal2015,color]
conn.execute('insert into company2015 (company,disease,daly2010,daly2015,color) values (?,?,?,?,?)', row)

for k in range(25,85):
    company = df2.iloc[k,2]
    print("company=====")
    print(company)
    if isinstance(company,float):
        if math.isnan(company):
            break
    disease = 'tb'


    #temp =  df2.iloc[k,4]
    if df2.iloc[k,3]== " " or df2.iloc[k,3].replace(' ','') == "-":
        tbdaly2010 = 0
    else: tbdaly2010 = float(df2.iloc[k,3].replace('-','').replace(',',''))

    if df2.iloc[k,4]== " ":
        tbdaly2015 = 0
    else: tbdaly2015 = float(df2.iloc[k,4].replace('-','').replace(',',''))


    #temp = df2.iloc[k,4].replace('-','0').replace(',','')
    print('=====tbdaly2015=====')
    print(tbdaly2015)
    #tbdaly2015 = float(temp)
    if tbdaly2015 > 0 or tbdaly2010 > 0:
        color = colors[i]
        print('=====tbdaly2015=====')
        print(tbdaly2015)
        row=[company,disease,tbdaly2010,tbdaly2015,color]
        manudata.append(row)
        i += 1
        conn.execute('insert into company2015 values (?,?,?,?,?)', row)

i=0
for k in range(25,85):
    company = df2.iloc[k,5]
    print("company=====")
    print(company)
    if isinstance(company,float):
        if math.isnan(company):
            break
    disease = 'hiv'

    if df2.iloc[k,6]== " ":
        tbdaly2010 = 0
    elif isinstance(df2.iloc[k,6],float):
        if math.isnan(df2.iloc[k,6]):
            tbdaly2010 = 0
    elif  df2.iloc[k,6] =="nan":
        tbdaly2010 = 0

    else: tbdaly2010 = float(df2.iloc[k,6].replace('-','0').replace(',',''))

    if df2.iloc[k,7]== " ":
        tbdaly2015 = 0
    else: tbdaly2015 = float(df2.iloc[k,7].replace('-','0').replace(',',''))

    print("=====hiv 2016===========")
    print(tbdaly2015)

    if tbdaly2015 > 0 or tbdaly2010 > 0 :
        color = colors[i]
        row=[company,disease,tbdaly2010,tbdaly2015,color]
        manudata.append(row)
        i += 1
        conn.execute('insert into company2015 values (?,?,?,?,?)', row)

i=0
for k in range(25,85):
    company = df2.iloc[k,8]
    print("company=====")
    print(company)
    if isinstance(company,float):
        if math.isnan(company):
            continue
    disease = 'malaria'
    #print(df2.iloc[k,9])
    if df2.iloc[k,9]== " " :
        tbdaly2010 = 0
    elif isinstance(df2.iloc[k,9],float):
        if math.isnan(df2.iloc[k,9]):
            tbdaly2010 = 0
    else: tbdaly2010 = float(df2.iloc[k,9].replace('-','0').replace(',',''))
    print(tbdaly2010)
    if df2.iloc[k,10]== " " :
        tbdaly2015 = 0
    elif isinstance(df2.iloc[k,10],float):
        if math.isnan(df2.iloc[k,10]):
            tbdaly2015 = 0
    else: tbdaly2015 = float(df2.iloc[k,10].replace('-','0').replace(',',''))
    print(tbdaly2015)
    if tbdaly2015 > 0 or tbdaly2010 > 0:
        color = colors[i]
        row=[company,disease,tbdaly2010,tbdaly2015,color]
        manudata.append(row)
        i += 1
        print("===============row ============")
        print(row)
        conn.execute('insert into company2015 values (?,?,?,?,?)', row)

print("2015=============end====")
#=========end 2015===========================

for k in range(25,88):
    company = df.iloc[k,2]
    #print(company)
    if isinstance(company,float):
        if math.isnan(company):
            break
    disease = 'tb'
    temp = df.iloc[k,3].replace('-','0').replace(',','')

    tbdaly2010 = float(temp)
    tbdaly2013 = float(df.iloc[k,4].replace('-','0').replace(',',''))
    if tbdaly2010 > 0 or tbdaly2013 > 0:
        color = colors[i]
        row=[company,disease,tbdaly2010,tbdaly2013,color]
        manudata.append(row)
        i += 1
        conn.execute('insert into manudis (company,disease,daly2010,daly2013,color)  values (?,?,?,?,?)', row)
i=0
for k in range(25,88):
    company = df.iloc[k,6]
    if isinstance(company,float):
        if math.isnan(company):
            break
    disease = 'hiv'
    print("temp===df2013==")
    print(df.iloc[k,10])
    if df.iloc[k,10].replace(' ','') =="#REF!":
        hivdaly2010 = 0
    else :hivdaly2010 = float(df.iloc[k,10].replace('-','0').replace(',',''))
    hivdaly2013 = float(df.iloc[k,11].replace('-','0').replace(',',''))
    if hivdaly2010 > 0 or hivdaly2013 > 0:
        color = colors[i]
        row=[company,disease,hivdaly2010,hivdaly2013,color]
        i += 1
        manudata.append(row)
        conn.execute('insert into manudis (company,disease,daly2010,daly2013,color)  values (?,?,?,?,?)', row)
i=0
for k in range(25,88):
    company = df.iloc[k,12]
    if isinstance(company,float):
        if math.isnan(company):
            break
    if df.iloc[k,13].replace(' ','') =="#REF!":
        daly2010 = 0
    else : daly2010 = float(df.iloc[k,13].replace('-','0').replace(',',''))
    daly2013 = float(df.iloc[k,14].replace('-','0').replace(',',''))
    if daly2010 > 0 or daly2013 > 0:
        color = colors[i]
        row=[company,daly2010,daly2013,color]
        i += 1
        manutotal.append(row)
        conn.execute('insert into manutot (company,daly2010,daly2013,color)  values (?,?,?,?)', row)

def cleanfloat(var):
    if type(var) != float:
        var = float(var.replace(',',''))
    if var != var:
        var = 0
    return var
oldrow = ['']
pat2010 = []
for i in range(1,43):
    prow = []
    comp = df.iloc[1,i]
    print(comp)
    prow.append(comp)
    for j in range(10,20):
        if j == 10:
            tb1 = cleanfloat(df.iloc[7,i])
            tb2 = cleanfloat(df.iloc[8,i])
            tb3 = cleanfloat(df.iloc[9,i])
            tb=[tb1,tb2,tb3]
            temp = (tb1+tb2+tb3)
            prow.append(temp)
        elif j == 11:
            mal1 = cleanfloat(df.iloc[10,i])
            mal2 = cleanfloat(df.iloc[11,i])
            mal=[mal1,mal2]
            temp = (mal1+mal2)
            prow.append(temp)
        elif j == 19:
            total = cleanfloat(df.iloc[j,i])
            prow.append(total)
        else:
            temp = df.iloc[j,i]
            #print("temp========")
            #print(temp)
            if isinstance(temp,float):
                 if math.isnan(temp):
                     temp = 0
            elif temp.replace(' ','') == "#REF!":
                temp = 0
            elif isinstance(temp,float) == False and isinstance(temp,int) == False :
                temp = float(temp.replace(',',''))
            if temp != temp:
                temp = 0
            prow.append(temp)
    if prow[0] == oldrow [0]:
        for ind in range(1,len(prow)):
            prow[ind] += oldrow[ind]
    oldrow = prow
    if comp != df.iloc[1,i+1]:
        pat2010.append(prow)
unmet = ['Unmet Need']
for j in range(10,20):
    if j == 10:
        #print(df.iloc[7,46])
        tb1 = cleanfloat(df.iloc[8,46])
        tb2 = cleanfloat(df.iloc[9,46])
        tb3 = cleanfloat(df.iloc[10,46])
        tb=[tb1,tb2,tb3]
        temp = (tb1+tb2+tb3)
        unmet.append(temp)
    elif j == 11:
        mal1 = cleanfloat(df.iloc[11,46])
        mal2 = cleanfloat(df.iloc[12,46])
        mal=[mal1,mal2]
        temp = (mal1+mal2)
        unmet.append(temp)
    elif j == 19:
        total = cleanfloat(df.iloc[j,46])
        unmet.append(total)
    else:
        temp = df.iloc[j,46]
        if temp == '#VALUE!' or temp.replace(' ','') == "#REF!":
            temp = 0
        if isinstance(temp,float) == False and isinstance(temp,int) == False:
            temp = float(temp.replace(',',''))
        if temp != temp:
            temp = 0
        unmet.append(temp)
pat2010.append(unmet)
colind = 0
for item in pat2010:
    item.append(colors[colind])
    colind+=1
    conn.execute(' insert into patent2010 values (?,?,?,?,?,?,?,?,?,?,?,?) ', item)
#print(pat2010)


oldrow = ['']
pat2013 = []
for i in range(50,91):
    prow = []
    comp = df.iloc[1,i]
    prow.append(comp)
    for j in range(10,20):
        if j == 10:
            tb1 = cleanfloat(df.iloc[7,i])
            tb2 = cleanfloat(df.iloc[8,i])
            tb3 = cleanfloat(df.iloc[9,i])
            tb=[tb1,tb2,tb3]
            temp = (tb1+tb2+tb3)
            prow.append(temp)
        elif j == 11:
            mal1 = cleanfloat(df.iloc[10,i])
            mal2 = cleanfloat(df.iloc[11,i])
            mal=[mal1,mal2]
            temp = (mal1+mal2)
            prow.append(temp)
        elif j == 19:
            total = cleanfloat(df.iloc[j,i])
            prow.append(total)
        else:
            temp = df.iloc[j,i]
            if isinstance(temp,float):
                 if math.isnan(temp):
                     temp = 0
            elif temp.replace(' ','') == "#REF!":
                temp = 0

            elif isinstance(temp,float) == False and isinstance(temp,int) == False:
                temp = float(temp.replace(',',''))
            if temp != temp:
                temp = 0
            prow.append(temp)
    if prow[0] == oldrow [0]:
        for ind in range(1,len(prow)):
            prow[ind] += oldrow[ind]
    oldrow = prow
    if comp != df.iloc[1,i+1]:
        pat2013.append(prow)
unmet = ['Need']
for j in range(10,20):
    if j == 10:
        #print(df.iloc[8,93])
        tb1 = cleanfloat(df.iloc[8,94])
        tb2 = cleanfloat(df.iloc[9,94])
        tb3 = cleanfloat(df.iloc[10,94])
        tb=[tb1,tb2,tb3]
        temp = (tb1+tb2+tb3)
        unmet.append(temp)
    elif j == 11:
        mal1 = cleanfloat(df.iloc[11,94])
        mal2 = cleanfloat(df.iloc[12,94])
        mal=[mal1,mal2]
        temp = (mal1+mal2)
        unmet.append(temp)
    elif j == 19:
        total = cleanfloat(df.iloc[j,94])
        unmet.append(total)
    else:
        temp = df.iloc[j,94]
        if isinstance(temp,float):
                 if math.isnan(temp):
                     temp = 0
        elif temp.replace(' ','') == "#REF!":
                temp = 0

        elif isinstance(temp,float) == False and isinstance(temp,int) == False:
            temp = float(temp.replace(',',''))
        if temp != temp:
            temp = 0
        unmet.append(temp)
pat2013.append(unmet)
colind = 0
for item in pat2013:
    item.append(colors[colind])
    colind+=1
    conn.execute(' insert into patent2013 values (?,?,?,?,?,?,?,?,?,?,?,?) ', item)
#print(pat2013)

conn.commit()