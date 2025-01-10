from flask import Flask, render_template
from neo4j import GraphDatabase
from graphviz import Digraph
import base64
import os

# Connexion à Neo4j
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Gabardiop"))

def fetch_tree_data_Base1(tx):
    query = """
    MATCH (p:Person:Base1)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]

def fetch_tree_data_Base2(tx):
    query = """
    MATCH (p:Person:Base2)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]
def fetch_tree_data_Base3(tx):
    query = """
    MATCH (p:Person:Base3)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def fetch_tree_data_Base4(tx):
    query = """
    MATCH (p:Person:Base4)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def fetch_tree_data_Base5(tx):
    query = """
    MATCH (p:Person:Base5)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def fetch_tree_data_Base6(tx):
    query = """
    MATCH (p:Person:Base6)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def fetch_tree_data_Base7(tx):
    query = """
    MATCH (p:Person:Base7)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def fetch_tree_data_Base8(tx):
    query = """
    MATCH (p:Person:Base8)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def fetch_tree_data_Base9(tx):
    query = """
    MATCH (p:Person:Base9)-[r:PARENT_DE]->(c:Person)
    RETURN p.nom_complet AS parent, type(r) AS relationship, c.nom_complet AS child
    """
    result = tx.run(query)
    return [(record["parent"], record["relationship"], record["child"]) for record in result]


def create_family_tree(tree_data):
    dot = Digraph()
    
    # Paramètres de grande taille pour une disposition moderne
    dot.attr(size="25,25", dpi="300", rankdir='LR')  # Disposition horizontale (Left to Right)
    
    # Styles des nœuds modernes
    dot.attr('node', shape='ellipse', style='filled', fillcolor='#cfe2f3', color='#0b5394', 
             fontname='Arial', fontsize='20', fontcolor='#073763', width='3.5', height='2')  # Plus large et plus haut
    
    # Styles des liens avec une couleur douce
    dot.attr('edge', fontname='Arial', fontsize='16', color='#0b5394', penwidth='2.5')  # Ligne plus épaisse et couleur douce

    # Créer des nœuds et des relations pour chaque élément
    family_dict = {}
    for parent, relationship, child in tree_data:
        if parent not in family_dict:
            family_dict[parent] = []
        family_dict[parent].append(child)

    for parent, children in family_dict.items():
        dot.node(str(parent), label=parent)
        for child in children:
            dot.node(str(child), label=child)
            dot.edge(str(parent), str(child), label="Enfant", color="#3d85c6", fontcolor="#3d85c6")

    return dot




app = Flask(__name__)

