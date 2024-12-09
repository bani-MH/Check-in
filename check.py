import mysql.connector
import random 


def check_user(user_id, action):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="localhost",  # Remplacez par votre hôte
            user="root",       # Remplacez par votre utilisateur
            password="",       # Remplacez par votre mot de passe
            database="projtiot"  # Remplacez par le nom de votre base de données
        )
        cursor = conn.cursor()

        # Vérifier si l'utilisateur existe dans la table 'employer'
        query_check = "SELECT * FROM employer WHERE id = %s"
        cursor.execute(query_check, (user_id,))
        user = cursor.fetchone()

        if user:
            # Si l'utilisateur existe, insérer l'action dans la table 'check_in'
            query_insert = """
            INSERT INTO check_in (id, nom, prenom, poste, action, temps)
            VALUES (%s, %s, %s, %s, %s, NOW())  # Utilisation de NOW() pour l'heure actuelle
            """
            values = (user[0], user[1], user[2], user[3], action)  # Utilisation des infos de l'utilisateur
            cursor.execute(query_insert, values)
            conn.commit()
            print(f"L'action '{action}' pour l'utilisateur ID {user_id} a été enregistrée.")
        else:
            # Si l'utilisateur n'existe pas
            print(f"L'utilisateur avec l'ID {user_id} n'existe pas.")

    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Exemple d'utilisation de la fonction

#check_user(24, 'Entrée')
#check_user(25, 'Entrée')
#check_user(23, 'Entrée')
#check_user(26, 'Entrée')
#check_user(28, 'Entrée')
#check_user(30, 'Entrée')
check_user(28, 'Sortie')
check_user(30, 'Sortie')
check_user(23, 'Sortie')
check_user(24, 'Sortie')
check_user(25, 'Sortie')
check_user(26, 'Sortie')

check_user(3, 'Entrée')
check_user(2, 'Sortie')
check_user(50, 'Entrée')






