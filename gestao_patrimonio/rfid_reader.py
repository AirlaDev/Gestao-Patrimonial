import requests

def ler_tag_rfid():
    url = "http://endereco-do-leitor/ler-tag"  # Substitua pelo endereço real da API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tag_id = data.get('tag_id')
            tag_text = data.get('tag_text')
            return tag_id, tag_text
        else:
            print(f"Erro na leitura da tag: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Erro ao conectar com o leitor RFID: {e}")
        return None, None