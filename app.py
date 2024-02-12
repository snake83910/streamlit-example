from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def search_vehicle_by_plate(plate_number):
    url = f"https://www.midas.fr/api/ecrm/vehicles/tires/search/platenumber/{plate_number}?plateLocale=FR"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@app.route('/')
def frontend():
    return render_template('frontend.html')

@app.route('/search')
def search():
    plate_number = request.args.get('plateNumber')
    vehicle_data = search_vehicle_by_plate(plate_number)
    return jsonify(vehicle_data)

if __name__ == "__main__":
    app.run(debug=True)
