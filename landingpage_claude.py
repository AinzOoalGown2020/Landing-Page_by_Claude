import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Analyse des Sites Web - Présentation au Comité", layout="wide")

# Fonction pour charger les données
@st.cache_data
def load_data():
    columns = [
        "Sites internet", "Vitesse de chargement", "Compatibilité multiplateforme",
        "Optimisation des images", "Navigation intuitive", "Design responsive",
        "Appels à l'action (CTA)", "Certificat SSL", "Protection contre les attaques",
        "Balises Meta", "Open graph personnalisé", "Intégration des réseaux sociaux"
    ]
    # Assurez-vous que le chemin du fichier est correct
    df = pd.read_excel("data_sites_web.xlsx", usecols=columns)
    df.set_index('Sites internet', inplace=True)
    return df

# Charger les données
try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {e}")
    st.stop()

# Fonction pour créer un graphique de performance globale
def create_performance_chart(data):
    performance = data.mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=performance.index, y=performance.values, ax=ax)
    ax.set_title("Performance Moyenne par Critère", fontsize=16)
    ax.set_xlabel("Critères", fontsize=12)
    ax.set_ylabel("Score Moyen", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

# Fonction pour créer un heatmap de corrélation
def create_correlation_heatmap(data):
    corr = data.corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt='.2f')
    ax.set_title("Matrice de Corrélation des Critères", fontsize=16)
    plt.tight_layout()
    return fig

# Titre et introduction
st.title("📊 Analyse des Performances des Sites Web")
st.markdown("""
    Cette présentation offre un aperçu détaillé des performances de nos sites web
    basé sur des critères clés. Notre objectif est d'identifier les forces et les axes
    d'amélioration pour optimiser notre présence en ligne.
""")

# Métriques clés
st.header("🔑 Indicateurs Clés de Performance")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de Sites Analysés", len(df))
col2.metric("Vitesse de Chargement Moyenne", f"{df['Vitesse de chargement'].mean():.2f}")
col3.metric("Score de Compatibilité Moyen", f"{df['Compatibilité multiplateforme'].mean():.2f}")
col4.metric("Score SSL Moyen", f"{df['Certificat SSL'].mean():.2f}")

# Graphique de performance globale
st.header("📈 Performance Globale par Critère")
performance_chart = create_performance_chart(df)
st.pyplot(performance_chart)
st.markdown("""
    Ce graphique présente la performance moyenne de nos sites web pour chaque critère évalué.
    Il nous permet d'identifier rapidement nos points forts et nos axes d'amélioration.
""")

# Matrice de corrélation
st.header("🔗 Corrélations entre les Critères")
correlation_heatmap = create_correlation_heatmap(df)
st.pyplot(correlation_heatmap)
st.markdown("""
    La matrice de corrélation ci-dessus illustre les relations entre les différents critères.
    Une corrélation forte (proche de 1 ou -1) indique que deux critères évoluent souvent ensemble,
    tandis qu'une corrélation faible (proche de 0) suggère une indépendance relative.
""")

# Analyse des top performers
st.header("🏆 Analyse des Sites les Plus Performants")
top_performers = df.mean(axis=1).nlargest(5)
st.dataframe(df.loc[top_performers.index])
st.markdown("""
    Ce tableau présente nos 5 sites les plus performants en moyenne sur tous les critères.
    Ces sites peuvent servir de modèles pour l'amélioration des autres.
""")

# Comparaison des sites
st.header("🔍 Comparaison Détaillée des Sites")
selected_sites = st.multiselect("Sélectionnez des sites à comparer", df.index.tolist(), default=df.index[:3].tolist())
if selected_sites:
    comparison_df = df.loc[selected_sites]
    fig, ax = plt.subplots(figsize=(12, 6))
    comparison_df.T.plot(kind='bar', ax=ax)
    ax.set_title("Comparaison des Sites Sélectionnés", fontsize=16)
    ax.set_xlabel("Critères", fontsize=12)
    ax.set_ylabel("Score", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    ax.legend(title="Sites", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""
        Ce graphique permet de comparer directement les performances des sites sélectionnés
        sur tous les critères. Utilisez cette visualisation pour identifier les forces spécifiques
        de chaque site et les domaines nécessitant une amélioration.
    """)

# Recommandations et Conclusion (inchangés)

# Pied de page
st.markdown("---")
st.markdown("Préparé par l'équipe d'analyse web | Données mises à jour le 21/10/2024")
