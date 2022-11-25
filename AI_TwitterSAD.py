# AI Twitter Sentiment Analysis for Data Science 
# Python
# Created, Modified & Testing by APKNETWORK

# Librerias necesarias para el uso de Al_TwitterSAD.py
from datetime import datetime #Extracción de atributos para el formato y la manipulación de la salida.
import re #Operaciones de coincidencia de expresiones regulares similares a las que se encuentran en Perl.
import numpy as np #Agregación soporte para arreglos y matrices grandes y multidimensionales.
import tweepy #Acceder a la API de Twitter.
from tweepy import OAuthHandler #La autenticación es manejada por la clase tweepy.AuthHandler.
from PIL import Image ##Deshuso de Pillow, elemento para cargar las imagenes.
from textblob import TextBlob #Proporcionar una API simple para sumergirse en tareas comunes de procesamiento de lenguaje natural (NLP).
import matplotlib.pyplot as plt #Herramienta para el graficado de pastel y el diagramado de nube
import pandas as pd #Manipulacion y analisis de datos para estructuras de datos y operaciones para manipular tablas numéricas y series de tiempo.
import io #Para tratar funciones principales de Python con varios tipos de E/S.
import os #Forma portátil de usar la funcionalidad dependiente del sistema operativo, para manipular os.path
import csv #Herramienta para generar los CSV
import configparser #Escribir programas de Python que los usuarios finales pueden personalizar fácilmente.
from wordcloud import WordCloud #Herramientas para crear diagramas de nube
from better_profanity import profanity #Version mejorada de la lib profanity de Ben Friendland, Limpieza increíblemente rápida de malas palabras (y su leetspeak) en cadenas

#Funcion para guardar los archivos de salida
def write_csv_type_of_param(nombre_archivo_salida,outtweets, type):
        with io.open(nombre_archivo_salida, type, encoding="utf-8", newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if type == "w":
                writer.writerow(['id', 'created_at', 'text', 'user', 'retweet_count', 'favorite_count'''])
            writer.writerows(outtweets)
        pass

# Instrucciones para leer en algunas versiones de Py archivos tipo .ini
def get_app_file_path(file):
    """Return the absolute path of the app's files. They should be in the same folder as this py file."""
    folder,_ = os.path.split(__file__)
    file_path = os.path.join(folder,file)
    return file_path

config = configparser.ConfigParser()
config.read(get_app_file_path('config.ini'))

# Asignación de las claves almacenadas del proyecto (TWITTER DEVELOP)
consumer_key = config['twitter']['api_key']
consumer_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Acceso a la data de twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True) #Wait_on_rate_limit hace la pausar al alcanzar el limite de tweepy

