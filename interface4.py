import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import time

# Connexion à la base de données
def get_data_from_db():
    try:
        connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="projtiot"
        )
        cursor = connexion.cursor()
        query = "SELECT id, nom, prenom, action, temps FROM check_in"
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Matricule", "Nom", "Prénom", "Action", "Temps"])
        cursor.close()
        connexion.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Erreur de connexion à la base de données : {err}")
        return None

# Calculer le nombre d'employés actuellement présents aujourd'hui
def calculate_today_presence(df):
    if df is None or df.empty:
        return 0

    # Assurez-vous que la colonne Temps est en datetime
    df["Temps"] = pd.to_datetime(df["Temps"])

    # Filtrer les données pour aujourd'hui
    today = date.today()
    df_today = df[df["Temps"].dt.date == today]

    # Si aucune donnée pour aujourd'hui, retourner 0
    if df_today.empty:
        return 0

    # Trouver la dernière action pour chaque employé (par Matricule)
    df_today = df_today.sort_values(by=["Matricule", "Temps"], ascending=[True, True])
    last_actions = df_today.groupby("Matricule").tail(1)

    # Compter les employés avec la dernière action étant "Entrée"
    currently_present = last_actions[last_actions["Action"] == "Entrée"].shape[0]
    return currently_present

# Diagramme en bâtons pour les check-ins par jour
def plot_check_in_bar_chart(df):
    if df is None or df.empty:
        st.warning("Aucune donnée pour générer le diagramme en bâtons.")
        return

    df["Jour"] = pd.to_datetime(df["Temps"]).dt.day_name()
    check_in_counts = df.groupby("Jour")["Matricule"].count()

    # Réorganiser l'ordre des jours de la semaine
    jours_ordres = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    check_in_counts = check_in_counts.reindex(jours_ordres, fill_value=0)

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    check_in_counts.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Nombre de Check-Ins par Jour de la Semaine", fontsize=16)
    plt.xlabel("Jour de la Semaine", fontsize=14)
    plt.ylabel("Nombre de Check-Ins", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(plt)

# Courbe pour les check-ins par jour
def plot_check_in_line_chart(df):
    if df is None or df.empty:
        st.warning("Aucune donnée pour générer la courbe.")
        return

    df["Jour"] = pd.to_datetime(df["Temps"]).dt.day_name()
    check_in_counts = df.groupby("Jour")["Matricule"].count()

    # Réorganiser l'ordre des jours de la semaine
    jours_ordres = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    check_in_counts = check_in_counts.reindex(jours_ordres, fill_value=0)

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    check_in_counts.plot(kind="line", marker="o", color="green")
    plt.title("Nombre de Check-Ins par Jour de la Semaine", fontsize=16)
    plt.xlabel("Jour de la Semaine", fontsize=14)
    plt.ylabel("Nombre de Check-Ins", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(plt)

# Titre de l'application
st.title("Interface de Suivi des Entrées et Sorties")

# Récupérer les données
df = get_data_from_db()

# Afficher les données dans un tableau
if df is not None and not df.empty:
    st.subheader("Historique des Entrées et Sorties des Utilisateurs")
    st.dataframe(df)  # Affiche la table des données

    # Calculer le nombre d'employés présents aujourd'hui
    currently_present = calculate_today_presence(df)

    # Afficher le compteur
    st.subheader("Compteur des Employés Actuellement Présents Aujourd'hui")
    st.metric(label="Employés présents", value=currently_present)

    # Afficher les graphiques
    st.subheader("Statistiques des Check-Ins")
    
    # Diagramme en bâtons
    st.write("**Diagramme en Bâtons des Check-Ins par Jour de la Semaine**")
    plot_check_in_bar_chart(df)
    
    # Courbe
    st.write("**Courbe des Check-Ins par Jour de la Semaine**")
    plot_check_in_line_chart(df)
else:
    st.warning("Aucune donnée disponible dans la base de données.")
