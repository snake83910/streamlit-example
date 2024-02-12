import streamlit as st
import requests

def search_vehicle_by_plate(plate_number):
    url = f"https://www.midas.fr/api/ecrm/vehicles/tires/search/platenumber/{plate_number}?plateLocale=FR"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def main():
    st.title('Recherche de véhicule par plaque d\'immatriculation')
    
    plate_number = st.text_input('Entrez le numéro de plaque d\'immatriculation :')
    
    if st.button('Rechercher'):
        if plate_number:
            vehicle_data = search_vehicle_by_plate(plate_number)
            if vehicle_data:
                st.json(vehicle_data)
            else:
                st.error('Aucun résultat trouvé pour cette plaque d\'immatriculation.')
        else:
            st.warning('Veuillez entrer un numéro de plaque d\'immatriculation.')

if __name__ == "__main__":
    main()
