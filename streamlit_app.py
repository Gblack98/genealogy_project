import streamlit as st
from neo4j import GraphDatabase
import os
import re
from pyvis.network import Network
import tempfile


from neo4j import GraphDatabase
import os

# Connexion à Neo4j Aura
uri = "neo4j+s://19ede69b.databases.neo4j.io"  # Utilisez l'URI fourni
username = "neo4j"  # Nom d'utilisateur
password = "rFzyDyAC0ayPT8nqLY-AFOnMRlYzwX_jtnAwk_JE19g"  # Mot de passe

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
    Trouve tous les ancêtres d'une personne.
    """
    person = clean_name(person)
    with driver.session() as session:
        query = """
        MATCH (a:Person)-[:PARENT_DE*]->(p:Person)
        WHERE toLower(p.nom_complet) = toLower($person)
        RETURN a.nom_complet AS Ancêtre
        """
        result = session.run(query, person=person)
        return [record["Ancêtre"] for record in result]

def find_descendants(person):
    """
    Trouve tous les descendants d'une personne.
    """
    person = clean_name(person)
    with driver.session() as session:
        query = """
        MATCH (p:Person)-[:PARENT_DE*]->(d:Person)
        WHERE toLower(p.nom_complet) = toLower($person)
        RETURN d.nom_complet AS Descendant
        """
        result = session.run(query, person=person)
        return [record["Descendant"] for record in result]

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
    net = Network(notebook=True, width="100%", height="600px", directed=True)
    # Ajout des nœuds
    node_ids = set()  # Pour garder une trace des nœuds ajoutés
    for node in nodes:
        if "nom_complet" in node:  # Vérifier que le nœud a bien un identifiant
            node_id = node["nom_complet"]
            node_label = node["nom_complet"]
            node_ids.add(node_id)  # Ajouter l'identifiant à l'ensemble
            # Mettre en évidence le nœud spécifié
            if highlight_node and node_id.lower() == highlight_node.lower():
                net.add_node(node_id, label=node_label, color="red")  # Couleur rouge pour le nœud mis en évidence
            else:
                net.add_node(node_id, label=node_label, color="lightblue")  # Couleur par défaut

    # Ajout des relations
    for relationship in relationships:
        if hasattr(relationship, "start_node") and hasattr(relationship, "end_node"):
            start_person = relationship.start_node["nom_complet"]
            end_person = relationship.end_node["nom_complet"]
            # Vérifier que les deux nœuds existent dans le graphe
            if start_person in node_ids and end_person in node_ids:
                net.add_edge(start_person, end_person, title=relationship.type)
            else:
                st.warning(f"Relation ignorée : {start_person} -> {end_person} (nœud manquant)")
        else:
            st.warning(f"Relation ignorée : format de relation invalide")

    # Générer le contenu HTML en mémoire
    html_content = net.generate_html()

    # Afficher le graph dans Streamlit
    st.components.v1.html(html_content, height=600)

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
            ancestors = find_ancestors(person_input)
            if ancestors:
                st.write(f"Les ancêtres de {person_input} sont :")
                for ancestor in ancestors:
                    st.write(f"- {ancestor}")
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
            descendants = find_descendants(person_input)
            if descendants:
                st.write(f"Les descendants de {person_input} sont :")
                for descendant in descendants:
                    st.write(f"- {descendant}")
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
            

st.write("---")
st.markdown("""
    **Application développée par [Ibrahima Gabar Diop](https://portfolio-igd.onrender.com/) avec :**
    - [Streamlit](https://streamlit.io)
    - [Python3](https://Python.com)
    - [Neo4j](https://Neo4j.com)  
    - [pyvis](https://pyvis.com)
    """)            
