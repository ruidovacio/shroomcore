from tkinter import *
import requests
import json
from PIL import Image, ImageTk, ImageEnhance
import io
import os
from urllib.parse import quote

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

URL = "https://toxicshrooms.vercel.app/api/mushrooms"
root = Tk()
root.title("shroomcore")
root.resizable(False, False)


def fetch_urls(url):  # funcion que hace fetch del api
    print("cargando...")
    response = requests.get(url)
    if response.status_code == 200:
        global all_lista
        global deadly_lista
        global poison_lista
        print("todo ok")
        fetched_lista = response.json()
        print(f"cargada lista con {len(fetched_lista)} valores")
        all_lista = [item for item in fetched_lista if (item.get("img"))]
        all_lista = [
            item for item in all_lista if (item.get("commonname"))]
        all_lista = [
            item for item in all_lista if (item.get("agent"))]
        print(f"clean up con {len(all_lista)} valores")
        deadly_lista = [item for item in all_lista if(item["type"]=="deadly")]
        poison_lista = [item for item in all_lista if(item["type"]=="poisonous")]
        return poison_lista
    else:
        print(response.status_code)


def change_index(change):  # funcion de los botones
    global index
    global clicked_button
    clicked_button = change
    if (index+change >= len(shrooms)):
        index = 0
    elif (index+change < 0):
        index = len(shrooms)-1
    else:
        index += change
    update()


def change_type(change):
    global shrooms
    global index
    index = 0
    if (change == "poisonous"):
        shrooms = poison_lista
    elif (change == "deadly"):
        shrooms = deadly_lista
    print(len(shrooms))
    update()


def cargar_imagen():
    global index
    img_url = shrooms[index]["img"]
    encoded_url = quote(img_url, safe='/:?=&')
    try:
        img_response = requests.get(
            encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
        print(img_response)
        img_cargar = Image.open(io.BytesIO(img_response.content))
        mejorar = ImageEnhance.Color(img_cargar)
        img_saturar = mejorar.enhance(4)
        img_filtros = img_saturar.resize((200, 200), Image.NEAREST).convert(
            'P', palette=Image.ADAPTIVE, colors=16).resize((425, 425), Image.NEAREST)
        img_done = ImageTk.PhotoImage(img_filtros)
        display.config(image=img_done)
        display.image = img_done
    except:
        print("error cargando imagen, cambiando...")
        change_index(clicked_button)


def update():  # actualizar info
    print("-------------")
    print(f"cargando indice {index}")
    # print(shrooms[index])
    nombre.config(text=shrooms[index]["commonname"])
    descripcion.config(
        text=f'{shrooms[index]["name"]} \n [{shrooms[index]["agent"]}] \n {shrooms[index]["type"]}')
    cargar_imagen()


# cargar la lista
global shrooms
shrooms = fetch_urls(URL)
index = 0

# cargar el gui

display = Label(root, image=None)
display.pack()

textos_frame = Frame(root, borderwidth=1, relief="sunken")
textos_frame.pack(ipady=10, expand="true", fill="both")

nombre = Label(textos_frame, font=("Arial 15 bold"), text=None)
nombre.pack(side="top")

descripcion = Label(
    textos_frame, text=None)
descripcion.pack(expand="true", fill="both", side="top")

botonera_tipo = Frame(root)
botonera_tipo.pack(side="left")

img_poison = ImageTk.PhotoImage(Image.open('icons/shroom.png').resize((50,50),Image.NEAREST))
b_all = Button(botonera_tipo, text="a", image=img_poison, padx=20, pady=20,
               command=lambda: change_type("poisonous")).pack(side="left")
img_death = ImageTk.PhotoImage(Image.open('icons/deadly.png').resize((50,50),Image.NEAREST))
b_death = Button(botonera_tipo, text="d", image=img_death, padx=20, pady=20,
                 command=lambda: change_type("deadly")).pack(side="left")

botonera_change = Frame(root)
botonera_change.pack(side="right")

img_prev = ImageTk.PhotoImage(Image.open('icons/left.png').resize((50,50),Image.NEAREST))
b_prev = Button(botonera_change, text="<<", image=img_prev, padx=20, pady=20, command=lambda: change_index(-1)
                ).pack(side="left")

img_next = ImageTk.PhotoImage(Image.open('icons/right.png').resize((50,50),Image.NEAREST))
b_next = Button(botonera_change, text=">>", image=img_next, padx=20, pady=20, command=lambda: change_index(1)
                ).pack(side="left")

update()
root.mainloop()
