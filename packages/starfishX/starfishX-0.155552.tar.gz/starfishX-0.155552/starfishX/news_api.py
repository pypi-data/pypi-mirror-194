import os
import pandas as pd
import datetime

from enum import Enum

from IPython.display import HTML

import re
english_check = re.compile(r'[a-zA-Z]')

class NewsTypeMatch(Enum):
 any = "any"
 all = "all"


from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def news_api_bydate(start_date,end_date,keyword):
    m1 = start_date.split('-')
    m2 = end_date.split('-')
    
    start_date = date(int(m1[0]), int(m1[1]), int(m1[2]))
    end_date = date(int(m2[0]), int(m2[1]), int(m2[2])) + timedelta(1)
    
    datecontent = [] 
    content_news = []
    for single_date in daterange(start_date, end_date):
      dateRange = str(single_date.strftime("%Y-%m-%d"))
     
      #ดึงข้อมูลใน Directory
      arr = os.listdir("news")
      #keyword = symbol

      dateDS = []
      content = []
      for filename in arr:
        file = "news/"+filename
        dateFilename = filename.replace("news-","").replace(".txt","")[:-3]
        
        #print(type(dateFilename),type(dateRange),dateRange,dateFilename)
        if(dateFilename==dateRange): 
          with open(file) as f:
            for line in f:
              lineP = line.lower() 
             
              for k in keyword:
                if(k in lineP):
                  #print(dateFilename+lineP)
                  datecontent.append(dateFilename)
                  lineP = lineP.replace('\n',' ')
                  content_news.append(lineP)  
                
    pd.set_option('display.max_colwidth', None)            
    return pd.DataFrame({'date':datecontent,'content':content_news})

def news_api(keyword,contentLen=100,contentShort=True,typeMatch=NewsTypeMatch.any,highlight=True):
 '''
 keyword : (list) คำที่ต้องการค้นหาในข่าว
 typeMatch : (str) มีสอง type คือ any คือคำใดคำหนึ่ง และ all คือต้อง match ทั้ง list
 '''   
 
 if(type(keyword)!=list):
   print("keyword must Type List")
   return 0

 #ดึงข้อมูลใน Directory
 arr = os.listdir("news")
 #keyword = symbol

 dateDS = []
 content = []
 for filename in arr:
  file = "news/"+filename
  date = filename.replace("news-","").replace(".txt","")[:-3]
  
  if('DS_Store' in file):
       continue 
      
  with open(file) as f:
   for line in f:
    lineP = line.lower() 
    #matching = [s for s in keyword if s.lower() in lineP]
    matching = []
    for s in keyword:
      if(s.lower() in lineP):
         #print(s.lower(),lineP)
         if(english_check.match(s.lower())):
           if(highlight):
             #print(s.upper(),s.lower())
             line = line.replace(s.upper(),"<mark>"+s.upper()+"</mark>")
             line = line.replace(s.lower(),"<mark>"+s.lower()+"</mark>")
             line = line.replace(s,"<mark>"+s+"</mark>")  #เพิ่มกรณี ตัวอักษรตัวแรกเป็นตัวใหญ่ เช่น Spin-off
           matching.append(s)
         else:
           if(highlight):
             line = line.replace(s,"<mark>"+s+"</mark>")
           matching.append(s)
    #  else:
    #     matching.append(None)
    #print(matching)


    if(typeMatch.value=="any"):
     if(len(matching)>0):
      dateDS.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
      content.append(line)
    
    if(typeMatch.value=="all"):
     if(len(matching)==len(keyword)):
      dateDS.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
      content.append(line)

 ################    
 if(len(content)==0):
    return 0

 dfNews = pd.DataFrame({"Date":dateDS,"content":content})

 #######################
 #ยุบข่าวให้ไม่ยาวเกินไป
 tmp = dfNews["content"].str.split(" ")
 shortContent = []
 for i in tmp:
  s = ""
  for j in i:
   if(len(s)+len(j)<=contentLen):
     s+=j+" "
     #print(j)
  
  shortContent.append(s.replace("\n","")) 

 pd.set_option('display.max_colwidth', None) # -1
 if(contentShort):
     dfNews["contentShort"] = shortContent
     df = dfNews[["Date","contentShort"]].sort_values(["Date"],ascending=False)
     if(highlight):
      df = HTML("<style> mark {background-color: yellow;color: black;} </style>"+df.to_html(escape=False))
      return df# = HTML(df.to_html(escape=False))

     return df 
 else:
     if(highlight):
       df = HTML("<style> mark {background-color: yellow;color: black;} </style>"+df.to_html(escape=False))
       return df# = HTML(df.to_html(escape=False))
     return dfNews.sort_values(["Date"],ascending=False)