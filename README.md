# tpAA

### Instrucciones para correr las notebooks:
0. Antes de iniciar, recomendamos instalar los paquetes mediante el comando `conda env create tpAA.yml`
1. Colocar el csv cabaventa.csv en la carpeta data
2. Correr las notebooks en el siguiente orden (las notebooks generan un output que es utilizado como input en la siguiente):
   1. Pre-processing (Errores / Missings / DroppedCols, etc)
   2. Feature Engineering (features nuevas)
   3. Modelo (categorización de precio / split / RandomSearch / Evaluacion)
   
En el repositorio, también hay una notebook con el análisis exploratorio y archivos *.py con funciones o clases (como por ejemplo el archivo cleaning.py).
