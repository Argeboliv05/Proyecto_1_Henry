from fastapi import FastAPI
import pandas as pd

app = FastAPI()


df = pd.read_csv('./dataset.csv')
df_cast = pd.read_csv('./cast.csv')
df_crew = pd.read_csv('./crew.csv')

df['release_date'] =pd.to_datetime(df['release_date'])

#Mapeo de Meses y dias
meses = {'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
    'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
    'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'}

dias = {'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3,
    'viernes': 4, 'sabado': 5, 'domingo': 6}


@app.get("/")
def root():
    return {"message": "Desarrollo API "}

#PRIMER ENDPOINT

@app.get("/Cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    
    # Mapear el mes ( convertirlo a numero)
    mes_num = int(meses.get(mes.lower()))

    # Realizar la consulta de cuantas peliculas fueron estrenadas
    
    cantidad = df[(df['status']=='Released')&(df['release_date'].dt.month == mes_num)].shape[0]
    mensaje = f"{cantidad} de peliculas fueron estrenadas en el mes de  {mes}"
    
    return  {"mensaje", mensaje}

#SEGUNDO ENDPOINT

@app.get("/Cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_mes(dia: str):
    
    # Mapear el dia ( convertirlo a numero)
    dia_num = dias.get(dia.lower())

    # Realizar la consulta de cuantas peliculas fueron estrenadas
    
    cantidad = df[(df['status']=='Released')&(df['release_date'].dt.weekday == dia_num)].shape[0]
    mensaje = f"{cantidad} de peliculas fueron estrenadas un  {dia}"
    
    return  {"mensaje", mensaje}

#TERCER ENDPOINT

@app.get("/Score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo: str):
    
    #consulta
    df_1 = df[df["title"].str.lower() == titulo.lower()]
    titulo = df_1.loc[0,"title"]
    año = df_1.loc[0,"release_date"].year
    score = df_1.loc[0,"vote_average"]


    mensaje = f"La pelicula {titulo} fue estrenada en el año {año} con un score de {score}"
    return  {"mensaje", mensaje}

#CUARTO ENDPOINT

@app.get("/Votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo: str):
    
    #consulta
    df_1 = df[df["title"].str.lower() == titulo.lower()].reset_index()

    try:
        if (df_1.loc[0,'vote_count'] < 2000):
            raise ValueError("Error: Hay menos de 2000 reseñas de esta pelicula'")
        else:
            titulo = df_1.loc[0,"title"]
            votaciones = df_1.loc[0,"vote_count"]
            score = df_1.loc[0,"vote_average"]
            año = df_1.loc[0,"release_date"].year

            mensaje = f"La pelicula {titulo} fue estrenada en el año {año}, cuenta con un total de {votaciones} valoraciones y un promedio de {score}"
            return  {"mensaje", mensaje}
    except ValueError as e:
        return  {"mensaje", str(e)}


#QUINTO ENDPOINT

@app.get("/Get_actor/{nombre_actor}")
def get_actor(actor: str):
     
    #consulta
    id_peliculas_actor = df_cast[df_cast['actor_name'].str.lower() == actor.lower()]['id'].drop_duplicates()
    df_peliculas_actor = pd.merge(df, id_peliculas_actor, on='id', how='inner')
    cantidad_peliculas_actor = df_peliculas_actor.shape[0]
    retorno_total_actor = round(float(df_peliculas_actor['return'].sum()),2)
    romedio_retorno_actor = round(float(df_peliculas_actor['return'].mean()),2)
    
    mensaje = f"El actor {actor} ha participado en {cantidad_peliculas_actor} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total_actor} con un promedio de {romedio_retorno_actor} por filmación"
     
    
    return  {"mensaje", mensaje}


#SEXTO ENDPOINT

@app.get("/Get_director/{nombre_director}")
def get_director(director: str):
     
    #consulta
    id_peliculas_director = df_crew[(df_crew['crew_name'].str.lower()==director.lower())&(df_crew['job']=='Director')]['id'].drop_duplicates()
    df_peliculas_director = pd.merge(df, id_peliculas_director, on='id', how='inner')
    df_peliculas_director.rename(columns={'title':'Titulo', 'release_date':'Fecha_lanzamiento', 'return':'Retorno', 'budget':'Presupuesto', 'revenue':'Ganancia'}, inplace=True)
    df_peliculas_director = df_peliculas_director[['Titulo', 'Fecha_lanzamiento', 'Retorno', 'Presupuesto', 'Ganancia']].set_index('Titulo')
    nuevo_dict = {'Director': director, 'pelicula': df_peliculas_director.to_dict('index')}

    
    return  {'mensaje':nuevo_dict}