from fastapi import FastAPI
import pandas as pd

import nltk
nltk.download('punkt')
nltk.download('stopwords')


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ast

import numpy as np



#LEER EL DATASET
df = pd.read_csv('./dataset.csv')

#CREAR LA INSTANCIA DE LA APLICACION FASTAPI
app = FastAPI()


df['release_date'] =pd.to_datetime(df['release_date'])
df['actors'] = df['actors'].apply(lambda x: ast.literal_eval(x))
df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x))
df['director'] = df['director'].apply(lambda x: ast.literal_eval(x))
df.loc[df["overview"].isnull(),"overview"] = ""

#MAPEO DE LOS MESES Y DIAS PARA UTILZARLO EN LAS FUNCIONES
meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}

dias = {'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3,
    'viernes': 4, 'sabado': 5, 'domingo': 6}


#ENDPOINT RAIZ
@app.get("/")
def root():
    return {"message": "Desarrrollo API por Argenis Bolivar"}

#PRIMER ENDPOINT

@app.get("/Cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):

    # Mapear el mes ( convertirlo a numero)
    mes_num = meses.get(mes.lower())

    if mes_num is None:
        return {"mensaje": f"Mes '{mes}' no es válido. Por favor ingresa un mes correcto."}

    # Realizar la consulta de cuantas peliculas fueron estrenadas
    cantidad = df[(df['status']=='Released')&(df['release_date'].dt.month == mes_num)].shape[0]
    mensaje = f"{cantidad} de peliculas fueron estrenadas en el mes de  {mes}"
    return  {"mensaje" : mensaje}
    
#SEGUNDO ENDPOINT

@app.get("/Cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_mes(dia: str):
    # Mapear el dia ( convertirlo a numero)
    dia_num = dias.get(dia.lower())
    
    if dia_num is None:
        return {"mensaje": f"Dia '{dia}' no es válido. Por favor ingresa un mes correcto."}

    # Realizar la consulta de cuantas peliculas fueron estrenadas
    cantidad = df[(df['status']=='Released')&(df['release_date'].dt.weekday == dia_num)].shape[0]
    mensaje = f"{cantidad} de peliculas fueron estrenadas un  {dia}"
    return  {"mensaje": mensaje}


#TERCER ENDPOINT

@app.get("/Score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo: str):
    
    #Filtar dataset por el titulo
    df_1 = df[df["title"].str.lower() == titulo.lower()]
    if df_1.empty:
        return {"mensaje": f"No se encontró información para la pelicula '{titulo}'."}

    #Extraer la informacion que requerimos del dataset
    titulo = df_1.loc[0,"title"]
    año = df_1.loc[0,"release_date"].year
    score = df_1.loc[0,"vote_average"]


    mensaje = f"La pelicula {titulo} fue estrenada en el año {año} con un score de {score}"
    return  {"mensaje": mensaje}


#CUARTO ENDPOINT

@app.get("/Votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo: str):
    
    #consulta
    df_1 = df[df["title"].str.lower() == titulo.lower()].reset_index()

    if df_1.empty:
        return {"mensaje": f"No se encontró información para la pelicula '{titulo}'."}

    if (df_1.loc[0,'vote_count'] < 2000):
        return {"mensaje": f"Existe menos de 2000 valoraciones para esta pelicula, no se puede calcular el score."}
        
    else:
        titulo = df_1.loc[0,"title"]
        votaciones = df_1.loc[0,"vote_count"]
        score = df_1.loc[0,"vote_average"]
        año = df_1.loc[0,"release_date"].year

        mensaje = f"La pelicula {titulo} fue estrenada en el año {año}, cuenta con un total de {votaciones} valoraciones y un promedio de {score}"
        return  {"mensaje", mensaje}




#QUINTO ENDPOINT

@app.get("/Get_actor/{actor}")
def get_actor(actor: str):
     
    #consulta


    df_actor = df[df['actors'].apply(lambda x: actor.lower() in [a.lower() for a in x])]
    
    if df_actor.empty:
        return {"mensaje": f"No se encontró información para el actor '{actor}'."}
    
    retorno_total_actor = round(float(df_actor['return'].sum()),2)
    cantidad_peliculas_actor = df_actor.shape[0]
    promedio_retorno_actor = round(float(df_actor['return'].mean()),2)
    
    mensaje = f"El actor {actor} ha participado en {cantidad_peliculas_actor} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total_actor} con un promedio de {promedio_retorno_actor} por filmación"
     
    
    return  {"mensaje": mensaje}



#SEXTO ENDPOINT

@app.get("/Get_director/{director}")
def get_director(director: str):
     

    #consulta
    df_director= df[df['director'].apply(lambda x: director.lower() in [a.lower() for a in x])]

    if df_director.empty:
        return {"mensaje": f"No se encontró información para el director '{director}'."}
    
    df_director = df_director[['title', 'release_date', 'return', 'budget', 'revenue']].set_index('title')
    nuevo_dict = {'Director': director, 'peliculas': df_director.to_dict('index')}

    
    return  {'mensaje':nuevo_dict}




stop_words = set(stopwords.words('english'))  #Conjunto que se utiliza para filtrar palabras irrelevantes (en Ingles)

#Funcion para tokenizar cadena de texto
def tokenizacion(texto):
    texto = texto.lower()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(texto)
    return [palabra for palabra in tokens if palabra not in stop_words]


df['texto_procesado'] = df['actors']+df['director']+df['genres']
df['texto_procesado'] = [' '.join(sentence) for sentence in df['texto_procesado']]
df['texto_procesado'] = df['texto_procesado']+" " +df['overview']
df['texto_procesado'] = df['texto_procesado'].apply(lambda x: tokenizacion(x)) 
df['texto_procesado'] = [' '.join(sentence) for sentence in df['texto_procesado']]


vector = TfidfVectorizer()
tfidf_vectores = vector.fit_transform(df['texto_procesado'])
tfidf_vectores = tfidf_vectores.astype(np.float32)




@app.get("/Recomendacion/{titulo}")
def recomendacion(titulo: str):
     # Buscar dentro del Dataframe, el indice que corresponda al titulo buscado
    idx = df[df['title'] == titulo].index[0]
    
    # Calculo de similitud del coseno entre el vector que representa el titulo y el resto de los vectores
    similitud_coseno = cosine_similarity(tfidf_vectores[idx],tfidf_vectores).flatten()
    similitud = list(enumerate(similitud_coseno))
    
    # Ordenar similitud de mayor a menor: para ver quienen tienen mayor similitud
    similitud = sorted(similitud, key=lambda x: x[1], reverse=True)
    
    # Obtener las 5 recoemndaciones
    top_n=5
    indices = [i[0] for i in similitud[1:top_n+1]]


    resultados = {index: df['title'].iloc[index] for index in indices}
    return resultados











    

