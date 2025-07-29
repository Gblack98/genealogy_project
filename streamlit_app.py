import streamlit as st
from neo4j import GraphDatabase
import re
from pyvis.network import Network
import requests

# Connexion à Neo4j Aura en utilisant st.secrets pour sécuriser les identifiants
uri = st.secrets["neo4j"]["uri"] 
username = st.secrets["neo4j"]["ton_username_à_toi"] 
password = st.secrets["neo4j"]["ton_password_à_toi"] 
driver = GraphDatabase.driver(uri, auth=(username, password))

# Fonctions pour interagir avec Neo4j
def clean_name(name):
    """
    Nettoie l'entrée utilisateur :
    - Supprime les espaces en trop avant/après.
    - Réduit les espaces multiples à un seul espace.
    - Convertit en minuscules pour une recherche insensible à la casse.
    """
    return re.sub(r"\s+", " ", name.strip()).lower()

def get_suggestions(partial_name):
    """
    Récupère une liste de suggestions basées sur une entrée partielle.
    """
    partial_name = clean_name(partial_name)
    with driver.session() as session:
        query = """
        MATCH (p:Person)
        WHERE toLower(p.nom_complet) CONTAINS toLower($partial_name)
        RETURN p.nom_complet AS name
        LIMIT 10
        """
        result = session.run(query, partial_name=partial_name)
        return [record["name"] for record in result]

def find_ancestors(person):
    """
    Trouve tous les ancêtres d'une personne et retourne les nœuds et les relations.
    """
    person = clean_name(person)
    with driver.session() as session:
        query = """
        MATCH path = (a:Person)-[:PARENT_DE*]->(p:Person)
        WHERE toLower(p.nom_complet) = toLower($person)
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        """
        result = session.run(query, person=person)
        nodes = set()
        relationships = set()
        for record in result:
            nodes.update(record["nodes"])
            relationships.update(record["relationships"])
        return list(nodes), list(relationships)

def find_descendants(person):
    """
    Trouve tous les descendants d'une personne et retourne les nœuds et les relations.
    """
    person = clean_name(person)
    with driver.session() as session:
        query = """
        MATCH path = (p:Person)-[:PARENT_DE*]->(d:Person)
        WHERE toLower(p.nom_complet) = toLower($person)
        RETURN nodes(path) AS nodes, relationships(path) AS relationships
        """
        result = session.run(query, person=person)
        nodes = set()
        relationships = set()
        for record in result:
            nodes.update(record["nodes"])
            relationships.update(record["relationships"])
        return list(nodes), list(relationships)

def find_relationship(person1, person2):
    """
    Trouve la relation entre deux personnes.
    """
    person1 = clean_name(person1)
    person2 = clean_name(person2)
    with driver.session() as session:
        query = """
        MATCH p=shortestPath((a:Person)-[*]-(b:Person))
        WHERE toLower(a.nom_complet) = toLower($person1)
          AND toLower(b.nom_complet) = toLower($person2)
        RETURN nodes(p) AS nodes, relationships(p) AS relationships
        """
        result = session.run(query, person1=person1, person2=person2)
        record = result.single()
        if record:
            return record["nodes"], record["relationships"]
        else:
            return None, None

def visualize_graph(nodes, relationships, highlight_node=None):
    """
    Crée une visualisation interactive du graph avec pyvis.
    :param nodes: Liste des nœuds à afficher.
    :param relationships: Liste des relations à afficher.
    :param highlight_node: Le nœud à mettre en évidence (couleur différente).
    """
    net = Network(notebook=True, width="1200px", height="800px", directed=True)  # Dimensions augmentées
    # Ajout des nœuds
    node_ids = set()  # Pour garder une trace des nœuds ajoutés
    for node in nodes:
        if "nom_complet" in node:  # Vérifier que le nœud a bien un identifiant
            node_id = node["nom_complet"]
            node_label = node["nom_complet"]
            node_ids.add(node_id)  # Ajouter l'identifiant à l'ensemble
            # Mettre en évidence le nœud spécifié
            if highlight_node and node_id.lower() == highlight_node.lower():
                net.add_node(node_id, label=node_label, color="red", size=30)  # Taille et couleur pour le nœud mis en évidence
            else:
                net.add_node(node_id, label=node_label, color="lightblue", size=20)  # Taille et couleur par défaut

    # Ajout des relations
    for relationship in relationships:
        if hasattr(relationship, "start_node") and hasattr(relationship, "end_node"):
            start_person = relationship.start_node["nom_complet"]
            end_person = relationship.end_node["nom_complet"]
            # Vérifier que les deux nœuds existent dans le graphe
            if start_person in node_ids and end_person in node_ids:
                net.add_edge(start_person, end_person, title=relationship.type, width=2)  # Épaisseur des relations augmentée
            else:
                st.warning(f"Relation ignorée : {start_person} -> {end_person} (nœud manquant)")
        else:
            st.warning(f"Relation ignorée : format de relation invalide")

    # Générer le contenu HTML en mémoire
    html_content = net.generate_html()

    # Afficher le graph dans Streamlit
    st.components.v1.html(html_content, height=800)  # Hauteur augmentée

