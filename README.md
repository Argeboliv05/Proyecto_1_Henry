
# PROYECTO 1. MVP DE SISTEMA DE RECOMENDACION

DESCRIPCION: Este código está diseñado para crear un sistema de recomendación basado en contenido para películas. Procesa y limpia el texto asociado a cada película, lo convierte en vectores de características utilizando TF-IDF, y luego usa la similitud del coseno para encontrar y recomendar películas similares a un título dado.

ESTRUCTURA DEL PROYECTO:

1. Transformaciones: Es esta parte del proyecto se revisa los datasets que tenemos para completar un proceso de ETL. Se revisan valores faltantes, se combinas datos, se eliminan columnas innecesarias. 

Los dos dataset se concatenan y se tiene una estructura de datos organizada.

En esta parte se ejecutan transformaciones a demanda y se termina guardando un archivo.csv con un dataset limpio y sin valore faltantes importantes.

2. Analisis Exploratorio de los Datos: En este notebook se busca observar las relaciones que tiene las columnas en el datasets.

Se interta ver la relacion que existen cada uno de los generon con la popularidad de la pelicula o las ganacias obtenidas. Se terminan de limpiar datos y se genera el dataset definitivo.

Al realizar el EDA se observa la poca correlacion entre sus datos y se decide realizar un modelo basado en contenido, es decir buscar similitudes entre peliculas basado en su resumen (overview), generos, directores y actores que participan el ella. 

3. MAIN.PY: En este archivo se encuentra el desarrollo del MVP. Se desallorra una API utilizando el paquete FASTAPI y se inicia con una seria de busquedas preestablecidas para comprobar el funcionamineto del deployment.

Se desarrolla un modelo de Sistema de Recomendacion basado en contenido, es decir que tan similes son dos peliculas si observamos su overview o su genero. 

Se utiliza funciones de tokenizacion, vectorizacion y calculo de similitud de coseno para lograr recomendar 5 peliculas a partir de una que inicialmente se indica. 

En link de la aplicacion ejecutada en rende es el siguiente:
https://proyecto-1-henry-flrq.onrender.com/docs

4. requeriments.txt. lista de las dependencias del proyecto

## Authors
ARGENIS BOLIVAR

argenis.bolivar@gmail.com

www.linkedin.com/in/argenis-bolivar-aa315743

- [@Argeboliv05](https://github.com/Argeboliv05)



