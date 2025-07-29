from neo4j import GraphDatabase
import os

# Connexion à la base de données Neo4j
uri = "bolt://localhost:7687"
username = "ton_username_à_toi"
password = os.getenv("NEO4J_PASSWORD", "ton_password_à_toi")  # Utilisation d'une variable d'environnement pour le mot de passe

driver = GraphDatabase.driver(uri, auth=(username, password))

def creer_individu(tx, nom_complet):
    """Crée un individu (nœud) dans Neo4j s'il n'existe pas déjà."""
    query = """
    MERGE (p:Person {nom_complet: $nom_complet})
    """
    tx.run(query, nom_complet=nom_complet)

def creer_relation(tx, parent_nom_complet, enfant_nom_complet):
    """Crée une relation parent-enfant entre deux nœuds en évitant les doublons."""
    query = """
    MATCH (p:Person {nom_complet: $parent_nom_complet}), (e:Person {nom_complet: $enfant_nom_complet})
    MERGE (p)-[:PARENT_DE]->(e)
    """
    tx.run(query, parent_nom_complet=parent_nom_complet, enfant_nom_complet=enfant_nom_complet)

def ajouter_individu_et_relations(tx, parent_nom_complet, enfants):
    """Ajoute un individu et crée des relations parent-enfant."""
    creer_individu(tx, parent_nom_complet)  # Crée le parent s'il n'existe pas
    
    for enfant_nom_complet in enfants:
        creer_individu(tx, enfant_nom_complet)  # Crée l'enfant s'il n'existe pas
        creer_relation(tx, parent_nom_complet, enfant_nom_complet)  # Crée la relation

