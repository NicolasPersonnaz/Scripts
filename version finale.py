import paramiko
import openpyxl
import time  # Ajout de l'importation du module time
"""
se fichier va pouvoir envoyer des commandes a une marque de switch en meme temps le 
fichier qu il utilise pour savoir quelles sont les adresses ip est : test qui est sur mon bureau
"""
def supprimer_espaces(liste):
    """
    Supprime les espaces avant et après chaque élément d'une liste.

    Args:
        liste (list): La liste à traiter.

    Returns:
        list: La liste modifiée sans les espaces avant et après chaque élément.
        
    supprime aussi les cases vide 
    """
    # Utiliser une compréhension de liste avec une condition pour ignorer les éléments vides
    liste_sans_espaces = [element.strip() if element is not None else None for element in liste]
    
    # Filtrer les éléments non-None de la liste
    return [element for element in liste_sans_espaces if element is not None]

# Exemple d'utilisation :


def execute_commands(host, username, password, commands):
    try:
        # Initialiser une session SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connexion au commutateur
        client.connect(hostname=host, username=username, password=password, timeout=10)

        # Ouverture d'un canal SSH
        channel = client.invoke_shell()

        # Attendre que le terminal soit prêt
        time.sleep(1)
        output = channel.recv(65535)

        # Exécution des commandes
        for command in commands:
            channel.send(command + '\n')
            time.sleep(1)  # Attendre la réponse
            output += channel.recv(65535)

        # Fermeture de la connexion
        channel.close()
        client.close()

        # Retourner la sortie des commandes
        return output.decode('utf-8')

    except paramiko.AuthenticationException:
        return "Authentication failed, please verify your credentials."
    except paramiko.SSHException as ssh_err:
        return f"SSH connection error: {ssh_err}"
    except Exception as e:
        return f"Error: {e}"

# Paramètres de connexion
username = 'username'
password = 'password'

# Charger les adresses IP à partir du fichier Excel
workbook = openpyxl.load_workbook(r'C:\Users\PERSONNAZN\Desktop\test.xlsx')
sheet = workbook['Feuil1']  # Assurez-vous de changer le nom de la feuille si nécessaire

# Initialiser une liste pour stocker les adresses IP
excel_ips = []

# Lire les adresses IP à partir de la première colonne (colonne A)
for row in sheet.iter_rows(values_only=True):
    ip_address = row[0]  # Supposons que les adresses IP sont dans la première colonne
    excel_ips.append(ip_address)

#efface les espaces devant et derriere et les cases vides 
excel_ips = supprimer_espaces(excel_ips)

# Exécution des commandes sur chaque commutateur
for i in range(len(excel_ips)):
    
    host = excel_ips[i] # Supposons que la colonne contenant les adresses IP est la première colonne
    commands = [
       
        'tftp X.X.X.X get MASTER/master_hp_5140_48p-stack.cfg startup.cfg'
    ]
    result = execute_commands(host, username, password, commands)
    print(f"Result for {host}: {result}")
