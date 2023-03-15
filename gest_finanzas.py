from pymongo import MongoClient
from pprint import pprint

import customtkinter

from tkinter import messagebox

import tkinter

import progress

from datetime import datetime

import json


import os, time, sys

from PIL import Image


import random

client = MongoClient('mongodb://usstyuuw2zx04naztyai:Adjd1WKkdhAJxXVvv5cA@n1-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017,n2-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017/bcqgsfusiciyvwb?replicaSet=rs0')
db = client['bcqgsfusiciyvwb']
collection = db.ingresos

#document = {"id": "AB3DSS22", "url": "https://discord.com/api/webhooks/1060431569686376518/C98B3O76kgEFeACKqdnTtfOY2YSTt9Q18kZrJYP_-TnC71vTFB0y58xPhDAoo24nhiZl"}
#result = collection.insert_one(document)

# find documents that match a query


class Ingresos(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("650x400")

        self.maxsize(650, 350)

        self.minsize(650, 350)

        ruta = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.iconbitmap(f"{ruta}/fina.ico")

        global meses
        meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"

        }

        global mes, dia , ano

        date = datetime.now()

        

        mes = date.month
        dia = date.day   
        ano = date.year     

        self.title(f"Gestor de Finanzas  [{mes}/{dia}/{ano}] | Developed by Alejandro Duque")

        global icon
        ruta = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon = customtkinter.CTkImage(light_image=Image.open(ruta+"/fina.png"),
                                        dark_image=Image.open(ruta+"/fina.png"),
                                        size=(150, 150),
                                        )

        self.home_frame = customtkinter.CTkFrame(self)
        self.home_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", pady=30, padx=30)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=icon)
        self.home_frame_large_image_label.grid(row=1, column=0, padx=20, pady=60)

        self.frame = customtkinter.CTkFrame(master=self, width=300, height=300)
        self.frame.grid(row=0, column=3, padx=(10, 20), pady=(60, 0), sticky="nsew")
        self.frame.grid_rowconfigure(7, weight=1)


        self.add_ingresos = customtkinter.CTkButton(master=self.frame, text="Añadir Ingresos", command=self.meter_ingresos)
        self.add_ingresos.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sacar_ingresos_b = customtkinter.CTkButton(master=self.frame, text="Restar Ingresos", command=self.sacar_ingresos)
        self.sacar_ingresos_b.grid(row=1, column=0, padx=20, pady=10)

        self.ver_ingresos = customtkinter.CTkButton(master=self.frame, text="Ver Ingresos", command=self.ver_ingresos_mes)
        self.ver_ingresos.grid(row=2, column=0, padx=20, pady=10)

        self.ver_ingresos_actual = customtkinter.CTkButton(master=self.frame, text="Ver Ingresos Actual", command=self.ver_ingresos_mes_actual)
        self.ver_ingresos_actual.grid(row=3, column=0, padx=20, pady=10)

        self.ver_deuda = customtkinter.CTkButton(master=self.frame, text="Ver Deudas", command=self.checkar_deuda)
        self.ver_deuda.grid(row=0, column=1, padx=20, pady=(20, 10))

        self.ver_deuda_res = customtkinter.CTkButton(master=self.frame, text="Saldar Deuda", command=self.restar_deuda)
        self.ver_deuda_res.grid(row=1, column=1, padx=20, pady=10)

        self.depurar_mes_ = customtkinter.CTkButton(master=self.frame, text="Depurar Meses", command=self.depurar_mes)
        self.depurar_mes_.grid(row=2, column=1, padx=20, pady=10)

        self.about = customtkinter.CTkButton(master=self.frame, text="About Us", command=self.info)
        self.about.grid(row=3, column=1, padx=20, pady=10)

        


    def meter_ingresos(self):

        ingresos_add = customtkinter.CTkInputDialog(text="Cuanta es la cantidad de ingresos que deseas agregar?", title="Añadir Ingresos a DB")
        ingresos_add = ingresos_add.get_input()

        try:
            ingresos_add = int(ingresos_add)

            decicion = messagebox.askquestion("Confirmar Monto", f"Estas seguro que quieres ingresar {ingresos_add}$?", icon='warning')

            if not decicion == 'yes':
                return messagebox.showinfo("Operacion cancelada!", "La operacion se cancelo!") 
            
        except ValueError:
            return messagebox.showinfo("Error!", "El ingreso ingresado debe ser un valor numerico entero!")
        
        id=str(mes)
        query = {"id": id}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)

        actual_monto = document["monto"]

        new_values = { "$set": { "monto": int(actual_monto)+ingresos_add } }


        result = collection.update_one(query, new_values)

        messagebox.showinfo("Ingresos Actualizados!", f"Actualmente tienes: {int(actual_monto)+ingresos_add}$")


    def sacar_ingresos(self):

        ingresos_remove = customtkinter.CTkInputDialog(text="Cuanta es la cantidad de ingresos que deseas eliminar?", title="Sacar Ingresos de DB")
        ingresos_remove = ingresos_remove.get_input()

        try:
            ingresos_remove = int(ingresos_remove)

            decicion = messagebox.askquestion("Confirmar Monto", f"Estas seguro que quieres quitar {ingresos_remove}$?", icon='warning')

            if not decicion == 'yes':
                return messagebox.showinfo("Operacion cancelada!", "La operacion se cancelo!") 
            
        except ValueError:
            return messagebox.showinfo("Error!", "El ingreso ingresado debe ser un valor numerico entero!")
        
        id=str(mes)
        query = {"id": id}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)

        actual_monto = int(document["monto"])


        if ingresos_remove > actual_monto:
            return messagebox.showinfo("Error!", "Mamawebo!, No tenemos tanto dinero para restar xd")

        new_values = { "$set": { "monto": int(actual_monto)-ingresos_remove } }


        result = collection.update_one(query, new_values)

        messagebox.showinfo("Ingresos Actualizados!", f"Actualmente tenias: {int(actual_monto)}$\nNuevos Ingresos: {int(actual_monto)-ingresos_remove}$")

    def ver_ingresos_mes(self):

        mes_ele = customtkinter.CTkInputDialog(text="De cual mes quieres ver los ingresos?", title="Verificar en DB")
        mes_ele = mes_ele.get_input()

        try:
            mes_ele = int(mes_ele)
            
        except ValueError:
            return messagebox.showinfo("Error!", "El ingreso ingresado debe ser un valor numerico entero!")
        
        id=str(mes_ele)
        query = {"id": id}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)

        actual_monto = document["monto"]

        mes = meses.get(mes_ele)

        messagebox.showinfo("Verificar Ingresos", f"Actualmente tienes en el mes de {mes}: {int(actual_monto)}$")
    
    def ver_ingresos_mes_actual(self):

        date = datetime.now()

        mes = date.month
        
        id=str(mes)
        query = {"id": id}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)

        actual_monto = document["monto"]

        mes = meses.get(mes)

        messagebox.showinfo("Verificar Ingresos", f"Actualmente tienes en el mes de {mes}: {int(actual_monto)}$")

    
    def checkar_deuda(self):

        deuda = customtkinter.CTkInputDialog(text="De cual banco quieres ver tu deuda?", title="Verificar Deudas en DB")
        deuda = deuda.get_input()

        deuda = deuda.lower()

        date = datetime.now()

        mes = date.month
        
        query = {"deuda": deuda}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)

        try:

            if document["monto"] is None:

                return messagebox.showinfo("Error!", f"Parece que no esta en la base de datos el banco {deuda.upper()}!")
        except: 
            return messagebox.showinfo("Error!", f"Parece que no esta en la base de datos el banco {deuda.upper()}!")

        actual_monto = document["monto"]

        mes = meses.get(mes)

        messagebox.showinfo("Verificar Deuda", f"Actualmente tienes en el banco {deuda.upper()} una deuda de: {int(actual_monto)}$")

    
    def restar_deuda(self):

        deuda = customtkinter.CTkInputDialog(text="De cual banco quieres ver tu deuda?", title="Verificar Deudas en DB")
        deuda = deuda.get_input()

        deuda = deuda.lower()

        date = datetime.now()

        mes = date.month
        
        query = {"deuda": deuda}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)
        
        try:

            if document["monto"] is None:

                return messagebox.showinfo("Error!", f"Parece que no esta en la base de datos el banco {deuda.upper()}!")
        except: 
            return messagebox.showinfo("Error!", f"Parece que no esta en la base de datos el banco {deuda.upper()}!")

        actual_monto = document["monto"]

        mes = meses.get(mes)

        if actual_monto > 0:

            messagebox.showinfo("Verificacion de Deuda", f"Actualmente tienes en el banco {deuda.upper()} una deuda de: {int(actual_monto)}$")
        else:
            messagebox.showinfo("Verificacion de Deuda", f"Actualmente no tienes ninguna deuda en el banco {deuda.upper()}!")
            return

        ingresos_remove_deuda = customtkinter.CTkInputDialog(text="Cuanta es la cantidad de ingresos que deseas eliminar?", title="Sacar Ingresos de DB")
        ingresos_remove_deuda = ingresos_remove_deuda.get_input()

        try:
            ingresos_remove_deuda = int(ingresos_remove_deuda)

            decicion = messagebox.askquestion("Confirmar Monto", f"Estas seguro que quieres saldar {ingresos_remove_deuda}$ del total de la deuda?", icon='warning')

            if not decicion == 'yes':
                return messagebox.showinfo("Operacion cancelada!", "La operacion se cancelo!") 
            
        except ValueError:
            return messagebox.showinfo("Error!", "El ingreso ingresado debe ser un valor numerico entero!")
        
        new_values = { "$set": { "monto": actual_monto-ingresos_remove_deuda } }

        result = collection.update_one(query, new_values)

        messagebox.showinfo("Gestor de deudas", f"Se actualizo el valor de su deuda ahora es de {actual_monto-ingresos_remove_deuda}$")
        

    def depurar_mes(self):

        decicion = messagebox.askquestion("Confirmar Depuracion", f"Estas seguro que quieres depurar todos los meses (Sin contar este!)?", icon='warning')

        if not decicion == 'yes':
            return messagebox.showinfo("Operacion cancelada!", "La operacion se cancelo!")

        monto_depurado=0

        for i in range(12):

            id=str(i+1)
            query = {"id": id}
            documents = collection.find(query)

            projection = { "monto": 1 }

            document = collection.find_one(query, projection)

            actual_monto = document["monto"]


            date = datetime.now()

            mes_actual = date.month

            if not i+1 == mes_actual:

                monto_depurado = monto_depurado + int(document["monto"])

                new_values = { "$set": { "monto": 0 } }

                result = collection.update_one(query, new_values)

        messagebox.showinfo("Depuracion", f"Los meses fueron depurados de manera correcta\nMonto total depurado: {monto_depurado}")

        
        query = {"depurado": "1"}
        documents = collection.find(query)

        projection = { "monto": 1 }

        document = collection.find_one(query, projection)

        actual_monto = document["monto"]

        new_values = { "$set": { "monto": monto_depurado+int(actual_monto) } }

        result = collection.update_one(query, new_values)


    def info(self):
        messagebox.showinfo("About Gestor de Finanzas", "Gestor de finanzas es un gestor muy sencillo para llevar\nUn buen segumiento de las mismas mediante MongoDB\nEsta aplicacion fue creada sin animos de lucro.\n\nDesarrollada por: Alejandro Duque\n© Todos los derechos reservados.")
        return
    



if __name__ == "__main__":
    app = Ingresos()
    app.mainloop()

