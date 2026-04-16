@echo off
setlocal

REM Demander les informations de configuration du switch
set /p switch_name=Entrez le nom du switch : 
set /p vlan_idmngt=Entrez l'ID du VLAN de management:
set /p vlan_namemngt=Entrez le nom du VLAN %vlan_idngt% :
set /p ip_addressmngt=Entrez l'adresse IP du switch : 
set /p port_mngt=Entrez le port d'administration :
set /p ip_addressntp=Entrez l'adresse IP du serveur NTP :
set /p snmp_community=Entrez la communauté SNMP :
set /p vlan_iduser=Entrez l'ID du VLAN des users:
set /p vlan_nameuser=Entrez le nom du VLAN %vlan_iduser% :
set /p vlan_idtel=Entrez l'ID du VLAN de la telephonie IP:
set /p vlan_nametel=Entrez le nom du VLAN %vlan_idtel% :
set /p port_user=Programmez le vlan user du port 1 jusqu'au port :


REM Nom du fichier de configuration
set config_file=C:\Users\n.personnaz\Desktop\script_aruba_cx\%switch_name%.txt
REM Chemin d'acces à putty
set putty_path=C:\ProgramData\chocolatey\bin\putty.exe



rem taskkill /f /im putty.exe
REM Écriture de la configuration de base du switch dans le fichier
echo configure terminal >> %config_file%
REM Configuration du nom
echo hostname %switch_name% >> %config_file%
REM Configuration du serveur NTP
echo no ntp server pool.ntp.org >> %config_file%
echo clock timezone europe/paris >> %config_file%
echo ntp server %ip_addressntp% >> %config_file%
echo ntp enable >> %config_file% 
REM Configuration du SNMP
echo snmp-server community %snmp_community%  >> %config_file%
echo access-level rw  >> %config_file%
echo snmp-server vrf default >> %config_file%

REM Configuration de l'interface de management
echo vlan %vlan_idmngt%  >> %config_file%
echo name %vlan_namemngt%  >> %config_file%
echo interface vlan %vlan_idmngt% >> %config_file%
echo ip address %ip_addressmngt% 255.255.255.0 >> %config_file%
echo no shutdown >> %config_file%
echo exit >> %config_file%
REM Configuration du port de management
echo interface 1/1/%port_mngt% >> %config_file%
echo description MANAGEMENT >> %config_file%
echo no shutdown >> %config_file%
echo vlan access %vlan_idmngt% >> %config_file%
echo exit >> %config_file%

REM Configuration des interfaces utilisateurs
echo vlan %vlan_iduser%  >> %config_file%
echo name %vlan_nameuser%  >> %config_file%
echo no shutdown >> %config_file%
echo vlan %vlan_idmtel%  >> %config_file%
echo name %vlan_nametel%  >> %config_file%
echo no shutdown >> %config_file%
echo exit >> %config_file%
REM Configuration des ports users
for /L %%i in (1,1,%port_user%) do (
	echo interface 1/1/%%i >> %config_file%
	echo description USER >> %config_file%
	echo no shutdown >> %config_file%
	echo vlan trunk native %vlan_iduser% >> %config_file%
	echo vlan trunk allowed %vlan_iduser%,%vlan_idtel% >> %config_file%
	echo exit >> %config_file%
    )


:loop
REM Configuration des VLANS du switch
set /p vlan_id=Entrez l'ID du VLAN (ou appuyez sur Enter pour terminer) : 
if "%vlan_id%"=="" goto :endloop

set /p vlan_name=Entrez le nom du VLAN %vlan_id% : 

REM Configuration du VLAN dans le fichier
echo vlan %vlan_id% >> %config_file%
echo name %vlan_name% >> %config_file%
echo exit >> %config_file%
set "vlan_id="

REM Aller à nouveau dans la boucle
goto :loop

:endloop
REM Ajouter les commandes de sortie et d'enregistrement de la configuration dans le fichier
echo write memory >> %config_file%
echo end >> %config_file%

echo Le fichier de configuration a été généré avec succès.

REM Ajoute une pause à la fin du script

type "C:\Users\n.personnaz\Desktop\script_aruba_cx\%switch_name%.txt" | clip

%putty_path% -serial COM3 -sercfg 115200,8,n,1,N -sessionlog %config_file% < %switch_name%.txt


REM Suppression du fichier temporaire


endlocal