import requests

# Cole o seu link do Xano aqui entre as aspas
BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:u798as7d" 

def get_subjects():
    try:
        # O Streamlit vai tentar buscar os dados nesta URL
        response = requests.get(f"{BASE_URL}/subjects")
        return response.json()
    except Exception as e:
        return {"error": str(e)}