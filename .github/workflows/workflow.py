import requests
import sys
from datetime import datetime

ignx = "rekrap2"  # JUST FOR WORKFLOW PURPOSES
result = [name.strip() for name in ignx.split(",")]

skin_results = []

for ign in result:
    modifiedign = ign.replace(" ", "%20")
    r = requests.get(f"https://api.geysermc.org/v2/xbox/xuid/{modifiedign}")
    if r.status_code != 200:
        sys.exit(f"\nIGN {ign} not found. Exiting...")
    else:
        xuid = r.json()["xuid"]
        r = requests.get(f"https://api.geysermc.org/v2/skin/{xuid}")
        try:
            skin_result = {
                "Player": ign,
                "XUID": xuid,
                "Hash": r.json()["hash"],
                "Is steve": "No" if r.json()["is_steve"] == "false" else "Yes",
                "Last modified": datetime.fromtimestamp(
                    int(r.json()["last_update"]) / 1000
                ),
                "Signature": r.json()["signature"],
                "Texture ID": r.json()["texture_id"],
                "Value": r.json()["value"],
                "Skin URL": f"https://textures.minecraft.net/texture/{r.json()['texture_id']}",
            }
        except KeyError:
            sys.exit(
                "API returned with a blank json. You might wanna check if the player exist. Exiting..."
            )
        print(f"\nPlayer {skin_result['Player']} found!\nXUID: {skin_result['XUID']}\n")
        print(
            f"Hash: {skin_result['Hash']}\nIs steve: {skin_result['Is steve']}\nLast modified: {skin_result['Last modified']}\nSignature: {skin_result['Signature']}\nTexture ID: {skin_result['Texture ID']}\nValue: {skin_result['Value']}\n"
        )
        skin_results.append(skin_result)

for skin_result in skin_results:
    print(f"Here is {skin_result['Player']}'s skin. Enjoy!\n{skin_result['Skin URL']}")
