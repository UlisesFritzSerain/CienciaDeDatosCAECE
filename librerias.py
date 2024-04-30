import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from scipy import stats
#NUMPY
array = np.array([1, 2, 3, 4, 5])
print("Suma de elementos:", np.sum(array))
print("Promedio de elementos:", np.mean(array))

nro_random = np.random.rand(5)
#nro_random = np.random.randint(1, 20, size=5)
print("Datos aleatorios generados:", nro_random)


#MATPLOTLIB
data = pd.read_csv("netflix_titles.csv") 
data_filtrado = data.dropna(subset=['country'])


peliculas_por_pais = data_filtrado['country'].value_counts()


top_10_paises = peliculas_por_pais.head(10)

# Grafico y sus detallea
plt.figure(figsize=(10, 6))
top_10_paises.plot(kind='bar', color='skyblue')
plt.title('Top 10 Países con más Películas en Netflix')
plt.xlabel('País')
plt.ylabel('Cantidad de Películas')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
