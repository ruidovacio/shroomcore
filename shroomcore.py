from tkinter import *
import requests
import json
from PIL import Image, ImageTk
import io
from urllib.parse import quote

URL = "https://toxicshrooms.vercel.app/api/mushrooms"
root = Tk()
root.title("shroomcore")


def fetch_urls(url):  # funcion que hace fetch del api
    print("cargando...")
    response = requests.get(url)
    if response.status_code == 200:
        print("todo ok")
        fetched_lista = response.json()
        print(f"cargada lista con {len(fetched_lista)} valores")
        filtered_lista = [item for item in fetched_lista if (item.get("img"))]
        filtered_lista = [
            item for item in filtered_lista if (item.get("commonname"))]
        filtered_lista = [
            item for item in filtered_lista if (item.get("agent"))]
        print(f"clean up con {len(filtered_lista)} valores")
        return filtered_lista
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
    # global set_type
    # global index
    # set_type = change
    # index = 0
    # change_index(1)
    pass


def cargar_imagen():
    global index
    img_url = shrooms[index]["img"]
    encoded_url = quote(img_url, safe='/:?=&')
    try:
        img_response = requests.get(
            encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
        print(img_response)
        img_cargar = Image.open(io.BytesIO(img_response.content))
        img_filtros = img_cargar.resize((200, 200), Image.NEAREST).convert(
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

b_all = Button(botonera_tipo, text="a", padx=20, pady=20,
               command=lambda: change_type("all")).pack(side="left")
b_poison = Button(botonera_tipo, text="p", padx=20, pady=20,
                  command=lambda: change_type("poison")).pack(side="left")
b_death = Button(botonera_tipo, text="d", padx=20, pady=20,
                 command=lambda: change_type("death")).pack(side="left")

botonera_change = Frame(root)
botonera_change.pack(side="right")


b_prev = Button(botonera_change, text="<<", padx=20, pady=20, command=lambda: change_index(-1)
                ).pack(side="left")
# .grid(column=3, row=2)
b_next = Button(botonera_change, text=">>", padx=20, pady=20, command=lambda: change_index(1)
                ).pack(side="left")
# .grid(column=4, row=2)

update()
root.mainloop()
