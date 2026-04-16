import openpyxl
import paramiko
import os
"""
le fichier va tester tout les mdp et login que je connais 
il n a rien trouvé avec seulement XX sans login
et il va créer un fichier pour noter chaque type de switch différent
il connait les adresses ip avec integration_switch_zabbix_metropole.xlsx
"""



# Fonction pour tester les connexions SSH et enregistrer les résultats dans le fichier spécifié
def tester_connexion(adresses_ip, username, password, output_filename):
    adresses_reussies = []

    with open(output_filename, "a") as fichier:  # Mode ajout
        for ip in adresses_ip:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                client.connect(hostname=ip, username=username, password=password, timeout=10)
                
                adresses_reussies.append(ip)
                fichier.write(ip + '\n')
                
                client.close()
            except Exception as e:
                print(f"Erreur lors de la connexion à {ip}: {e}")

    return adresses_reussies

# Charger les adresses IP à partir du fichier Excel
def charger_adresses_ip(chemin_fichier):
    workbook = openpyxl.load_workbook(chemin_fichier)
    sheet = workbook.active

    adresses_a_tester = []
    for row in sheet.iter_rows(values_only=True):
        ip_address = row[0]
        adresses_a_tester.append(ip_address)
    
    return adresses_a_tester

# Supprimer les espaces des adresses IP
def supprimer_espaces(liste):
    return [element.strip() if element is not None else None for element in liste]

# Définir les cas de test et leurs paramètres spécifiques
cas_de_tests = [
    {"nom_fichier": "test_alcatel.xlsx", "username": 'A', "password": 'A'},
    {"nom_fichier": "test_dri.xlsx", "username": 'B', "password": 'B'},
    {"nom_fichier": "test_hp.xlsx", "username": None, "password": 'B'},
    {"nom_fichier": "test_!.xlsx", "username": 'B', "password": 'B'}
]

# Dossier de sortie
dossier_sortie = os.path.join(os.path.expanduser("~"), "Desktop", "switch")
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Charger les adresses IP à partir du fichier "integration_switch_zabbix_metropole.xlsx"
adresses_a_tester = charger_adresses_ip(os.path.join(dossier_sortie, "integration_switch_zabbix_metropole.xlsx"))

# Traitement pour chaque cas de test
for cas in cas_de_tests:
    # Créer le chemin complet pour le fichier de sortie
    nom_fichier_sortie = os.path.join(dossier_sortie, cas["nom_fichier"])
    
    # Tester les connexions SSH et enregistrer les résultats dans le fichier de sortie
    adresses_reussies = tester_connexion(adresses_a_tester, cas["username"], cas["password"], nom_fichier_sortie)
    print(f"Connexions réussies pour {cas['nom_fichier']} : {adresses_reussies}")
