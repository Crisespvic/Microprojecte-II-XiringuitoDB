import pymongo
from pymongo import MongoClient
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

usuari_actual = None

# Funció per crear la base de dades
def crear_bd():
    # Conexió a MongoDB
    client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
    db = client["xiringuitoDB"]

    # Crear les coleccions (si no existeixen)
    usuaris = db["usuaris"]
    tumbones = db["tumbones"]
    lloguers = db["lloguers"]
    users = db["users"]


    tumbones_inicials = [{"_id": i, "Estat": "Lliure", "Preu": 40.00} for i in range(1, 21)]

    users_inicials = [
        {"_id": 1, "NomUsuari": "admin", "Contrasenya": "1234", "Permissos": "Administrador"},
        {"_id": 2, "NomUsuari": "user", "Contrasenya": "0000", "Permissos": "Usuari"}
    ]

    if tumbones.count_documents({}) == 0:
        tumbones.insert_many(tumbones_inicials)
        print("Tumbones inicials insertades correctament.")

    if users.count_documents({}) == 0:
        users.insert_many(users_inicials)
        print("Usuaris del sistema insertats correctament.")

    print("Base de dades i coleccions creades correctament.")

def insertar_tumbones_inicials():
    # Conexió a MongoDB
    client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
    db = client["xiringuito_db"]
    tumbones = db["tumbones"]

    # Inserta 20 tumbones amb estat "Lliure" y preu 40€
    _ids_inicials = [{"_id": i, "Estat": "Lliure", "Preu": 40.00} for i in range(1, 21)]

    if tumbones.count_documents({}) == 0:
        tumbones.insert_many(_ids_inicials)
        print("Tumbones inicials insertades correctament.")
    else:
        print("Tumbones inicials ja existeixen en la base de dades.")

# Funció per obtenir els permisos de l'usuari actual des de la base de dades
def obtenir_permisos(username):
    client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
    db = client["xiringuitoDB"]
    users = db["users"]
    resultat = users.find_one({"NomUsuari": username})
    permisos_usuari = resultat.get("Permissos", None) if resultat else None
    client.close()
    return permisos_usuari

# Funció per validar les credencials de l'usuari
def validar_credencials(username, password):
    try:
        client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
        db = client["xiringuitoDB"]
        users = db["users"]
        resultat = users.find_one({"NomUsuari": username, "Contrasenya": password})
        return bool(resultat)
    except Exception as e:
        print("Error de la base de dades:", e)
        return False
    finally:
        client.close()

