import ovh
import os
import requests
import time
from datetime import datetime, timedelta

#si il faut regénérer un token : 
#GET /me/bill

#GET /me/bill/*
client = ovh.Client(
    endpoint='ovh-eu',
    application_key='',
    application_secret='',
    consumer_key=''
)


# Dossier de sauvegarde
output_dir = "factures_ovh"
os.makedirs(output_dir, exist_ok=True)

# Calcul de la date limite (aujourd'hui - 3 ans, soit 3 * 365 jours)
date_limite = datetime.now() - timedelta(days=3*365)
print(f"📅 Filtre activé : téléchargement des factures émises après le {date_limite.strftime('%d/%m/%Y')}")

print("Récupération de la liste des factures...")
try:
    bills = client.get('/me/bill')
    # On inverse la liste pour commencer par les plus récentes (souvent plus pertinent)
    bills.reverse() 
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit(1)

print(f"✅ {len(bills)} factures trouvées au total. Analyse des dates...")

count_downloaded = 0
count_skipped = 0

for i, bill_id in enumerate(bills):
    target_path = os.path.join(output_dir, f"{bill_id}.pdf")
    
    # Affichage de progression
    print(f"[{i+1}/{len(bills)}] {bill_id} :", end=" ", flush=True)

    if os.path.exists(target_path):
        print("➡️ Déjà là.")
        continue

    try:
        # 1. On récupère les détails
        details = client.get(f'/me/bill/{bill_id}')
        
        # 2. VERIFICATION DE LA DATE
        bill_date_str = details.get('date') # Format ex: "2023-01-26T11:29:44+01:00"
        
        if bill_date_str:
            # On prend juste les 10 premiers caractères (YYYY-MM-DD) pour simplifier
            bill_date_obj = datetime.strptime(bill_date_str[:10], "%Y-%m-%d")
            
            if bill_date_obj < date_limite:
                print(f"🚫 Trop vieux ({bill_date_str[:10]})")
                count_skipped += 1
                # Astuce : Comme on a inversé la liste (plus récent au plus vieux),
                # si on tombe sur une facture trop vieille, toutes les suivantes le seront aussi.
                # On peut donc arrêter le script ici pour gagner du temps !
                # Si tu préfères tout vérifier quand même, commente la ligne 'break' ci-dessous.
                # break 
                continue
        
        # 3. On prend le lien PDF
        pdf_url = details.get('pdfUrl')

        if not pdf_url:
            print("❌ Pas de lien PDF.")
            continue

        # 4. On télécharge
        r = requests.get(pdf_url)
        
        if r.status_code == 200:
            with open(target_path, "wb") as f:
                f.write(r.content)
            print(f"✅ Téléchargé ({bill_date_str[:10]})")
            count_downloaded += 1
        else:
            print(f"❌ Erreur HTTP {r.status_code}")

        time.sleep(0.2)

    except Exception as e:
        print(f"\n❌ Erreur : {e}")

print(f"\n--- Terminé ! {count_downloaded} fichiers téléchargés, {count_skipped} ignorés. ---")
