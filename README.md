# 🛠️ Toolbox d'Automatisation & DevOps - Full Edition

Ce dépôt est une collection complète de scripts (Python, PowerShell, Bash, Batch) conçus pour l'administration système, la gestion réseau et l'automatisation de tâches IT.

## 📋 Sommaire des Scripts

### 🌐 Gestion OVH, DNS & Cloud
* **`acme.py`** : Nettoyage automatisé des zones DNS OVH (suppression des records `_acme-challenge`).
* **`facture.py`** : Récupération et archivage local des factures PDF OVH des 3 dernières années via API.
* **`listage-azure.ps1`** : Export CSV de l'annuaire des utilisateurs Azure AD/Entra ID.

### 🛡️ Administration AD & Sécurité Windows
* **`inactif.ps1`** : Audit d'hygiène AD (Utilisateurs/PC inactifs depuis 6 mois et comptes M365 non utilisés).
* **`save.txt`** : (Script PowerShell/Bash) Configuration de GPO pour Windows Update et scripts de nettoyage `apt` pour Linux.
* **`connexionauto`** : Configuration d'un compte utilisateur Windows avec autologon et désactivation de la mise en veille (idéal pour bornes/écrans de monitoring).
* **`panel.ps1`** : Optimisation des registres Windows 11 pour l'utilisation de tablettes tactiles en bureau distant (clavier visuel, mode tablette).

### 🖧 Gestion Réseau & Switches (Aruba, HP, Alcatel)
* **`version finale.py`** : Script SSH massif permettant d'envoyer des commandes de configuration à une liste de switches définie dans un Excel.
* **`testevraimenttout.py`** : Scanner de vulnérabilité/connexion qui teste plusieurs combinaisons de logins/mots de passe sur un parc de switches et trie les résultats par marque dans des fichiers Excel distincts.
* **`testetout.py`** : Vérificateur de connectivité SSH simple qui note les IPs accessibles dans un fichier Excel de suivi.
* **`ipfixe.py`** : Automatisation de l'injection de configuration via SSH/TFTP sur des switches HP/Aruba.
* **`switcharuba.bat`** : Générateur interactif de fichiers de configuration pour switches Aruba CX (VLANs, management, NTP, SNMP, ports users).

### 🗄️ Sauvegarde & Bases de Données (MSPR)
* **`mspr3bdd_nightly.sh`** : Script de sauvegarde MySQL hautement sécurisé (umask 0077) avec journalisation, vérification d'intégrité et rotation sur NAS.
* **`backup_mspr3bdd_frequent.sh`** : Sauvegarde MySQL à haute fréquence avec rotation des 12 derniers fichiers SQL.

### 🤖 Web & Communication (Automation)
* **`slack.py`** : Synchronisation entre Slack et Bitwarden (Password Manager). Le script crée des groupes dans Bitwarden basés sur les canaux Slack et synchronise les membres automatiquement.
* **`login.py`** : Automatisation de navigateur (Selenium/Edge) pour se connecter automatiquement à une mire de surveillance web spécifique.

### 📄 Manipulation de Documents
* **`markdown.py`** : Convertisseur de documentation Markdown (Wiki) vers le format PDF pour la génération de livrables contractuels.
* **`enregistreimagepdf.py`** : Extraction automatisée des images contenues dans un PDF.
* **`enregistreimageword.py`** : Extraction des images intégrées dans des fichiers `.docx`.
* **`imprimante.ps1`** : Inventaire des imprimantes locales et réseau vers CSV.