# Fonction pour envoyer un message via Formspree en utilisant st.secrets pour sécuriser l'endpoint
def send_via_formspree(name, email, message):
    """
    Envoie les données du formulaire à Formspree.
    """
    formspree_url = st.secrets["formspree"]["url"]  # Utilisation de st.secrets pour l'URL sécurisée
    data = {
        "name": name,
        "email": email,
        "message": message,
    }
    try:
        response = requests.post(formspree_url, data=data)
        if response.status_code == 200:
            st.success("Votre message a été envoyé avec succès !")
        else:
            st.error(f"Erreur lors de l'envoi du message : {response.status_code}")
    except Exception as e:
        st.error(f"Erreur lors de l'envoi du message : {e}")

# Styles CSS pour améliorer l'apparence
st.markdown(
    """
    <style>
    /* Titre principal */
    h1 {
        font-size: 36px !important;
        text-align: center;
    }

    /* Cases de saisie */
    .stTextInput input {
        font-size: 20px !important;
        padding: 10px !important;
    }

    /* Boutons */
    .stButton button {
        font-size: 20px !important;
        padding: 10px 20px !important;
        background-color: #2E86C1 !important;
        color: white !important;
        border-radius: 5px !important;
    }

    /* Texte */
    .stMarkdown {
        font-size: 20px !important;
    }

    /* Suggestions */
    .stMarkdown p {
        font-size: 18px !important;
        color: #2E86C1 !important;
    }

    /* Graphique */
    .stComponents iframe {
        width: 100% !important;
        height: 900px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Interface utilisateur Streamlit
st.title("Exploration Généalogique avec Neo4j")

# Sélection du type de recherche
search_type = st.selectbox(
    "Sélectionner un type de recherche",
    ["Ancêtres", "Descendants", "Relation entre deux personnes"],
    index=0,  # "Ancêtres" est sélectionné par défaut
    help="Veuillez choisir un type de recherche."
)

if search_type == "Ancêtres":
    person_input = st.text_input("Nom de la personne pour trouver ses ancêtres", key="person_ancestors")
    if person_input:
        suggestions = get_suggestions(person_input)
        if suggestions:
            st.write("Suggestions :", suggestions)
    
    if st.button("Rechercher les ancêtres"):
        if person_input:
            nodes, relationships = find_ancestors(person_input)
            if nodes:
                st.write(f"Les ancêtres de {person_input} sont :")
                visualize_graph(nodes, relationships, highlight_node=person_input)
            else:
                st.write(f"Aucun ancêtre trouvé pour {person_input}.")
        else:
            st.write("Veuillez entrer un nom de personne.")

elif search_type == "Descendants":
    person_input = st.text_input("Nom de la personne pour trouver ses descendants", key="person_descendants")
    if person_input:
        suggestions = get_suggestions(person_input)
        if suggestions:
            st.write("Suggestions :", suggestions)
    
    if st.button("Rechercher les descendants"):
        if person_input:
            nodes, relationships = find_descendants(person_input)
            if nodes:
                st.write(f"Les descendants de {person_input} sont :")
                visualize_graph(nodes, relationships, highlight_node=person_input)
            else:
                st.write(f"Aucun descendant trouvé pour {person_input}.")
        else:
            st.write("Veuillez entrer un nom de personne.")

elif search_type == "Relation entre deux personnes":
    # Champ de saisie pour la première personne
    person1_input = st.text_input("Nom de la première personne", key="person1")
    if person1_input:
        suggestions1 = get_suggestions(person1_input)
        if suggestions1:
            st.write("Suggestions :", suggestions1)

    # Champ de saisie pour la deuxième personne
    person2_input = st.text_input("Nom de la deuxième personne", key="person2")
    if person2_input:
        suggestions2 = get_suggestions(person2_input)
        if suggestions2:
            st.write("Suggestions :", suggestions2)

    # Bouton pour lancer la recherche de la relation
    if st.button("Rechercher la relation"):
        if person1_input and person2_input:
            nodes, relationships = find_relationship(person1_input, person2_input)
            if nodes and relationships:
                # Visualiser le graphique avec les deux personnes mises en évidence
                visualize_graph(nodes, relationships, highlight_node=person1_input)
            else:
                st.write("Aucune relation trouvée entre ces deux personnes.")
        else:
            st.write("Veuillez entrer les noms des deux personnes.")

# Formulaire de contact avec Formspree
st.write("---")
st.header("Contactez-moi")
st.write("Pour des feedbacks, des contributions, des suggestions ou des demandes, veuillez remplir le formulaire ci-dessous.")

with st.form("contact_form"):
    name = st.text_input("Nom complet", key="name")
    email = st.text_input("Email", key="email")
    message = st.text_area("Message", key="message")
    submit_button = st.form_submit_button("Envoyer")

    if submit_button:
        if name and email and message:
            send_via_formspree(name, email, message)
        else:
            st.warning("Veuillez remplir tous les champs du formulaire.")

# Informations de contact
st.write("---")
st.header("Informations de contact")
st.write("📧 Adresse e-mail : gabardiop1@outlook.com")
st.write("📞 Téléphone : +221775778507")
st.write("🌐 Portfolio : [Visitez mon portfolio](https://portfolio-igd.onrender.com/)")
st.write("🔗 LinkdIn :(https://www.linkedin.com/in/ibrahima-gabar-diop-730537237/)")
