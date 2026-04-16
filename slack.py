#!/usr/bin/env python3
import requests
import time
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

BASE_URL = os.getenv("VW_BASE_URL")
ORG_ID = os.getenv("VW_ORG_ID")
CLIENT_ID = os.getenv("VW_CLIENT_ID")
CLIENT_SECRET = os.getenv("VW_CLIENT_SECRET")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

SLACK_PREFIX = "client_"
VW_PREFIX = "Client-"

def get_token():
    url = f"{BASE_URL}/identity/connect/token"
    data = {"grant_type": "client_credentials", "scope": "api", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "device_identifier": "vps-sync", "device_name": "VPS-Debian", "device_type": "3"}
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def get_slack_channels():
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    url = "https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=1000"
    r = requests.get(url, headers=headers).json()
    return {c["name"][len(SLACK_PREFIX):].capitalize(): c["id"] for c in r.get("channels", []) if c["name"].startswith(SLACK_PREFIX)}

def sync():
    print(f"--- 🤖 SYNC START: {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        vw_users = {u["email"]: u["id"] for u in requests.get(f"{BASE_URL}/api/organizations/{ORG_ID}/users", headers=headers).json()["data"]}
        vw_groups = {g["name"]: g for g in requests.get(f"{BASE_URL}/api/organizations/{ORG_ID}/groups", headers=headers).json()["data"]}
        slack_channels = get_slack_channels()

        for client_name, slack_id in slack_channels.items():
            vw_name = f"{VW_PREFIX}{client_name}"
            
            # Création auto
            if vw_name not in vw_groups:
                print(f"🔨 Création groupe: {vw_name}")
                payload = {"name": vw_name, "accessAll": False, "collections": [], "users": []}
                r = requests.post(f"{BASE_URL}/api/organizations/{ORG_ID}/groups", headers=headers, json=payload)
                if r.status_code in [200, 201]:
                    vw_groups[vw_name] = r.json()
                else: 
                    continue

            # Synchro membres
            group_id = vw_groups[vw_name]["id"]
            headers_slack = {"Authorization": f"Bearer {SLACK_TOKEN}"}
            m_ids = requests.get(f"https://slack.com/api/conversations.members?channel={slack_id}", headers=headers_slack).json().get("members", [])
            
            target_ids = []
            for m_id in m_ids:
                u = requests.get(f"https://slack.com/api/users.info?user={m_id}", headers=headers_slack).json()
                if u.get("ok") and not u["user"]["is_bot"]:
                    email = u["user"]["profile"].get("email")
                    if email in vw_users: 
                        target_ids.append(vw_users[email])

            # Update final
            g_details = requests.get(f"{BASE_URL}/api/organizations/{ORG_ID}/groups/{group_id}", headers=headers).json()
            payload = {"name": vw_name, "accessAll": False, "collections": g_details.get("collections", []), "users": target_ids}
            requests.put(f"{BASE_URL}/api/organizations/{ORG_ID}/groups/{group_id}", headers=headers, json=payload)
            print(f"✅ {vw_name} synchronisé.")
            
    except Exception as e:
        print(f"💥 Erreur critique: {e}")

if __name__ == "__main__":
    sync()
