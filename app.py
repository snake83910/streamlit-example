from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def search_vehicle_by_plate(plate_number):
    url = f"https://www.midas.fr/api/ecrm/vehicles/tires/search/platenumber/{plate_number}?plateLocale=FR"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Erreur {response.status_code} lors de la requête."}

@app.route('/search-vehicle', methods=['GET'])
def search_vehicle():
    plate_number = request.args.get('plate_number')
    if not plate_number:
        return jsonify({"error": "Numéro de plaque d'immatriculation manquant."}), 400
    
    vehicle_data = search_vehicle_by_plate(plate_number)
    
    return jsonify(vehicle_data)

if __name__ == '__main__':
    app.run(debug=True)
