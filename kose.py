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
sql3="select articlesContent from articles"
myCursor.execute(sql3)
records3 = myCursor.fetchall()

sql4 = "select articlesID from articles"
myCursor.execute(sql4)
records4=myCursor.fetchall()

saglik = ['ilaç','kanser','sağlk','zayıflamak','obezite','hastane',
          'sağlık bakanlığı','kan dolaşımı','kalp','yağ','stres','ağrı','doğum','hamile','sigara'
    ,'alkol','ciğer','damar','bağışık','diş','fayda','iltiha','hasta','tümör','diyabet','hijyen','kolesterol','depresyon','kilo','trans',
          'beslen','cilt','bakım','yağ','oran','uyku','psikoloji','bağırsak','prostat','kırık','ilaç','kanser','sağlk','zayıflamak','obezite','hastane',
          'sağlık bakanlığı','kan dolaşımı','kalp','yağ','stres','ağrı','doğum','hamile','sigara'
    ,'alkol','ciğer','damar','bağışık','diş','fayda','iltiha','hasta','tümör','diyabet','hijyen','kolesterol','depresyon','kilo','trans',
          'beslen','cilt','bakım','yağ','oran','uyku','psikoloji','ilaç','kanser','sağlk','zayıflamak','obezite','hastane'
          ,'ilaç','kanser','sağlk','zayıflamak','obezite','hastane','gdo','ilaç','kanser','sağlk','zayıflamak','obezite',
          'hastane','gdo','hormon','hormon','hormon','hormon','sağlık bakanlığı','kan dolaşımı','sağlık bakanlığı','kan dolaşımı','sağlık bakanlığı','kan dolaşımı'
    ,'cilt bakımı','cilt bakımı','cilt bakımı','cilt bakımı','felç','felç','felç']

spor = ['futbol','futbol','futbol','futbol','futbol','futbol','voleybol','basket','gol','top','şampiyon','şampiyon','şampiyon','şampiyon','başarı','transfer','brezilya','alman'
    ,'ispanyol','portekizli','süper','lig','premier','efeler','bayan voleybol','taktik'
    ,'teknik','defans','hücum','pres','kondisyon','kamp','final','çeyrek','yarı','son 16','puan'
    ,'stad','antrenman','soyunma odası','zirve','küme','kupa','yetenek'
    ,'oyuncu','stoper','forvet','kaleci','galatasaray','cimbom','fener','beşiktaş',
        'bonservis','kort','federer','nadal','djokovic','tenis','süper lig','süper lig','süper lig','stoper','stoper','stoper',
        'forvet','forvet','forvet','galatasaray','fenerbahçe','galatasaray','fenerbahçe','teknik direktör','çeyrek final',
        'barcelona','futbol','voleybol','basket','gol','şampiyon','başarı','transfer','brezilya','alman'
    ,'ispanyol','portekizli','süper','lig','premier','efeler','bayan voleybol','takti'
    ,'teknik','defans','hücum','pres','kondisyon','kamp','final','çeyrek','yarı','son 16','puan'
    ,'stad','antrenman','soyunma odası','zirve','küme','kupa','yetenek'
    ,'oyuncu','stoper','forvet','kaleci','galatasaray','cimbom','fener','beşiktaş',
        'bonservis','kort','federer','nadal','djokovic','tenis','futbol','futbol','futbol','soyunma odası','soyunma odası','soyunma odası'
    ,'soyunma odası','teknik direktör','teknik direktör','teknik direktör','teknik direktör' ]


