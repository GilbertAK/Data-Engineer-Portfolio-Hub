import datetime
import os

# Génère un horodatage précis pour forcer une modification du fichier
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Chemin du fichier à modifier
file_path = "heartbeat.txt"

# Ecriture dans le fichier pour simuler une mise à jour de maintenance
with open(file_path, "w", encoding="utf-8") as f:
    f.write(f"Dernière maintenance système : {current_time}\nStatut : Opérationnel")

print(f"Succès : heartbeat.txt mis à jour à {current_time}")

