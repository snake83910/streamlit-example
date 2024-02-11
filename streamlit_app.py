from flask import Flask, request, jsonify
import requests
import urllib3
import re
import webbrowser

app = Flask(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/api/plate-info', methods=['POST'])
def plate_info():
    data = request.get_json()
    platenumber = data.get('platenumber')
    country = data.get('country', 'FR')

    url = "https://www.123pneus.fr/ws/driveright/vehicle"
    headers = {
    "Host": "www.123pneus.fr",
    "Connection": "keep-alive",
    "Content-Length": "40",
    "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    "X-CSRF-TOKEN": "bd3dbec0-119b-4245-985a-e7c98ecdf821",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-platform": '"Windows"',
    "Origin": "https://www.123pneus.fr",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.123pneus.fr/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": "LSID=625741b0-2f52-4a20-bb24-9d755bccba29; ab__511258664_1698668846=VARIATION; SESSION=b65cf047-8dac-4a75-aa6d-65a4b36d2c4b; __cmpconsent25422=BP5y-YtP5y-YtAfMVBFRABAAAAA4uAkgAUABYAFQALgAZAA4ACAAE4AKoAWABcADIAGgARgAmABSAC2AGEAOcAgACBgEGAQkAiACJAEcAJQAUgArQBhgDLAHkAP0AgYBCADAgH6AR7AmwCbQGtAOLA; __cmpcccu25422=aBP5y-YtgBwAzADQAGwAOAOgAAgAEAAPAAoACwAHAATAAuABoAD0AKAApABoAD4AIIAQwAmgBeAD2AIcATIAxABogELAIkAUSAp4CoAFcALMAj0BRoC4wF-gMNAbsA4IBxIDkgHngPRAeqBBwCFgESQImARQAqcBWoCwMFsgWzA7gCPgE3wKHQUaApHBUACpQFSwKowCC6tl1dOtOdk87NyAP0K-KmcA; _gid=GA1.2.1248526877.1707579141; _fbp=fb.1.1707579140879.545827150; lantern=8604ade2-2e35-43d9-a233-599d963747fc; sat_track=true; _gat_UA-190589453-10=1; _ga=GA1.2.1227620391.1707579141; cto_bundle=Ue7aS190ZUxibHNnbnlpSHclMkJubTl1eHZBRXBNJTJGdVIxOEE0QkxaeiUyQm4lMkZIb0o0ciUyRmdlZ0NMeFE4UE4zUHRseUhMMGhESDlERXFkQ2FHbkx2elVJVVVlZGdHdW8zalg0Q3klMkI0bWtQQzdYcHJpTDBaWSUyRmVhTFBJSTlQQUpWbFdxNVpBZFlUdHM5S0slMkZXVzg4V2V0YWVhMXV4MGVnJTNEJTNE; _ga_XSF3N6ZQ2V=GS1.1.1707579140.1.1.1707579210.0.0.0; _ga_WPYRC83S1X=GS1.1.1707579140.1.1.1707579210.0.0.0"
}
    data = {"platenumber": platenumber, "country": country}

    response = requests.post(url, json=data, headers=headers, verify=False)

    if response.status_code == 200:
        car_id = response.json()["carID"]

        url_second_request = f"https://www.123pneus.fr/delticom/brand/proxy/?rsmKBA={car_id}"
        response_second_request = requests.get(url_second_request, verify=False)

        if response_second_request.status_code == 200:
            response_data = response_second_request.json()
            dimensions = []

            for item in response_data:
                if 'd' in item:
                    tire_dimension = item['d']
                    match = re.match(r'(\d+)/(\d+) R(\d+) (\d+)([A-Z])', tire_dimension)
                    
                    if match:
                        largeur = match.group(1)
                        hauteur = match.group(2)
                        diametre = match.group(3)
                        indice_charge = match.group(4)
                        symbole_vitesse = match.group(5)
                        
                        dimensions.append({
                            'largeur': largeur,
                            'hauteur': hauteur,
                            'diamètre': diametre,
                            'indice_charge': indice_charge,
                            'symbole_vitesse': symbole_vitesse
                        })
                    else:
                        return jsonify({"error": "La chaîne de données 'd' ne contient pas suffisamment d'informations."})
                else:
                    return jsonify({"error": "La clé 'd' est manquante dans l'élément."})

            if dimensions:
                url_pneus = f"https://tousvospneus.com/shop/?filter_largeur={dimensions[0]['largeur']}&filter_hauteur={dimensions[0]['hauteur']}&filter_diametre={dimensions[0]['diamètre']}&filter_charge={dimensions[0]['indice_charge']}&filter_vitesse={dimensions[0]['symbole_vitesse']}"
                return jsonify({"dimensions": dimensions, "url_pneus": url_pneus})
            else:
                return jsonify({"error": "Aucune dimension de pneu n'a été récupérée."})
        else:
            return jsonify({"error": "Erreur lors de la deuxième requête."}), response_second_request.status_code
    else:
        return jsonify({"error": "Erreur lors de la première requête."}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