ekonomi=['faiz','hazine','ekonomi','borsa','dolar','tl','kredi','işsizlik','batıyor','kriz','iflas','işyeri','borç','borc','milyar'
,'kepenk','işletme','maaş','prim','sigorta','emekli','yaptırım','banka','bank','sermaye',
         'ımf','sanayi','ucuz','paha','üretim','avro','ticari','ticaret','para','sat','pazar','dükkan','doğal gaz','petrol','yakıt','elektrik'
         ,'fatura','yatırım','amerika','abd','teknoloji','girişim','döviz','faiz','faiz','faiz','dolar','ithalat','ihracat','dış borç'
         ,'banka','banka','eyt','banka','usd','euro','iflas','kriz','işyeri','sanayi','sanayi','ucuz','pazar','satış','vergi','kdv'
         ,'ötv','faiz','hazine','ekonomi','borsa','dolar','tl','kredi','işsizlik','batıyor','kriz','iflas','işyeri','borç','borc','milyar'
         ,'kepenk','işletme','maaş','prim','sigorta','emekli','yaptırım','banka','bank','sermaye',
         'ımf','sanayi','ucuz','paha','üretim','avro','ticari','ticaret','para','sat','pazar','dükkan','doğal gaz','petrol','yakıt','elektrik'
         ,'fatura','yatırım','amerika','abd','teknoloji','girişim','döviz','girişim','döviz','girişim','döviz','girişim','döviz','zam','zam','zam','zam'
         ,'ithalat','ihracat','ithalat','ihracat','ithalat','ihracat','ithalat','ihracat','ithalat','ihracat','ithalat','ihracat','ithalat','ihracat','dolar','dolar','dolar',
         'sanayi','sanayi','sanayi','hazine','ekonomi','borsa','hazine','ekonomi','borsa','vergi','vergi','vergi','vergi','vergi','vergi','kdv','ötv']

siyaset=['amerika','israil','trump','rusya','s400','belediye','seçim','meclis','millet','vekil','vali','başkan','cumhur','ittifak'
         ,'ekrem','imamoglu','belge','rant','terör','pkk','fetö','binali','yıldırım','izmir','istanbul','başkent','kurmay'
         'hulisi','yaptırım','siyas','erdoğan','recep','devlet','bakan','pyd','işid','cumhur','katar','venezuella'
         'savunma','sondaj','yunanistan','mhp','chp','akp','parlamento','darbe','mhp','chp','akp','belge','rant'
         ,'terör','pkk','fetö','meclis','millet','vekil','vali','başkan','cumhur','binali','binali','binali','binali','binali'
         ,'meclis','meclis','meclis','meclis','pkk','fetö','pkk','fetö','pkk','fetö','vekil','vali','chp','ak parti','ak parti'
         ,'ak parti','erdoğan','erdoğan',
         'amerika', 'israil', 'trump', 'rusya', 's400', 'belediye', 'seçim', 'meclis', 'millet', 'vekil', 'vali',
         'başkan', 'cumhur', 'ittifak'
    , 'ekrem', 'imamoglu', 'belge', 'rant', 'terör', 'pkk', 'fetö', 'binali', 'yıldırım', 'izmir', 'istanbul',
         'başkent', 'kurmay'
                    'hulisi', 'yaptırım', 'siyaset', 'erdoğan', 'recep', 'devlet', 'bakan', 'pyd', 'işid', 'cumhur',
         'katar', 'venezuella'
                  'savunma', 'hava', 'sondaj', 'adalar', 'yunanistan', 'mhp', 'chp', 'akp', 'parlamento', 'darbe',
         'mhp', 'chp', 'akp', 'belge', 'rant'
    , 'terör', 'pkk', 'fetö', 'meclis', 'millet', 'vekil', 'vali', 'başkan', 'cumhur', 'binali', 'binali', 'binali',
         'binali', 'pkk', 'fetö', 'meclis'
    , 'pkk', 'fetö', 'meclis', 'pkk', 'fetö', 'meclis', 'pkk', 'fetö', 'meclis', 'vekil', 'vali', 'başkan', 'vekil',
         'vali', 'başkan', 'vekil', 'vali', 'başkan', 'siyas',
         'siyas', 'siyas', 'siyas', 'mhp', 'chp', 'akp', 'mhp', 'chp', 'akp', 'mhp', 'chp', 'akp', 'mhp', 'chp', 'akp',
         'mhp', 'chp', 'akp', 'putin', 'merkel', 'putin', 'merkel', 'putin', 'merkel'
    , 'yaptırım', 'yaptırım', 'yaptırım', 'yaptırım'
         ]

