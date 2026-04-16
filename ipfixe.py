import paramiko
import openpyxl
import time  # Ajout de l'importation du module time
"""
ce fichier va ecrire des commandes sur les quelques switchs qui lui sont passé en paramétre 
"""
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




exel = ['172.30.90.145' ,  '172.30.91.67' , '172.30.90.158']

# Exécution des commandes sur chaque commutateur
for i in range(len(exel)):
    host = exel[i]  # Supposons que la colonne contenant les adresses IP est la première colonne
    commands = [
       
        'tftp X.X.X.X get MASTER/master_hp_5140_48p-stack.cfg startup.cfg'
    ]
    result = execute_commands(host, username, password, commands)
    print(f"Result for {host}: {result}")