# Funció per centrar les finestres a la pantalla
def centrar_finestra(finestra, amplada, alçada):
    screen_width = finestra.winfo_screenwidth()
    screen_height = finestra.winfo_screenheight()
    x = (screen_width // 2) - (amplada // 2)
    y = (screen_height // 2) - (alçada // 2)
    finestra.geometry(f"{amplada}x{alçada}+{x}+{y}")

# Funció per mostrar la finestra de login
def mostrar_finestra_login(root):
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x150")
    centrar_finestra(login_window, 300, 150)
    
    tk.Label(login_window, text="Nom d'usuari:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    
    tk.Label(login_window, text="Contrasenya:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def validar_login():
        global usuari_actual
        username = username_entry.get()
        password = password_entry.get()
        
        
        if validar_credencials(username, password):
            usuari_actual = username
            login_window.destroy()
            root.deiconify()
        else:
            messagebox.showerror("Error", "Credencials incorrectes")

    tk.Button(login_window, text="Login", command=validar_login).pack()
    login_window.mainloop()



#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<PRINCIPAL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def iniciar_aplicacio():
    root = tk.Tk()
    root.title("XIRINGUITO XUPITET I BECAETA")
    root.configure(bg="SteelBlue")
    root.geometry("376x294")
    root.resizable(width=False, height=False)
    button_font = ("Arial", 9, "bold")
    root.withdraw()
    global usuari_actual
    centrar_finestra(root, 376, 294)

    def nou_lloguer():
        nova_finestra = tk.Toplevel(root)
        nova_finestra.title("Nou Lloguer")
        nova_finestra.configure(bg="SteelBlue")

        x = root.winfo_x() + root.winfo_width() + 2
        y = root.winfo_y() -37

        nova_finestra.geometry(f"416x294+{x}+{y}")

        tk.Label(nova_finestra, text="Codi tumbona:", bg="Gold").grid(row=0, column=0, padx=10, pady=5)
        codi_entry = tk.Entry(nova_finestra)
        codi_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(nova_finestra, text="DNI Usuari:", bg="Gold").grid(row=1, column=0, padx=10, pady=5)
        dni_entry = tk.Entry(nova_finestra)
        dni_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(nova_finestra, text="Nom Usuari:", bg="Gold").grid(row=2, column=0, padx=10, pady=5)
        nom_entry = tk.Entry(nova_finestra)
        nom_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(nova_finestra, text="Telèfon Usuari:", bg="Gold").grid(row=3, column=0, padx=10, pady=5)
        telefon_entry = tk.Entry(nova_finestra)
        telefon_entry.grid(row=3, column=1, padx=10, pady=5)

        def llogar_tumbona():
            client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
            db = client["xiringuitoDB"]

            tumbones = db["tumbones"]
            usuaris = db["usuaris"]
            lloguers = db["lloguers"]

            codi = codi_entry.get()
            dni = dni_entry.get()
            nom = nom_entry.get()
            telefon = telefon_entry.get()

            if not dni:
                messagebox.showwarning("Advertència", "Si us plau, introdueix el DNI per poder llogar la tumbona.", parent=root)
                return

            try:
                # Verifica que la tumbona existeix
                tumbona = tumbones.find_one({'_id': int(codi)})
                if not tumbona:
                    messagebox.showwarning("Advertència", "Aquesta tumbona no existeix.", parent=root)
                    return

                # Verifica l'estat de la tumbona
                if tumbona['Estat'] == "Lliure":
                    # Actualitza o crea l'usuari
                    usuaris.update_one({'dni': dni}, {'$set': {'nom': nom, 'telefon': telefon}}, upsert=True)
                    
                    # Actualitza l'estat de la tumbona a "Ocupada"
                    tumbones.update_one({'_id': int(codi)}, {'$set': {'Estat': "Ocupada"}})
                    
                    # Afegeix el lloguer
                    data_actual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    lloguers.insert_one({'Usuari': dni, 'Tumbona': codi, 'Data_Inici': data_actual, 'Data_Fi': None})
                    
                    messagebox.showinfo("Info", "Lloguer realitzat amb èxit", parent=root)
                else:
                    messagebox.showwarning("Advertència", "Aquesta tumbona ja està ocupada.", parent=root)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=root)
            finally:
                client.close()
                nova_finestra.destroy()


        llogar_button = tk.Button(nova_finestra, text="Llogar", width=53, height=5, bg="Gold", font=button_font, command=llogar_tumbona)
        llogar_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def cobrar_lloguer():
        permisos_usuari = obtenir_permisos(usuari_actual)
        if permisos_usuari == 'Administrador':
            nova_finestra = tk.Toplevel(root)
            nova_finestra.title("Cobrar lloguer")
            nova_finestra.configure(bg="SteelBlue")

            x = root.winfo_x() - root.winfo_width() -25
            y = root.winfo_y() -38

            nova_finestra.geometry(f"400x164+{x}+{y}")

            tk.Label(nova_finestra, text="Codi Tumbona:", bg="Gold").grid(row=0, column=0, padx=10, pady=5)
            codi_entry = tk.Entry(nova_finestra)
            codi_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(nova_finestra, text="DNI Client:", bg="Gold").grid(row=1, column=0, padx=10, pady=5)
            dni_entry = tk.Entry(nova_finestra)
            dni_entry.grid(row=1, column=1, padx=10, pady=5)

            def cobrar():
                codi = codi_entry.get()
                dni = dni_entry.get()

                client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
                db = client["xiringuitoDB"]
                lloguers = db["lloguers"]
                tumbones = db["tumbones"]

                if codi and dni:
                    try:
                        # Busca el lloguer actiu per aquesta tumbona i client
                        lloguer = lloguers.find_one({'Tumbona': codi, 'Usuari': dni, 'Data_Fi': None})
                        if lloguer:
                            # Busca el preu de la tumbona
                            tumbona = tumbones.find_one({'_id': int(codi)})
                            if tumbona:
                                preu = tumbona['Preu']
                                messagebox.showinfo("Info", f"Import cobrat: {preu} euros", parent=root)

                                # Actualitza la data de fi del lloguer
                                data_fi = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                                lloguers.update_one({'_id': lloguer['_id']}, {'$set': {'Data_Fi': data_fi}})
                                
                                # Actualitza l'estat de la tumbona a "Lliure"
                                tumbones.update_one({'_id': int(codi)}, {'$set': {'Estat': "Lliure"}})
                            else:
                                messagebox.showerror("Error", "No s'ha trobat cap tumbona amb aquest codi.", parent=root)
                        else:
                            messagebox.showerror("Error", "El codi de la tumbona o el DNI de l'usuari no coincideixen amb cap entrada a la taula de lloguers.", parent=root)
                    except Exception as e:
                        messagebox.showerror("Error", str(e), parent=root)
                    finally:
                        client.close()
                        nova_finestra.destroy()
                else:
                    messagebox.showwarning("Advertència", "Si us plau, introdueix el codi de la tumbona i el DNI del client correctament.", parent=root)
            
            # Botó (pantalla emergent) per a cobrar la tumbona
            cobrar_button = tk.Button(nova_finestra, text="Cobrar", width=50, height=5, bg="Gold", font=button_font, command=cobrar)
            cobrar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        else:
            messagebox.showerror("Accés Denegat", "No tens permisos d'administrador per accedir a aquesta funcionalitat.", parent=root)
    
    def mostrar_informacio_beneficis(benefici, tumbones_cobrades):
        nova_finestra = tk.Toplevel()
        nova_finestra.title("Recompte de Beneficis")
        nova_finestra.configure(bg="SteelBlue")
        x = root.winfo_x() - root.winfo_width() -25
        y = root.winfo_y() +164
        nova_finestra.geometry(f"400x164+{x}+{y}")

        if tumbones_cobrades is not None:
            label_beneficis = tk.Label(nova_finestra, text=f"El total de beneficis és: {benefici} euros", bg="Gold", font=("Helvetica", 14))
            label_beneficis.pack(pady=20)
        else:
            label_no_beneficis = tk.Label(nova_finestra, text="No hi ha cap tumbona llogada actualment.", bg="Gold", font=(button_font, 16))
            label_no_beneficis.pack(pady=20)

        nova_finestra.mainloop()

    def consultar_beneficis():
        client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
        db = client["xiringuitoDB"]

        # Crear les coleccions (si no existeixen)
        usuaris = db["usuaris"]
        tumbones = db["tumbones"]
        lloguers = db["lloguers"]
        users = db["users"]

        permisos_Usuari = obtenir_permisos(usuari_actual)
        if permisos_Usuari == 'Administrador':
            try:
                tumbones_cobrades = lloguers.count_documents({'Data_Fi': {'$ne': None}})
                # La consulta per obtenir el preu de les tumbones és incorrecta.
                # Cal obtenir només un preu ja que totes les tumbones tenen el mateix preu.
                preu_tumbona = tumbones.find_one({}, {'Preu': 1})
                if preu_tumbona:
                    benefici = tumbones_cobrades * preu_tumbona['Preu']
                else:
                    benefici = 0
                mostrar_informacio_beneficis(benefici, tumbones_cobrades)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=root)
        else:
            messagebox.showerror("Accés Denegat", "No tens permisos d'administrador per accedir a aquesta funcionalitat.", parent=root)


    def mostrar_informacio(total_lliures, codisL, codisO):
        nova_finestra = tk.Toplevel()
        nova_finestra.title("Informació de Tumbones Lliures")
        nova_finestra.configure(bg="SteelBlue")

        x = root.winfo_x()
        y = root.winfo_y() - root.winfo_height() + 75
        nova_finestra.geometry(f"792x144+{x}+{y}")

        label_total = tk.Label(nova_finestra, text=f"Hi ha {total_lliures} tumbones lliures.", bg="Gold", font=("Arial", 20))
        label_total.pack(pady=10)

        label_codis_Lliures = tk.Label(nova_finestra, text=f"Lliures: {codisL}", bg="Gold", font=("Arial", 16))
        label_codis_Lliures.pack(pady=10)

        label_codis_Ocupades = tk.Label(nova_finestra, text=f"Ocupades: {codisO}", bg="Gold", font=("Arial", 16))
        label_codis_Ocupades.pack(pady=10)

        nova_finestra.mainloop()

    def consultar_tumbones_lliures():
        client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
        db = client["xiringuitoDB"]

        # Crear les coleccions (si no existeixen)
        usuaris = db["usuaris"]
        tumbones = db["tumbones"]
        lloguers = db["lloguers"]
        users = db["users"]

        try:
            total_lliures = tumbones.count_documents({'Estat': 'Lliure'})
            codi_lliures = tumbones.find({'Estat': 'Lliure'}, {'_id': 1})
            codisL = ", ".join(str(codi['_id']) for codi in codi_lliures)
            codi_ocupades = tumbones.find({'Estat': 'Ocupada'}, {'_id': 1})
            codisO = ", ".join(str(codi['_id']) for codi in codi_ocupades)

            mostrar_informacio(total_lliures, codisL, codisO)
        except Exception as e:
            print("Error:", e)

    def mostrar_dades_usuari():
        permisos_Usuari = obtenir_permisos(usuari_actual)
        if permisos_Usuari == 'Administrador':
            nova_finestra = tk.Toplevel(root)
            nova_finestra.title("Dades Usuari")
            nova_finestra.configure(bg="SteelBlue")

            x = root.winfo_x() 
            y = root.winfo_y() + 296

            nova_finestra.geometry(f"376x140+{x}+{y}")

            tk.Label(nova_finestra, text="Codi Tumbona:", bg="Gold").grid(row=0, column=0, padx=10, pady=5)
            codi_entry = tk.Entry(nova_finestra)
            codi_entry.grid(row=0, column=1, padx=10, pady=5)



            def mostrar():
                codi = codi_entry.get()

                client = MongoClient("mongodb://admin:admin@172.17.0.2:27017/")
                db = client["xiringuitoDB"]
                lloguers = db["lloguers"]
                usuaris = db["usuaris"]
                tumbones = db["tumbones"]

                if codi:
                    try:
                        # Busca el lloguer actiu per aquesta tumbona
                        lloguer = lloguers.find_one({'Tumbona': codi, 'Data_Fi': None})
                        if lloguer:
                            # Obté la informació del client
                            client_info = usuaris.find_one({'dni': lloguer['Usuari']})
                            info_text = (
                                f"Informació del client:\n"
                                f"DNI: {client_info['dni']}\n"
                                f"Nom: {client_info['nom']}\n"
                                f"Telèfon: {client_info['telefon']}\n"
                            )
                            messagebox.showinfo("Informació del client", info_text, parent=root)
                        else:
                            messagebox.showwarning("Advertència", "No s'ha trobat cap lloguer actiu per aquesta tumbona", parent=root)
                    except Exception as e:
                        messagebox.showerror("Error", str(e), parent=root)
                    finally:
                        client.close()
        else:
            messagebox.showerror("Accés Denegat", "No tens permisos d'administrador per accedir a aquesta funcionalitat", parent=root)

        crear_boto(root)
    
        # Mostrar finestra emergent (Mostrar Usuari)
        mostrar_button = tk.Button(nova_finestra, text="Mostrar", width=47, height=5 , bg="Gold" , font=button_font, command=mostrar)
        mostrar_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    # Mètode per crear el botó per mostrar les dades de l'usuari
    def crear_boto(root):
        mostrar_usuari_button = tk.Button(root, text="Mostrar Usuari", width=20, height=5 , bg="Gold" , font=button_font, command=mostrar_dades_usuari)
        mostrar_usuari_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # Botó per a llogar una tumbona
    nou_lloguer_button = tk.Button(root, text="Nou Lloguer", width=20, height=5 , bg="Gold" , font=button_font, command=nou_lloguer)
    nou_lloguer_button.grid(row=1, column=2, padx=10, pady=5)

    # Botó per efectuar un cobrament
    cobrar_button = tk.Button(root, text="Cobrar",  width=20, height=5 , bg="Gold" , font=button_font, command=cobrar_lloguer)
    cobrar_button.grid(row=3, column=2, padx=10, pady=5)

    # Botó per consultar el recompte de beneficis
    consultar_button = tk.Button(root, text="Consultar Beneficis", width=47, height=5 , bg="Gold" , font=button_font, command=consultar_beneficis)
    consultar_button.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

    # Botó per consultar el recompte de tumbones lliures
    tumbones_lliures_button = tk.Button(root, text="Tumbones Lliures", width=20, height=5 , bg="Gold" , font=button_font, command=consultar_tumbones_lliures)
    tumbones_lliures_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Botó per mostrar les dades d'un client
    mostrar_usuari_button = tk.Button(root, text="Mostrar Usuari", width=20, height=5 , bg="Gold" , font=button_font, command=mostrar_dades_usuari)
    mostrar_usuari_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    
    # Mostrar la finestra de login al iniciar el programa
    mostrar_finestra_login(root)
      
    # INICI DE L'APLICACIÓ
    root.mainloop()

# Executar la funció per crear la base de dades al iniciar el programa
crear_bd()

# Executar aplicació
iniciar_aplicacio()
