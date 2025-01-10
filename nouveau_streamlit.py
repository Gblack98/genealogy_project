import streamlit as st
import json
from neo4j import GraphDatabase
import os

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = os.getenv("NEO4J_PASSWORD", "Gabardiop")
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_people_list(tx):
    """
    Récupère la liste des personnes disponibles dans la base de données.
    """
    query = """
    MATCH (p:Person)
    RETURN p.nom_complet AS nom_complet
    """
    result = tx.run(query)
    return [record["nom_complet"] for record in result]

def get_family_tree(tx, root_person):
    """
    Récupère l'arbre généalogique à partir d'une personne racine.
    """
    query = """
    MATCH path = (root:Person {nom_complet: $root_person})-[:PARENT_DE*]->(descendant:Person)
    WITH root, descendant, relationships(path) AS rels
    RETURN root, descendant, rels
    """
    result = tx.run(query, root_person=root_person)
    return [{"root": record["root"], "descendant": record["descendant"], "rels": record["rels"]} for record in result]

def format_tree_for_d3(data):
    """
    Formate les données pour D3.js.
    """
    tree = {"name": data[0]["root"]["nom_complet"], "children": []}
    for entry in data:
        parent = entry["root"]["nom_complet"]
        child = entry["descendant"]["nom_complet"]
        # Ajouter l'enfant à l'arbre
        tree["children"].append({"name": child})
    return tree

def get_tree_data(root_person):
    """
    Récupère et formate les données de l'arbre généalogique.
    """
    with driver.session() as session:
        data = session.read_transaction(get_family_tree, root_person)
        return format_tree_for_d3(data)

# Interface Streamlit
st.title("Arbre Généalogique Interactif")

# Récupérer la liste des personnes disponibles
with driver.session() as session:
    people_list = session.read_transaction(get_people_list)

# Sélection de la personne racine
root_person = st.selectbox("Choisissez la personne racine :", people_list, index=people_list.index("Asta Madièye Diop") if "Asta Madièye Diop" in people_list else 0)

if st.button("Afficher l'arbre"):
    tree_data = get_tree_data(root_person)
    st.write("Données de l'arbre :", tree_data)
    
    # Définir le contenu HTML et JavaScript directement dans une chaîne de caractères
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Arbre Généalogique</title>
        <script src="https://d3js.org/d3.v6.min.js"></script>
        <style>
            .node circle {{
                fill: #fff;
                stroke: steelblue;
                stroke-width: 3px;
            }}
            .node text {{
                font: 14px sans-serif;
                fill: #333;
            }}
            .link {{
                fill: none;
                stroke: #999;
                stroke-width: 2px;
            }}
            svg {{
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <script>
            var treeData = {json.dumps(tree_data)};

            var margin = {{top: 20, right: 120, bottom: 20, left: 120}},
                width = window.innerWidth - margin.right - margin.left,
                height = window.innerHeight - margin.top - margin.bottom;

            var svg = d3.select("body").append("svg")
                .attr("width", width + margin.right + margin.left)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var root = d3.hierarchy(treeData);
            var tree = d3.tree().size([height, width]);

            tree(root);

            var link = svg.selectAll(".link")
                .data(root.links())
                .enter().append("path")
                .attr("class", "link")
                .attr("d", d3.linkHorizontal()
                    .x(function(d) {{ return d.y; }})
                    .y(function(d) {{ return d.x; }})
                );

            var node = svg.selectAll(".node")
                .data(root.descendants())
                .enter().append("g")
                .attr("class", "node")
                .attr("transform", function(d) {{ return "translate(" + d.y + "," + d.x + ")"; }});

            node.append("circle")
                .attr("r", 10);

            node.append("text")
                .attr("dy", ".35em")
                .attr("x", function(d) {{ return d.children ? -13 : 13; }})
                .style("text-anchor", function(d) {{ return d.children ? "end" : "start"; }})
                .text(function(d) {{ return d.data.name; }});
        </script>
    </body>
    </html>
    """
    
    # Afficher l'arbre dans Streamlit
    st.components.v1.html(html_content, height=800)