import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog

data = pd.read_csv("netflix_titles.csv")  

root = tk.Tk()
root.title("Preguntas")

respuesta = None


def seleccionar_opcion(opcion):
    global respuesta
    respuesta = opcion
    root.destroy()

def hacer_pregunta(pregunta, opciones):
    global respuesta

    ventana_pregunta = tk.Toplevel()
    ventana_pregunta.title("Pregunta")

    label_pregunta = tk.Label(ventana_pregunta, text=pregunta)
    label_pregunta.pack(pady=10)

    # Función para seleccionar una opción y cerrar la ventana
    def seleccionar_opcion(opcion):
        global respuesta
        respuesta = opcion
        ventana_pregunta.destroy()

    for opcion in opciones:
        boton = tk.Button(ventana_pregunta, text=opcion, command=lambda o=opcion: seleccionar_opcion(o))
        boton.pack()

    ventana_pregunta.wait_window()

    return respuesta

def recomendar_pelicula_o_serie():
    # Preguntas
    respuestas = []
    respuestas.append(hacer_pregunta("¿Prefieres películas o series?", ["Películas", "Series"]))
    print(respuestas[0])
    if respuestas[0] is None:
        return  # Si el usuario no seleccionó ninguna opción, salimos de la función

    # Obtener los géneros top 10 que más se repiten
    if respuestas[0] == "Películas":
        generos_top = data[data['type'] == 'Movie']['listed_in'].str.split(', ').explode().value_counts().head(10).index.tolist()
    else:
        generos_top = data[data['type'] == 'TV Show']['listed_in'].str.split(', ').explode().value_counts().head(10).index.tolist()

    genero = hacer_pregunta("¿Qué género prefieres?", generos_top)
    print(genero)
    pais = simpledialog.askstring("Pregunta", "¿Tienes alguna preferencia de país? (Dejar en blanco si no tienes preferencia)")
    print("El pais es" + pais)
    actor = simpledialog.askstring("Pregunta", "¿Quieres filtrar por un actor? (Dejar en blanco si no quieres filtrar por actor)")

    if respuestas[0] == "Películas":
        duracion = hacer_pregunta("¿Cuál es la duración que prefieres?", ["Menos de 90 minutos", "Entre 90 y 150 minutos", "Más de 150 minutos"])
    else:
        duracion = hacer_pregunta("¿Cuál es la duración que prefieres?", ["Menos de 4 temporadas", "4 temporadas o más"])
    # Filtrar los datos según las respuestas del usuario
    if respuestas[0] == 'Películas':
        tipo = 'Movie'
    else:   
        tipo = 'TV Show' 
    filtro = (data['type'] == tipo)
    print(filtro)
    filtro &= data['listed_in'].str.contains(genero, case=False)
    if pais:
        filtro &= (data['country'] == pais)
    if actor:
        filtro &= (data['cast'].str.contains(actor, case=False))
    print(filtro)
    
    if respuestas[0] == "Películas":
        if "Menos de 90 minutos" in duracion:
            filtro &= (data['duration'].str.contains('^\d+ min$', case=False))
        elif "Entre 90 y 150 minutos" in duracion:
            filtro &= (data['duration'].str.contains('^\d+ min$|^\d+-\d+ min$', case=False))
        else:
            filtro &= (data['duration'].str.contains('^\d+-\d+ min$|^\d+ min$', case=False))
    else:
        if "Menos de 4 temporadas" in duracion:
            filtro &= (data['duration'].str.contains('^\d+ Seasons$', case=False))
        else:
            filtro &= (data['duration'].str.contains('^\d+ Seasons|\d+ Seasons$', case=False))
    print(filtro)
    recomendaciones = data[filtro]['title'].tolist()

    if len(recomendaciones) == 0:
        messagebox.showinfo("Sin resultados", "Lo siento, no encontré ninguna película o serie que coincida con tus preferencias.")
    else:
        messagebox.showinfo("Recomendaciones", f"¡Aquí tienes algunas recomendaciones para ti:\n{', '.join(recomendaciones)}!")
        print(data[filtro].shape[0])
    # Cerrar la ventana de preguntas
    root.destroy()

# interfaz gráfica con tkinter 
label_pregunta = tk.Label(root, text="")
label_pregunta.pack(pady=10)
botones_opciones = []

# Botón para iniciar
boton_recomendar = tk.Button(root, text="Recomendar", command=recomendar_pelicula_o_serie)
boton_recomendar.pack(pady=20)


root.mainloop()

data['cast'] = data['cast'].fillna('') 
actor_name = "Adam Sandler"
actor_filter = data['cast'].isin([actor_name]) 
filtered_data = data[actor_filter]

filtered_data = data[data['cast'].str.contains(actor_name, case=False)]
movie_titles = filtered_data['title'].tolist()
print(f"Películas en las que aparece {actor_name}:")
for title in movie_titles:
    print(title)