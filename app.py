import streamlit as st
import requests
import re

def search_vehicle_by_plate(plate_number):
    url = f"https://www.midas.fr/api/ecrm/vehicles/tires/search/platenumber/{plate_number}?plateLocale=FR"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Déclenche une erreur pour les codes d'état HTTP non valides
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Une erreur s'est produite : {e}")
        return None
    except ValueError:
        st.error("Impossible d'analyser la réponse JSON.")
        return None

def validate_plate_number(plate_number):
    # Expression régulière pour les numéros de plaque d'immatriculation français
    pattern = r"^[A-Z]{2}\d{3}[A-Z]{2}$"
    return re.match(pattern, plate_number)

def main():
    st.title("Recherche de véhicule par plaque d'immatriculation")
    
    plate_number = st.text_input("Entrez le numéro de plaque d'immatriculation :")
    
    if st.button("Rechercher"):
        if not plate_number:
            st.warning("Veuillez entrer un numéro de plaque d'immatriculation.")
        elif not validate_plate_number(plate_number):
            st.error("Format de plaque incorrect. Veuillez saisir une plaque au format AA306VV.")
        else:
            vehicle_data = search_vehicle_by_plate(plate_number)
            if vehicle_data:
                st.json(vehicle_data)
            else:
                st.error("Aucun résultat trouvé pour cette plaque d'immatriculation.")

if __name__ == "__main__":
    main()
