import streamlit as st
import os
from neo4j import GraphDatabase


# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = os.getenv("NEO4J_PASSWORD", "Gabardiop")

driver = GraphDatabase.driver(uri, auth=(username, password))
def find_relationship(person1, person2):
    with driver.session() as session:
        query = """
        MATCH p=shortestPath((a:Person {nom_complet: $person1})-[*]-(b:Person {nom_complet: $person2}))
        RETURN p
        """
        result = session.run(query, person1=person1, person2=person2)
        return result.data()

st.title("Recherche de relations familiales")
person1 = st.text_input("Nom de la première personne")
person2 = st.text_input("Nom de la deuxième personne")
if st.button("Rechercher"):
    result = find_relationship(person1, person2)
    st.write(result)