# Aqui va la consulta del usuario
#palabra = ['Ricardo Anaya']
palabra=['MORENA','AMLO','Cabeza de Algodón','Elecciones 2024','Marcelo Ebrard', 'Claudia Sheinbaum', 'Adán Augusto lopez', 'Ricardo Monreal', 'Candidatos Morena'] 
for x in palabra:    
    # En este caso, el proyecto que nos fue asignado requeria el arreglo de palabras sobre AMLO
    # Se filtrar la consulta para eliminar retweets
    query = input(x)
    filtered = query + "-filter:retweets"

    # Se genera los últimos tweets sobre la consulta dada
    tweets = tweepy.Cursor(api.search_tweets, 
                            q=filtered,
                            lang="en").items(300)

    # Se crea una lista de los tweets, los usuarios y su ubicación
    list1 = [[tweet.text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]

    # Se convierte la lista en un marco de datos
    df = pd.DataFrame(data=list1, 
                        columns=['tweets','user', "location"])

    # Convierte solo los tweets en una lista
    tweet_list = df.tweets.to_list()

    # Crea una función para limpiar los tweets. 
    # Eliminar las blasfemias o insultos, los caracteres innecesarios, los espacios y las palabras vacías.
    def clean_tweet(tweet):
        if type(tweet) == np.float:
            return ""
        r = tweet.lower()
        r = profanity.censor(r)
        r = re.sub("'", "", r) # Esto es para evitar quitar las contracciones en ingles.
        r = re.sub("@[A-Za-z0-9_]+","", r)
        r = re.sub("#[A-Za-z0-9_]+","", r)
        r = re.sub(r'http\S+', '', r)
        r = re.sub('[()!?]', ' ', r)
        r = re.sub('\[.*?\]',' ', r)
        r = re.sub("[^a-z0-9]"," ", r)
        r = r.split()
        #Los stopwords son palabras que normalmente no se usan al momento del analisis de sentimientos
        #stopwords = ["a","actualmente","adelante","además","afirmó","agregó","ahora","ahí","al","algo","alguna","algunas","alguno","algunos","algún","alrededor","ambos","ampleamos","ante","anterior","antes","apenas","aproximadamente","aquel","aquellas","aquellos","aqui","aquí","arriba","aseguró","así","atras","aunque","ayer","añadió","aún","bajo","bastante","bien","buen","buena","buenas","bueno","buenos","cada","casi","cerca","cierta","ciertas","cierto","ciertos","cinco","comentó","como","con","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue","consiguen","consigues","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanto","cuatro","cuenta","cómo","da","dado","dan","dar","de","debe","deben","debido","decir","dejó","del","demás","dentro","desde","después","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","e","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en","encima","encuentra","entonces","entre","era","erais","eramos","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba","estabais","estaban","estabas","estad","estada","estadas","estado","estados","estais","estamos","estan","estando","estar","estaremos","estará","estarán","estarás","estaré","estaréis","estaría","estaríais","estaríamos","estarían","estarías","estas","este","estemos","esto","estos","estoy","estuve","estuviera","estuvierais","estuvieran","estuvieras","estuvieron","estuviese","estuvieseis","estuviesen","estuvieses","estuvimos","estuviste","estuvisteis","estuviéramos","estuviésemos","estuvo","está","estábamos","estáis","están","estás","esté","estéis","estén","estés","ex","existe","existen","explicó","expresó","fin","fue","fuera","fuerais","fueran","fueras","fueron","fuese","fueseis","fuesen","fueses","fui","fuimos","fuiste","fuisteis","fuéramos","fuésemos","gran","grandes","gueno","ha","haber","habida","habidas","habido","habidos","habiendo","habremos","habrá","habrán","habrás","habré","habréis","habría","habríais","habríamos","habrían","habrías","habéis","había","habíais","habíamos","habían","habías","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","has","hasta","hay","haya","hayamos","hayan","hayas","hayáis","he","hecho","hemos","hicieron","hizo","hoy","hube","hubiera","hubierais","hubieran","hubieras","hubieron","hubiese","hubieseis","hubiesen","hubieses","hubimos","hubiste","hubisteis","ubiéramos","hubiésemos","hubo","igual","incluso","indicó","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","junto","la","lado","largo","las","le","les","llegó","lleva","llevar","lo","los","luego","lugar","manera","manifestó","mayor","me","mediante","mejor","mencionó","menos","mi","mientras","mio","mis","misma","mismas","mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","nada","nadie","ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","os","otra","otras","otro","otros","para","parece","parte","partir","pasada","pasado","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","podrá","podrán","podría","podrían","poner","por","por qué","porque","posible","primer","primera","primero","primeros","principalmente","propia","propias","propio","propios","próximo","próximos","pudo","pueda","puede","pueden","puedo","pues","que","quedó","queremos","quien","quienes","quiere","quién","qué","realizado","realizar","realizó","respecto","sabe","abeis","sabemos","saben","saber","sabes","se","sea","seamos","sean","seas","segunda","segundo","según","seis","ser","seremos","será","serán","serás","seré","seréis","sería","seríais","seríamos","serían","serías","seáis","señaló","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","su","sus","suya","suyas","suyo","suyos","sí","sólo","tal","también","tampoco","tan","tanto","te","tendremos","tendrá","tendrán","tendrás","tendré","tendréis","tendría","tendríais","tendríamos","tendrían","tendrías","tened","teneis","tenemos","tener","tenga","tengamos","tengan","tengas","tengo","tengáis","tenida","tenidas","tenido","tenidos","teniendo","tenéis","tenía","teníais","teníamos","tenían","tenías","tercera","ti","tiempo","tiene","tienen","tienes","toda","todas","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","trata","través","tres","tu","tus","tuve","tuviera","tuvierais","tuvieran","tuvierasW","tuvieron","tuviese","tuvieseis","tuviesen","tuvieses","tuvimos","tuviste","tuvisteis","tuviéramos","tuviésemos","tuvo","tuya","tuyas","tuyo","tuyos","tú","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras","vosotros","voy","vuestra","vuestras","vuestro","vuestros","ya","yo","él","éramos","ésta","éstas","éste","éstos","última","últimas","último","últimos"] #Stopwords mas famosas usadas en español
        stopwords = ["s","may","for", "on", "an", "a", "of", "and", "in", "the", "to", "from"] #Stopwords mas usadas en ingles
        r = [w for w in r if not w in stopwords]
        r = " ".join(word for word in r)
        return r

    # Se ejecute la lista de tweets a través de la función.
    cleaned = [clean_tweet(tw) for tw in tweet_list]
    now = datetime.now()
    nombre_archivo_salida = x + ' ' +now.strftime("%d-%m-%Y %H-%M-%S") + '.csv' #Se le da el nombre al archivo

    if os.path.isfile(nombre_archivo_salida):
        write_csv_type_of_param(nombre_archivo_salida,cleaned, "a");
    else:
        write_csv_type_of_param(nombre_archivo_salida,cleaned, "w");

    #f = open('path/to/csv_file', 'w')
    #writer = csv.writer(f)
    #writer.writerow(cleaned)

    print(cleaned)
    cleaned
    print()

    # Define los objetos de sentimiento usando TextBlob
    sentiment_objects = [TextBlob(tweet) for tweet in cleaned]
    sentiment_objects[0].polarity, sentiment_objects[0]

    # Crea una lista de valores de polaridad y texto de tweet
    sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

    # Imprime el valor de la fila 0.
    sentiment_values[0]

    # Imprime todos los valores de sentimiento
    sentiment_values[0:99]

    # Crea un marco de datos de cada tweet contra su polaridad
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])
    print(sentiment_df)
    print()
    sentiment_df


    # Guarda la columna de polaridad como 'n'.
    n=sentiment_df["polarity"]

    # Convierte esta columna en una serie, 'm'.
    m=pd.Series(n)

    # Inicializa variables, 'pos', 'neg', 'neu'.
    pos=0
    neg=0
    neu=0

    # Crea un ciclo para clasificar los tweets como Positivos, Negativos o Neutrales.
    # Cuenta el número de cada uno.
    for items in m:
        if items>0:
            print("Positive")
            pos=pos+1
        elif items<0:
            print("Negative")
            neg=neg+1
        else:
            print("Neutral")
            neu=neu+1
            
    print(pos,neg,neu)

    pieLabels=["Positive","Negative","Neutral"]

    populationShare=[pos,neg,neu]

    figureObject, axesObject = plt.subplots()

    axesObject.pie(populationShare,labels=pieLabels,autopct='%1.2f',startangle=90)

    axesObject.axis('equal')

    plt.show()

    # Muestra la cantidad de usuarios de Twitter que se sienten de cierta manera sobre el tema en cuestión.
    print("%f percent of twitter users feel positive about %s"%(pos,query))

    print("%f percent of twitter users feel negative about %s"%(neg,query))

    print("%f percent of twitter users feel neutral about %s"%(neu,query))

    # Crear una Wordcloud a partir de los tweets
    all_words = ' '.join([text for text in cleaned])
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