text="""
  Binali Yıldırım’ın twitter hesabından “İstanbul Rum Ortodoks Patrikhanesi Ekümenik Patriği ve İstanbul Başpiskoposu Patrik Bartholomeos’un isim gününü kutluyor, sağlıklı ve uzun bir ömür diliyorum” diye bir tweet atıldı ve kıyamet koptu… İlk tepki CHP’lilerden geldi, “Patrik hakkında nasıl olur da ‘ekümenik’ unvanını kullanırsın?” dediler, başka yerlerden de benzer tepkilerin gelmesi üzerine Binali Bey’in hesabındaki tweet bir saat sonra silindi ve yerini “ekümenik” ifadesinin geçmediği “Fener Rum Patriği Sayın Bartholomeos’un isim gününü kutlar, kendisine sağlıklı bir ömür dilerim” diyen bir başka mesaj aldı. Derken işe muhafazakârından lâikine, sağcısından solcusuna, politikacısına, hattâ Cübbeli Ahmet Hoca’ya kadar bir anda herkes dahil oldu ve Binali Bey’in “ekümenik” sözünün kullanılmasına verip veriştirildi… Ne Lozan’ın çiğnenmesi kaldı, ne bu ifadenin günah olduğu, ne de bu işin bir adım sonrasında İstanbul’un adının “Kostantinopolis”e dönme ihtimalinin bulunduğu… YANLIŞA İMAN ETMEK… Bazı yanlışlara inanmaya ve o hatâlara iman edercesine bağlanmaya pek bir meraklıyızdır… “Lozan Andlaşması’nın gizli maddelerinin olduğu ve 2023’te sona ereceği”, “Atatürk’ün gizli bir vasiyetinin bulunduğu” yahut “Hilâfet’in İngiltere’nin baskısı ile kaldırıldığı” gibisinden palavraları kastediyorum… Bu gibi saçmalıkların arasında uzun senelerden buyana “Fener Patrikhanesi’nin faaliyet alanı Lozan Andlaşması ile belirlenmiştir, Patrikhane’nin âmiri Fatih Kaymakamlığı’dır, Patrik oraya bağlıdır” şeklinde aslı-astarı olmayan bir iddia da yeralıyor ve “Fener Patrikhanesi’nin ekümenikliğini kabul ettiğimiz takdirde Lozan’ın delineceğine ve Türkiye’nin başına belâ açılacağına” inanılıyor. Binali Yıldırım’ın ilk tweetinin birbirlerinden tamamen farklı kamplara mensup olanları bile yekvücut hâle getirip “Ekümenikliğe hayır!’ dedirtmesinin sebebi, Patrikhane konusunda sımsıkı sarıldığımız bu yanlışlardır! Şimdi, Lozan bahsinde senelerden buyana yazdığım, söylediğim ama bir türlü anlatamadığım bir hususu tekrar edeyim: Lozan Andlaşması’nda Patrikhane yoktur, bu müesseseden andlaşmanın hiçbir maddesinde bahsedilmez! Mesele gerçi görüşmelerde ele alınmış, Türk tarafı Patrikhane’nin Türkiye’den gitmesini ısrarla istemiş ama karşı tarafı ikna edememiş, neticede Patrikhane yerinde kalmış fakat andlaşma metnine dahil edilmemiştir. Fener’in Fatih Kaymakamlığı’na yahut İstanbul Valiliği’ne bağlı olması diye bir şey de sözkonusu değildir; bütün bu iddialar Patrikhane meselesini kendilerine sermaye edinmiş zevâtın vaktiyle alâka çekme ve üstadlık taslama vasıtası olarak ortaya attıkları palavralardan ibrettir! İşin aslı böyle olduğu halde yıllanmış yazarların, anlı-şanlı akademisyenlerin ve memleketin birbirlerinden seçkin âlim, filozof, kanaat önderi, vesairesinin Lozan’ı bir defa olsun okumamış olmalarına rağmen Patrikhane’nin bahsinin her geçişinde hâlâ “Lozan da Lozan, canım gülüm Lozan!” diye tutturmalarına bilmem ne demek gerekir? ADAMLAR 15 ASIRDIR EKÜMENİK! Gündeme her gelişinde milletin sinirlerini oynatan “ekümenik” sözü siyasî değil dinî bir ibâredir, Klâsik Yunanca’da dünyanın “meskûn” yani “insanların yaşadığı kısmı” mânâsına gelen “he oikoumene ge” kavramından Latince’ye “oecumenicus” diye geçmiş, “ekümenik”e bizde eskiden “cihanşümûl”, sonra da “evrensel” denmiştir… Yahudi ırkına mahsus olan Musevîlik haricindeki bütün dinler ekümenik, yani evrenseldir ve bu iş bünyesinde “tebliğ” faaliyetine yer veren her itikat için şarttır… Biz kabul edelim yahut etmeyelim, Patrikhane de kendi itikadının gereği olarak 1500 küsur seneden buyana zaten ekümeniktir, “Oikemenikon Patriarkhion” yani “Ekümenik Patrikhane” unvanını tâââ o zamanlardan buyana daima kullanmış, Ortodoks kiliseleri tarafından “eşitler arasında birinci” mânâsına gelen “primus inter pares” kabul edilmiştir ve Ortodoks kiliselerinin tamamı dualarında ilk önce İstanbul’daki “Ekümenik Patrik” Bartholomeos’un ismini zikrederler… Patrikhane’nin 19. asırdaki Yunan isyanında, sonra da İstiklâl Harbi senelerinde başımıza çeşit çeşit dertler açtığını, aleyhimizde çalışan Etniki Eterya yahut Mavri Mira gibi teşkilâtları bütün gücüyle desteklediğini bilelim ve hatırlayalım, amennâ… Ama, Fener Patrikhanesi’nin zamanla bir çeşit Vatikan hâlini almasına imkân bulunmadığını, zira bunun Ortodoks doktrinine ters düştüğünü; Ortodoks kilisesinin asırlardan buyana devletin altında olduğunu, patriklerin Bizans zamanında bile hem protokolde, hem de dünyevî uygulamalarda daima İmparator’a tâbi kaldıklarını da bilelim… PATRİK FETVA VERİRSE… Yunanistan bugün Batı Trakya’daki Müslüman azınlığın kendi müftülerini seçme özgürlüklerini zorlaştırmaktadır ve bizim buna karşı “Ruhban Okulu” kartını oynamamız “mütekabiliyet esası” gereği hakkımızdır… Fakat, Batı Trakya’daki müftü seçiminin yahut Ruhban Okulu meselesinin “maddî” ve “siyasî”, ekümeniklik bahsinin ise “uhrevî” meseleler olduğunu, mütekabiliyet kuralı ile alâkasının bulunmadığını, Patrikhane’nin ekümenikliğinin ise Ortodoks kilisesi haricinde hiç kimseyi ve tabii bizi alâkadar etmeyeceğini unutmamamız şartıyla! Patrikhane’nin ekümenik olmasını kabul etmeyip “Sen ekümenik değilsiiiin!” diye bas bas bağırmamız neye benzer, bilir misiniz? Fener Patriği Bartholomeos’un günün birinde aklına esip “Müslümanlar oruç tutmayı bilmiyorlar, iftar vaktinden önce kebap yiyebilirler, oruçları bozulmaz! Ama öğle namazını da yanlış kılıyorlar! Önce iki rekât farz, sonra üç rekât sünnet olması lâzım!” diye fetva vermeye kalkışmasına… Binali Bey bu işin doğrusunu söyleyecekti ama söyletmediler!  

"""
deneme=0
text=text.lower()
for i in range(0, len(siyaset)):
    deneme = deneme + text.count(siyaset[i])
