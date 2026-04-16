import ovh

# 1. Instancier le client avec tes NOUVELLES clés (à générer !)
client = ovh.Client(
    endpoint='ovh-eu',
    application_key='TON_NOUVEL_APP_KEY',
    application_secret='TON_NOUVEL_APP_SECRET',
    consumer_key='TON_NOUVEAU_CONSUMER_KEY',
)

# Liste de tes domaines à nettoyer
zones = [
    'X',
    'X',
    'X',
    'X',
    'X',
    'X'
]

print(" Démarrage du grand ménage DNS (Mode Avancé)...")

for zone in zones:
    print(f"\n--- Traitement de la zone : {zone} ---")
    
    try:
        # 2. On récupère TOUS les IDs des champs TXT de la zone (sans filtrer tout de suite)
        all_txt_ids = client.get(f'/domain/zone/{zone}/record', fieldType='TXT')
        
        ids_to_delete = []
        
        # 3. On regarde le détail de chaque champ TXT pour voir son vrai nom
        for record_id in all_txt_ids:
            record_details = client.get(f'/domain/zone/{zone}/record/{record_id}')
            subdomain = record_details.get('subDomain', '')
            
            # Si le sous-domaine existe ET qu'il contient "_acme-challenge"
            if subdomain and '_acme-challenge' in subdomain:
                ids_to_delete.append((record_id, subdomain))
                
        # 4. On supprime ceux qu'on a repérés
        if not ids_to_delete:
            print(f" Aucun _acme-challenge trouvé sur {zone}. C'est tout propre !")
        else:
            print(f" {len(ids_to_delete)} enregistrements trouvés. Suppression en cours...")
            
            for record_id, subdomain in ids_to_delete:
                client.delete(f'/domain/zone/{zone}/record/{record_id}')
                print(f"   -> Supprimé : {subdomain} (ID: {record_id})")
            
            # Appliquer les changements
            client.post(f'/domain/zone/{zone}/refresh')
            print(f" Mise à jour de la zone {zone} terminée avec succès.")
            
    except ovh.exceptions.APIError as e:
        print(f" Erreur avec le domaine {zone} : {e}")

print("\n Terminé ! La boucle est bouclée.")
