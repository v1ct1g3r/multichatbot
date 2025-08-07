from traducir import en2es
import requests


def chuck_norris(prompt):
    """Obtener una broma acerca de Chuck Norris"""
    try:
        categories = requests.get("https://api.chucknorris.io/jokes/categories").json()
        for category in categories:
            if category in prompt:
                url = f"https://api.chucknorris.io/jokes/random?category={category}"
                response = requests.get(url)
                data = response.json()
                break
        else:
            return "Disculpa. Al parecer esa categoría no existe."

        if response.status_code == 200:
            broma = data["value"]
            return en2es(broma)
    except Exception as e:
        return "Disculpa. Ocurrió un problema al buscar el chiste."