@app.route('/')
def index():
    with driver.session() as session:
        tree_data_Base1 = session.read_transaction(fetch_tree_data_Base1)
        tree_data_Base2 = session.read_transaction(fetch_tree_data_Base2)
        tree_data_Base3 = session.read_transaction(fetch_tree_data_Base3)
        tree_data_Base4 = session.read_transaction(fetch_tree_data_Base4)
        tree_data_Base5 = session.read_transaction(fetch_tree_data_Base5)
        tree_data_Base6 = session.read_transaction(fetch_tree_data_Base6)
        tree_data_Base7 = session.read_transaction(fetch_tree_data_Base7)
        tree_data_Base8 = session.read_transaction(fetch_tree_data_Base8)
        tree_data_Base9 = session.read_transaction(fetch_tree_data_Base9)


        



    family_tree_Base1 = create_family_tree(tree_data_Base1)
    family_tree_Base2 = create_family_tree(tree_data_Base2)
    family_tree_Base3 = create_family_tree(tree_data_Base3)
    family_tree_Base4 = create_family_tree(tree_data_Base4)
    family_tree_Base5 = create_family_tree(tree_data_Base5)
    family_tree_Base6 = create_family_tree(tree_data_Base6)
    family_tree_Base7 = create_family_tree(tree_data_Base7)
    family_tree_Base8 = create_family_tree(tree_data_Base8) 
    family_tree_Base9 = create_family_tree(tree_data_Base9)

    family_tree_path_Base1 = '/tmp/family_tree_Base1.png'
    family_tree_path_Base2 = '/tmp/family_tree_Base2.png'
    family_tree_path_Base3 = '/tmp/family_tree_Base3.png'
    family_tree_path_Base4 = '/tmp/family_tree_Base4.png'
    family_tree_path_Base5 = '/tmp/family_tree_Base5.png'
    family_tree_path_Base6 = '/tmp/family_tree_Base6.png'
    family_tree_path_Base7 = '/tmp/family_tree_Base7.png'
    family_tree_path_Base8 = '/tmp/family_tree_Base8.png'
    family_tree_path_Base9 = '/tmp/family_tree_Base9.png'



    family_tree_Base1.format = 'png'
    family_tree_Base2.format = 'png'
    family_tree_Base3.format = 'png'
    family_tree_Base4.format = 'png'
    family_tree_Base5.format = 'png'
    family_tree_Base6.format = 'png'
    family_tree_Base7.format = 'png'
    family_tree_Base8.format = 'png'
    family_tree_Base9.format = 'png'


    family_tree_Base1.render(filename='/tmp/family_tree_Base1')
    family_tree_Base2.render(filename='/tmp/family_tree_Base2')
    family_tree_Base3.render(filename='/tmp/family_tree_Base3')
    family_tree_Base4.render(filename='/tmp/family_tree_Base4')
    family_tree_Base5.render(filename='/tmp/family_tree_Base5')
    family_tree_Base6.render(filename='/tmp/family_tree_Base6')
    family_tree_Base7.render(filename='/tmp/family_tree_Base7')
    family_tree_Base8.render(filename='/tmp/family_tree_Base8')
    family_tree_Base9.render(filename='/tmp/family_tree_Base9')




    with open(family_tree_path_Base1, 'rb') as f:
        family_tree_img_Base1 = f.read()

    family_tree_img_base64_Base1 = base64.b64encode(family_tree_img_Base1).decode('utf-8')

    with open(family_tree_path_Base2, 'rb') as f:
        family_tree_img_Base2 = f.read()

    family_tree_img_base64_Base2 = base64.b64encode(family_tree_img_Base2).decode('utf-8')

    with open(family_tree_path_Base3, 'rb') as f:
        family_tree_img_Base3 = f.read()

    family_tree_img_base64_Base3 = base64.b64encode(family_tree_img_Base3).decode('utf-8')

    with open(family_tree_path_Base4, 'rb') as f:
        family_tree_img_Base4 = f.read()

    family_tree_img_base64_Base4 = base64.b64encode(family_tree_img_Base4).decode('utf-8')

    with open(family_tree_path_Base5, 'rb') as f:
        family_tree_img_Base5 = f.read()

    family_tree_img_base64_Base5 = base64.b64encode(family_tree_img_Base5).decode('utf-8')

    with open(family_tree_path_Base6, 'rb') as f:
        family_tree_img_Base6 = f.read()

    family_tree_img_base64_Base6 = base64.b64encode(family_tree_img_Base6).decode('utf-8')

    with open(family_tree_path_Base7, 'rb') as f:
        family_tree_img_Base7 = f.read()

    family_tree_img_base64_Base7 = base64.b64encode(family_tree_img_Base7).decode('utf-8')

    with open(family_tree_path_Base8, 'rb') as f:
        family_tree_img_Base8 = f.read()

    family_tree_img_base64_Base8 = base64.b64encode(family_tree_img_Base8).decode('utf-8')
    with open(family_tree_path_Base9, 'rb') as f:
        family_tree_img_Base9 = f.read()

    family_tree_img_base64_Base9 = base64.b64encode(family_tree_img_Base9).decode('utf-8')
    

    return render_template('index.html', 
                           family_tree_img_base64_Base1=family_tree_img_base64_Base1,
                           family_tree_img_base64_Base2=family_tree_img_base64_Base2,
                           family_tree_img_base64_Base3=family_tree_img_base64_Base3,
                           family_tree_img_base64_Base4=family_tree_img_base64_Base4,
                           family_tree_img_base64_Base5=family_tree_img_base64_Base5,
                           family_tree_img_base64_Base6=family_tree_img_base64_Base6,
                           family_tree_img_base64_Base7=family_tree_img_base64_Base7,
                           family_tree_img_base64_Base8=family_tree_img_base64_Base8,
                           family_tree_img_base64_Base9=family_tree_img_base64_Base9)

if __name__ == '__main__':
    app.run(debug=True)
