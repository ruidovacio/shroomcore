from tkinter import *
import requests
import json
from PIL import Image, ImageTk
import io
from urllib.parse import quote

URL = "https://toxicshrooms.vercel.app/api/mushrooms"
root = Tk()
root.title("shroomcore")
root.geometry("500x550")

def fetch_urls(url): #funcion que hace fetch del api
    print("cargando...")
    response = requests.get(url)
    if response.status_code == 200:
        print("todo ok")
        fetched_lista = response.json()
        print(f"cargada lista con {len(fetched_lista)} valores")
        for x in fetched_lista:
            if x["img"] == "":
                fetched_lista.remove(x)
        for x in fetched_lista:
            if x["commonname"] == "":
                fetched_lista.remove(x)
        for x in fetched_lista:
            if x["agent"] == "":
                fetched_lista.remove(x)
        print(f"clean up con {len(fetched_lista)} valores")
        return fetched_lista
    else:
        print(response.status_code)


def change_index(change): #funcion de los botones
    global index
    if (index+change >= len(shrooms)):
        index = 0
    elif (index+change <= 0):
        index = len(shrooms)-1
    else:
        index += change
    update()


def cargar_imagen():
    global index
    img_url = shrooms[index]["img"]
    print(img_url)
    encoded_url = quote(img_url, safe='/:?=&')
    img_response = requests.get(
        encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
    print(img_response)
    img_data = img_response.content
    img_cargar = Image.open(io.BytesIO(img_data))
    img_cargar = img_cargar.resize((200, 200), Image.NEAREST).convert(
        'P', palette=Image.ADAPTIVE, colors=16).resize((400, 400), Image.NEAREST)
    img_foto = ImageTk.PhotoImage(img_cargar)
    display.config(image=img_foto)
    display.image = img_foto

    # display.config(image=shrooms[index]["img"])
    # print(shrooms[index]["img"])


def update(): #actualizar info
    print(index)
    nombre.config(text=shrooms[index]["commonname"])
    descripcion.config(
        text=f'{shrooms[index]["name"]} \n {shrooms[index]["agent"]} \n {shrooms[index]["type"]}')
    cargar_imagen()


# cargar la lista
shrooms = fetch_urls(URL)
index = 0

# cargar el gui
nombre = Label(root, font=("Arial 15 bold"), text=None)
nombre.grid(column=1, row=0)
descripcion = Label(
    root, text=None)
descripcion.grid(column=1, row=1)

display = Label(root, image=None)
display.grid(column=1, row=2)

b_prev = Button(root, text="<<", command=lambda: change_index(-1)
                ).grid(column=0, row=3)
b_next = Button(root, text=">>", command=lambda: change_index(1)
                ).grid(column=2, row=3)

update()
root.mainloop()
