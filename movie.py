import mysql
import mysql.connector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sqlalchemy
from nltk.tokenize import sent_tokenize
import logging
from gensim.summarization import *

engine =sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/news_db')
connection = mysql.connector.connect(user="root", password=None, host="localhost", database="news_db")
myCursor = connection.cursor()




#****************************************HABERLERİ EKLEME KISMI********************************************************************
sql="select newsContent from news"
myCursor.execute(sql)
records = myCursor.fetchall()

sql2 = "select newsID from news"
myCursor.execute(sql2)
records2=myCursor.fetchall()

myCursor.execute("delete from keywords")
myCursor.execute("alter table keywords AUTO_INCREMENT = 0")
sentences=[]

#Keywords bulma ve tabloya ekleme işlemi
for i in range(0,len(records),1):
  text = str(records[i][0])
  #print(i)


  textKeywords = keywords(text)
  if  textKeywords=="" :
    #print(str(i)+""+textKeywords + ""+str(len(text)))
    myCursor.execute("INSERT INTO keywords(keywords,contentType,contentID)  VALUES('{}',1,'{}')".format(10*(" "+text), records2[i][0]))
    #myCursor.execute("update keywords set keywords = '{}', contentType = '{}' where contentID = {}".format(textKeywords,1,i+1))
    #myCursor.execute("update staj.habert set articlesContent= '{}' where yazarid = {}".format(textSum, i + 1))

  else :

    myCursor.execute("INSERT INTO keywords(keywords,contentType,contentID)  VALUES('{}',1,'{}')".format(textKeywords,records2[i][0]))
    connection.commit()

sql8="select keywords from keywords"
myCursor.execute(sql8)
sonuc=myCursor.fetchall()


#****************************************KÖŞE YAZILARINI EKLEME KISMI********************************************************************

sql3="select articlesContent from articles"
myCursor.execute(sql3)
records3 = myCursor.fetchall()

sql4 = "select articlesID from articles"
myCursor.execute(sql4)
records4=myCursor.fetchall()

#Keywords bulma ve tabloya ekleme işlemi
"""""
for i in range(0,len(records3),1):
  text = str(records3[i][0])

  try:
    textSum = summarize(text,ratio=0.25)
  except:
    textSum = text
  textKeywords = keywords(textSum)
  print(textKeywords)
  #myCursor.execute("INSERT INTO keywords(keywords,contentType,contentID)  VALUES('{}',2,'{}')".format(textKeywords,records4[i][0]))
  #myCursor.execute("update keywords set keywords = '{}', contentType = '{}' where contentID = {}".format(textKeywords,1,i+1))
  #myCursor.execute("update staj.habert set articlesContent= '{}' where yazarid = {}".format(textSum, i + 1))
  connection.commit()
"""""


df=pd.read_sql_query("SELECT * FROM news INNER JOIN categories ON news.categoryID = categories.id INNER JOIN newspapers ON news.newsPaperID = newspapers.id INNER JOIN keywords ON news.newsID = keywords.contentID WHERE keywords.contentType = 1 ORDER by newsID asc",engine)
#print(df.head())
#Öneri kısmı
#----------------------------------------------------------------------------------
#print(df.index)

def get_title_from_index(index):
	return df[df.index == index]["newsTitle"].values[0]

def get_index_from_title(title):

	return df[df.newsTitle == title]["newsID"].values[0]

#-------------------------------------------------------------------------------

#myCursor.execute("SHOW COLUMNS FROM news_db.news")
#result = myCursor.fetchall()
features = ['categoryTitle','newspaperTitle']




def combine_features(row):
  try:

    return     20*(" " + row['categoryTitle']) + 5*(" " + row['newspaperTitle'])
  except:
    print ("Error:",row)


df["combined_features"] = df.apply(combine_features,axis=1)

cv = CountVectorizer()
#print(df['combined_features'])
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
print(df.head(207))

count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

print("*****************************************************************************************")
news_user_likes_recommendation = "Ticari taksilere 'son durak' operasyonu"
news_index = get_index_from_title(news_user_likes_recommendation)-1
print(news_index)
similar_news = list(enumerate(cosine_sim[news_index]))
sorted_similar_news = sorted(similar_news,key = lambda x:x[1], reverse=True)
print(sorted_similar_news)
i=0

print(sorted_similar_news[0][0])
print(sorted_similar_news[1][0])


for k in range(0,10):
  sqlqry = "SELECT newsTitle FROM news WHERE newsID = {}".format((sorted_similar_news[k][0])+1)
  myCursor.execute(sqlqry)
  resultt = myCursor.fetchall()
  print(resultt[0][0])


"""""""""""
for new in sorted_similar_news:
  print("new[0]: ",new[0])
  print(get_title_from_index(new[0]))
  i=i+1
  if i> 50:
   break
"""""
