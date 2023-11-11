import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

file_path = 'NetflixOriginals.csv'

# Charger le jeu de données avec un encodage spécifié
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    # Si l'encodage 'utf-8' échoue, essayer 'latin-1' ou 'ISO-8859-1'
    df = pd.read_csv(file_path, encoding='latin-1')

# Convertir la colonne 'Premiere' au format datetime
df['Premiere'] = pd.to_datetime(df['Premiere'], errors='coerce', format='%d-%b-%y')

# Mise en page de l'application Streamlit
st.title("Tableau de bord des films Netflix")

# Afficher les données brutes
st.subheader('Données brutes')
st.write(df)

# Élément interactif : Filtre par genre et langue
selected_genre = st.selectbox('Sélectionnez un genre :', ['Tous'] + list(df['Genre'].unique()))
selected_language = st.selectbox('Sélectionnez une langue :', ['Toutes'] + list(df['Language'].unique()))

# Filtrer les données en fonction du genre et de la langue sélectionnés
filtered_data = df.copy()
if selected_genre != 'Tous':
    filtered_data = filtered_data[filtered_data['Genre'] == selected_genre]
if selected_language != 'Toutes':
    filtered_data = filtered_data[filtered_data['Language'] == selected_language]

# Graphique 1 : Afficher les statistiques
st.subheader(f"Statistiques pour le genre {selected_genre} et la langue {selected_language} :")
st.write(filtered_data[['IMDB Score', 'Runtime']].describe())

# Graphique 2 : Top 5 des films par score IMDB
st.subheader('Top 5 des films par score IMDB')
if not filtered_data.empty:
    top_5_movies = filtered_data.nlargest(5, 'IMDB Score')[['Title', 'IMDB Score']]
    st.table(top_5_movies.set_index('Title'))

# Graphique 3 : Graphique d'évolution pour le score IMDB
st.subheader('L\'évolution pour le score IMDB')
if not filtered_data.empty:
    imdb_evolution = filtered_data.groupby('Premiere')['IMDB Score'].mean()
    st.line_chart(imdb_evolution)

# Graphique 4 : Histogramme pour la durée
st.subheader('La distribution des durées')
fig, ax = plt.subplots()
ax.hist(filtered_data['Runtime'], bins=20, edgecolor='black')
ax.set_xlabel('Durée des films')
ax.set_ylabel('Fréquence des films')
st.pyplot(fig)

# Graphique 5 : Area Chart pour la distribution des films par date de sortie au fil du temps (cumulatif)
st.subheader('La distribution des films par date de sortie au fil du temps (cumulatif)')
if not filtered_data.empty:
    release_date_distribution = filtered_data.groupby('Premiere').size().cumsum().reset_index(name='Cumulative Count')
    st.area_chart(release_date_distribution.set_index('Premiere'))

