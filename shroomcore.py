from tkinter import *
import requests
import json

URL = "https://toxicshrooms.vercel.app/api/mushrooms"
root = Tk()
root.title("shroomcore")

def fetch_urls(url):
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


shrooms = fetch_urls(URL)
index = 0

nombre = Label(root, font=("Arial 15 bold"),text=shrooms[index]["commonname"])
nombre.grid(column=1, row=0)
descripcion = Label(root, text=f'{shrooms[index]["name"]} \n {shrooms[index]["agent"]} \n {shrooms[index]["type"]}')
descripcion.grid(column=1, row=1)

def change_index(change):
    global index
    if (index+change >= len(shrooms)):
        index = 0
    elif (index+change <= 0):
        index = len(shrooms)-1
    else:
        index += change
    update()

def update():
    print(shrooms[index])
    nombre.config(text=shrooms[index]["commonname"])
    descripcion.config(text=f'{shrooms[index]["name"]} \n {shrooms[index]["agent"]} \n {shrooms[index]["type"]}')


b_prev = Button(root, text="<<", command=lambda: change_index(-1)
                ).grid(column=0, row=2)
b_next = Button(root, text=">>", command=lambda: change_index(1)
                ).grid(column=2, row=2)

root.mainloop()