print(deneme)

for k in range(len(records3)):
    siralama=[]


    records3[k]=records3[k][0].lower()
    #print(str(k)+""+records3[k])
    sporSayi=0
    saglikSayi=0
    siyasetSayi=0
    ekonomiSayi=0
    for i in range(0,len(siyaset)):
        siyasetSayi=siyasetSayi+records3[k].count(siyaset[i])
    for i in range(0,len(ekonomi)):
        ekonomiSayi=ekonomiSayi+records3[k].count(ekonomi[i])
    for i in range(0,len(saglik)):
        saglikSayi=saglikSayi+records3[k].count(saglik[i])
    for i in range(0,len(spor)):
        sporSayi=sporSayi+records3[k].count(spor[i])



    siralama.append(siyasetSayi)
    siralama.append(ekonomiSayi)
    siralama.append(saglikSayi)
    siralama.append(sporSayi)
    katindex=siralama.index(max(siralama))#0. index siyaset 1. index ekonomi #2.index saglik #3. index spor
    print(str(katindex)+" "+ records3[k] )
    if katindex == 0 :
        sql2="UPDATE articles SET categoryID = '{}' WHERE articles.articlesID = '{}'".format(7,k+1)
        myCursor.execute(sql2)
        connection.commit()
    elif katindex == 1 :
        sql2 = "UPDATE articles SET categoryID = '{}' WHERE articles.articlesID = '{}'".format(2, k + 1)
        myCursor.execute(sql2)
        connection.commit()
    elif katindex == 2:
        sql2 = "UPDATE articles SET categoryID = '{}' WHERE articles.articlesID = '{}'".format(8, k + 1)
        myCursor.execute(sql2)
        connection.commit()
    elif katindex == 3:
        sql2 = "UPDATE articles SET categoryID = '{}' WHERE articles.articlesID = '{}'".format(3, k + 1)
        myCursor.execute(sql2)
        connection.commit()