def ajouter_tous_les_individus():
    """Ajoute tous les individus et leurs relations à la base de données."""
    with driver.session() as session:
        # Liste des individus et de leurs relations
        relations =  [
            ("Asta Madièye Diop", ["Baba Ndiaré Ndiaye"]),
            ("Baba Ndiaré Ndiaye", ["Marie Baba Ndiaré Ndiaye", "Awa Baba Ndiaré Ndiaye", "Madiop Baba Ndiaré Ndiaye"]),
            ("Marie Baba Ndiaré Ndiaye", ["Anta Sarr Ndiawar"]),
            ("Anta Sarr Ndiawar", ["Oulimata Diouf"]),
            ("Oulimata Diouf", ["Mar Seck", "Massène Diallo", "Alpha Ndiaye", "Iba Diagne", "Isse Tew Diagne", "Diarra Ouli"]),
            ("Awa Baba Ndiaré Ndiaye", ["Penda Camara", "Djibril Camara"]),
            ("Penda Camara", ["Ainina Diop", "Binta Yama Diop", "Magatte Diop Ibnou", "Babacar Diop", "Yaye Awa Diop", "Abdoulaye Kébé", "Souleymane kébé", "Amy Kébé"]),
            ("Ibnou Diop Wara", ["Ainina Diop", "Binta Yama Diop", "Magatte Diop Ibnou", "Yaye Awa Diop", "Babacar Diop"]),
            ("Amadou Lamine Kébé", ["Abdoulaye Kébé", "Souleymane kébé", "Amy Kébé"]),
            ("Djibril Camara", ["Malick Camara", "Latyr Camara", "Ibou Camara", "Mame Aida Camara"]),
            ("Marguerite Boye", ["Malick Camara", "Latyr Camara", "Ibou Camara", "Mame Aida Camara"]),
            ("Malick Camara", ["Margot", "Cheikh Demba Camara"]),
            ("Adja Fat Ly", ["Margot", "Cheikh Demba Camara"]),
            ("Mame Aida Camara", ["Binta Guèye"]),
            ("Madiop Baba Ndiaré Ndiaye", ["Boly Ndiaye"]),
            ("Boly Ndiaye", ["Awa Boly Ndiaye"]),
            ("Awa Boly Ndiaye", ["Rokhaya Ndiaye Awa Boly"]),
            ("Rokhaya Ndiaye Awa Boly", ["Serigne Babacar Sy"]),
            ("Latyr Camara", ["Mame Marième Camara", "Margot Camara", "Yacine Camara"]),
            ("Seune Ndiaye", ["Tame"]),
            ("Tame", ["Birame Khoudia Tame Ndiaye"]),
            ("Souleymane Ndiaye", ["Marième Ndiaye", "Astou Ndiaye", "Moustapha Ndiaye", "Oulimata Ndiaye", "Ismaila Ndiaye", "Ndeye Rosalie Ndiaye", "Madiagne Ndiaye", "Ibrahima Ndiaye", "Fatou Ndiaye", "Bassirou Ndiaye", "Seynabou Ndiaye", "Seune Ndiaye (Souleymane)"]),
            ("Sakoki Ndiaye", ["Souleymane Ndiaye"]),
            ("Birame Rouba Ndiaye", ["Sakoki Ndiaye", "Mamour Ndiaye"]),
            ("Yirim Mbagnick Ndiaye", ["Birame Rouba Ndiaye"]),
            ("Mandiaye Khedj", ["Yirim Mbagnick Ndiaye"]),
            ("Birame Rouba Mamour Ndiaye", ["Mandiaye Khedj"]),
            ("Mamour  Ndiaye", ["Birame Rouba Mamour Ndiaye"]),
            ("Mandiaye Birame", ["Mamour  Ndiaye"]),
            ("Birame Samba Ndiaye", ["Mandiaye Birame"]),
            ("Birame Khoudia Tame Ndiaye", ["Sokhna Ndiaye"]),
            ("Sokhna Ndiaye", ["Arame Bonko"]),
            ("Arame Bonko", ["Safiétou Niang"]),
            ("Safiétou Niang", ["Serigne Abdou Aziz Sy", "Serigne Mansour Sy", "Abib Sy", "Sokhna Oumou Khalry Malick", "Sokhna Rokhaya Malick", "Sokhna Nafissatou Malick"]),
            ("Kombarou Ndaw", ["Ngouye Ndiaye", "Fama Sy", "Seune Ndiaye"]),
            ("Fama Sy", ["Birame Rouba Ndiaye", "Aymérou Fama Ndiaye"]),
            ("Ngouye Ndiaye", ["Fatimata Ngouye"]),
            ("Fatimata Ngouye", ["Seynabou"]),
            ("Amadou Yélé", ["Seynabou", "Sakhéwar"]),
            ("Sakhéwar", ["Lat-Dior"]),
            ("William Diouf", ["Oulimata Diouf", "Rosalie Diouf"]),
            ("Rosalie Diouf", ["Souleymane Ndiaye", "Amadou Moustapha Diagne", "Moctar Diagne", "Baba Diagne", "Fatou Diagne", "Astou Diagne", "Amadou Abdoulaye Diagne"]),
            ("Djiby Diagne", ["Amadou Moustapha Diagne", "Moctar Diagne", "Baba Diagne", "Fatou Diagne", "Astou Diagne", "Amadou Abdoulaye Diagne"]),
            ("Edmond Diouf", ["Mame Guitté Diouf"]),
            ("Mame Guitté Diouf", ["Astou Fall", "Mame Pourmera Fall", "Ousseynou Fall", "Assane Fall", "Ablaye Fall", "Cheikh Fall"]),
            ("Astou Fall", ["Ndeye Tabara Diop", "Ndeye Binta Diop", "Pape Diop"]),
            ("Mame Pourmera Fall", ["Lamine Tew", "Soppé Diop", "Mame S. Diop"]),
            ("Binta Sarr", ["Fatou Diallo"]),
            ("Fatou Diallo", ["Marième Ndiaye", "Aissatou Ndiaye", "Amadou Moustapha Ndiaye", "Oulimata Ndiaye", "Rosalie Ndiaye", "Madiagne Ndiaye", "Babacar Dieng", "Baaye Dieng", "Madicke Dieng"]),
            ("Pape Thiaka Dieng", ["Babacar Dieng", "Baaye Dieng", "Madicke Dieng"]),
            ("Ndiogou Seck", ["Yatma Seck"]),
            ("Yatma Seck", ["Mar Seck", "Malick Seck", "Pathé Ndegg Seck", "Ouleymatou Seck", "Fary Seck"]),
            ("Marième Ndiaye", ["Binta Yama Seck", "Nafissatou Seck", "Aminta Seck", "Mouhamadou Moustapha Seck", "Pathé Seck", "Penda Ndiaye Seck", "Mame Aida Seck"]),
            ("Maguette Fall Dagana", ["Warxa Seck"]),
            ("Courra Dièye Sarr", ["Maguette Seck"]),
            ("Nafissatou Diop Attoumane", ["Marième Seck (Nafissatou Diop)", "Fatou Seck (Nafissatou Diop)", "Moustapha Seck", "Boubacar Seck", "Aissatou Seck"]),
            ("Mar Seck", ["Binta Yama Seck", "Nafissatou Seck", "Aminta Seck", "Mouhamadou Moustapha Seck", "Pathé Seck", "Penda Ndiaye Seck", "Mame Aida Seck", "Marième Seck (Nafissatou Diop)", "Fatou Seck (Nafissatou Diop)", "Moustapha Seck", "Boubacar Seck", "Aissatou Seck", "Magatte Seck", "Warxa Seck"]),
            ("Binta Yama Seck", ["Ndeye Wouly Diagne", "Pape Mar Diagne", "Idrissa Diagne", "Tidjane Diagne", "Madjiguène Diagne", "Makhtar Diagne", "Moussa Diagne", "Diarra Diagne", "Yatma Diagne", "Nafissatou Diagne", "Mame Aida Diagne"]),
            ("Nafissatou Seck", ["Magatte Diop", "Mame Aissatou Diedhiou", "Magatte Fall Diedhiou", "Fatou Néné Diedhiou", "Alphousseynou Diedhiou", "Assane Diedhiou", "Ismaila Diedhiou", "Mouhameth Diedhiou"]),
            ("Aminta Seck", ["Binta Sarr Thoub", "Abdou Yacine Cissé", "Safiétou Cissé", "Ndèye Marième Cissé"]),
            ("Fatou Nar Diagne", ["Pape Mar Seck", "Ndèye Tacko Seck", "Lalla Seck", "Famara Seck", "Ndeye Birame Seck", "Cheikh Seck", "El Djiby Seck", "Mame Khady"]),
            ("Mouhamadou Moustapha Seck", ["Marième Seck (Fatou Pouye)", "Ndoumbé Seck", "Pathé Seck", "Fatou Seck (Fatou Pouye)", "Ndeye Ami Seck", "Boubacar Seck", "Bassirou Seck", "Pape Mar Seck", "Ndèye Tacko Seck", "Lalla Seck", "Famara Seck", "Ndeye Birame Seck", "Cheikh Seck", "El Djiby Seck", "Mame Khady"]),
            ("Diarra Diagne", ["Ibrahima Gabar Diop","Fatou Cissé Diop","Assane Gabar Diop"]),
            ("Fatou Pouye", ["Marième Seck (Fatou Pouye)", "Ndoumbé Seck", "Pathé Seck", "Fatou Seck (Fatou Pouye)", "Ndeye Ami Seck", "Boubacar Seck", "Bassirou Seck"]),
            ("Pathé Seck", ["Makha Seck", "Penda Ndiaye Seck", "Sokhna Oumou Kalsoume Seck", "Pauline Seck", "Aby Seck", "Marième Aicha Seck", "Marième Nora Seck"]),
            ("Yacine Diop", ["Makha Seck", "Penda Ndiaye Seck"]),
            ("Ndèye Coumba Seck", ["Sokhna Oumou Kalsoume Seck", "Pauline Seck", "Aby Seck", "Marième Aicha Seck"]),
            ("Laurence Ba", ["Marième Nora Seck"]),
            ("Fa Gaye", ["Mota Sarr", "Anna Sarr", "Massar Fa Gaye", "Balla Sarr", "Demba Lo Sarr", "Mandaw Sarr", "Sokhna Fall", "Médoune Sène", "Awa Dièye"]),
            ("Sokhna Fall", ["Fatou Fall"]),
            ("Fatou Fall", ["Yatma Dièye"]),
            ("Yatma Dièye", ["Sokhna Mbacké Dièye", "Moustapha Dièye", "Colé Yate Dièye", "Nafi Dièye", "Aida Bayo", "Rama Dièye", "Idrissa Dièye", "Doudou Diop Dièye"]),
            ("Sokhna Bayo Sarr", ["Sokhna Mbacké Dièye", "Moustapha Dièye", "Colé Yate Dièye", "Nafi Dièye", "Aida Bayo", "Rama Dièye", "Idrissa Dièye", "Doudou Diop Dièye"]),
            ("Massar Fa Gaye", ["Penda Ndiaye Sarr"]),
            ("Gandj Dièye", ["Awa Dièye"]),
            ("Awa Dièye", ["Yacine Dièye Sall", "Daly Sall"]),
            ("Mota Sarr", ["Yatma Seck"]),
            ("Nar Gaye", ["Dame Awa Fall", "Moussa Fall", "Alioune Fall"]),
            ("Mbous Mademba", ["Masseck Fanta", "Cheikh Malamine Seck", "Fatoumata Seck", "Mame Arama Ngandji Seck", "Astou Seck"]),
            ("Maguette Seck",["Fatou Diouf"]),
            ("Marième Seck (Nafissatou Diop)",["Bitty Ndaw"]),
            ("Fatou Seck (Nafissatou Diop)",["Fama Seck","Baye Diawara", "Moustapha Diawara", "Amineta Diawara", "Ndèye Fatou Diawara", "Serigne Malick Diawara"]),
            ("Boubacar Seck", ["Pape Mar Seck (Boubacar)", "Rose Seck", "Aida Seck", "Mbaye Seck", "Abou Khassim Seck", "Outala Seck", "Mame Ibou Seck", "Cheikh Seck", "Ndèye Awa Seck"]),
            ("Aissatou Seck",["Oulymata Diallo", "Pape Gana Diallo", "Ndèye Nafi Diallo", "Marème Seck Diallo", "Ndèye Sophie Diallo", "Hamth Diallo", "Meissa Diallo"]),
            ("Iba Diagne",["Mamadou Diagne"]),
            ("Mamadou Diagne",["Ndeye Wouly Diagne", "Pape Mar Diagne", "Moussa Diagne", "Diarra Diagne", "Yatma Diagne", "Nafissatou Diagne", "Mame Aida Diagne"]),
            ("Makhtar Diagne",["Pape Mar Diagne", "Idrissa Diagne",  "Mouhamadou Tidjane Diagne", "Madjiguène Diagne"]),
            ("Mame Ass Seck", ["Bayma Seck", "Cheikh Makhfouss Seck (Mame Ass)", "Thiané Seck", "Ndèye Aida Seck", "Nafi Seck", "Ndèye Wouly Seck", "Mouhamed Seck", "Ndiawar Seck", "Bouna Seck", "Pape Mamadou Seck"]),
            ("Oulimata Ndiaye", ["Ndèye Ouly Ndiaye", "Pape Ndiawar Ndiaye", "Seynabou Wade", "Cheikh Makhfouss Seck(Oulimata)", "Mame Ass Seck", "Adjara Seck"]),
            ("Ndèye Rosalie Ndiaye", ["Ndoumbé Sarr", "Pape Moustaphe Ndiaye", "Adjara Ndiaye", "Pape Iba Ndiaye", "Babacar Ndiaye"]),
            ("Moustapha Ndiaye", ["Mame Binta Ndiaye", "Baye Soulèye Ndiaye", "Lamine Bousso Ndiaye", "Fatou Mbegué Ndiaye"]),
            ("Astou Ndiaye", ["Moustapha Diagne", "Bouna Ndiaye", "Assy Dièye", "Ndèye Fatou Dièye", "Pape Makhtar Dièye", "Aida Dièye"]),
            ("Kader Diagne",["Moustapha Diagne"]),
            ("Amadou Ndiaye",["Bouna Ndiaye"]),
            ("Magatte Diop",["Ibrahima Gabar Diop","Fatou Cissé Diop", "Assane Gabar Diop", "Amadou Bamba Diop", "Lamine Gabar Diop"])
        ]
        # Ajout des individus et de leurs relations
        for parent, enfants in relations:
            session.write_transaction(ajouter_individu_et_relations, parent, enfants)

def main():
    """Fonction principale pour exécuter toutes les opérations."""
    try:
        ajouter_tous_les_individus()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        driver.close()

# Exécuter la fonction principale
if __name__ == "__main__":
    main()
