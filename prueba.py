import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog

data = pd.read_csv("netflix_titles.csv")

filtro = (data['type'] == 'Movie')
filtro &= data['listed_in'].str.contains('Dramas', case=False)
#filtro &= (data['duration'].str.contains('^\d+ min$', case=False))

recomendaciones = data[filtro]['title'].tolist()

print(data[filtro].shape[0])

#print(recomendaciones)