df=pd.read_sql_query("""SELECT * FROM articles INNER JOIN categories ON articles.categoryID = categories.id INNER JOIN newspapers 
on articles.newsPaperID=newspapers.id INNER JOIN  writers on articles.writerID = writers.id ORDER by articlesID asc""",engine)
print(df.head())

def get_title_from_index(index):
	return df[df.index == index]["articlesTitle"].values[0]

def get_index_from_title(title):

	return df[df.articlesTitle == title]["articlesID"].values[0]

features = ['categoryTitle','newspaperTitle','writerName']




def combine_features(row):
  try:

    return     20*(" " + row['categoryTitle']) + 5*(" " + row['newspaperTitle']) + 1*(" " + row['writerName'])
  except:
    print ("Error:",row)


df["combined_features"] = df.apply(combine_features,axis=1)
#print(df['combined_features'])

cv = CountVectorizer()
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

print("*****************************************************************************************")
articles_user_likes_recommendation = "Ayıbın ağa babası"
news_index = get_index_from_title(articles_user_likes_recommendation)-1
print(news_index)
similar_news = list(enumerate(cosine_sim[news_index]))
sorted_similar_news = sorted(similar_news,key = lambda x:x[1], reverse=True)
print(sorted_similar_news)
i=0
for k in range(0,10):
  sqlqry = "SELECT articlesTitle FROM articles WHERE articlesID = {}".format((sorted_similar_news[k][0])+1)
  myCursor.execute(sqlqry)
  resultt = myCursor.fetchall()
  if (resultt[0][0] != articles_user_likes_recommendation):
      print(resultt[0][0])
