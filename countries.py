from traducir import en2es, es2en
import requests


def template(country):
    url2 = f"https://restcountries.com/v3.1/translation/{country}"
    response = requests.get(url2)
    output_string = ""
    if response.status_code == 200:
        data = response.json()
        output_string += f"--- Datos de {en2es(country)} ---\n"

        # 1. Nombre
        output_string += f"Nombre Común: {en2es(data[0]['name']['common'])}\n"
        output_string += f"Nombre Oficial: {en2es(data[0]['name']['official'])}\n"
        output_string += f"Bandera: {data[0]['flags']['png']}\n" # Incluimos la URL de la bandera aquí

        # 2. Capital
        capital = data[0].get('capital', 'No disponible')[0]
        output_string += f"Capital: {capital}\n"

        # 3. Región y Subregión
        output_string += f"Región: {en2es(data[0].get('region', 'No disponible'))}\n"
        output_string += f"Subregión: {en2es(data[0].get('subregion', 'No disponible'))}\n"

        # 4. Población
        output_string += f"Población: {data[0].get('population', 'No disponible'):,}\n"

        # 5. Área
        output_string += f"Área: {data[0].get('area', 'No disponible'):,} km²\n"

        # 6. Idiomas
        output_string += "Idiomas:\n"
        languages = data[0].get('languages', {})
        if languages:
            for code, lang_name in languages.items():
                output_string += f"  - {en2es(lang_name)} ({code})\n"
        else:
            output_string += "  - No disponibles\n"

        # 7. Monedas
        output_string += "Monedas:\n"
        currencies = data[0].get('currencies', {})
        if currencies:
            for code, currency_info in currencies.items():
                output_string += f"  - {en2es(currency_info.get('name', 'N/A'))} ({code}), Símbolo: {currency_info.get('symbol', 'N/A')}\n"
        else:
            output_string += "  - No disponibles\n"

        # 8. Código de país (ISO)
        output_string += f"Código ISO Alpha-2: {data[0].get('cca2', 'No disponible')}\n"
        output_string += f"Código ISO Alpha-3: {data[0].get('cca3', 'No disponible')}\n"

        # 9. Dominios de Nivel Superior (TLD)
        tld = ', '.join(data[0].get('tld', ['No disponible']))
        output_string += f"TLD: {tld}\n"

        # 10. Husos Horarios
        timezones = ', '.join(data[0].get('timezones', ['No disponible']))
        output_string += f"Husos Horarios: {timezones}\n"

        # 11. Latitud y Longitud
        latlng = data[0].get('latlng')
        if latlng and len(latlng) == 2:
            output_string += f"Latitud: {latlng[0]}, Longitud: {latlng[1]}\n"
        else:
            output_string += "Latitud/Longitud: No disponibles\n"
        
        return output_string
    else:
        return "Oops. Ocurrió un problema."


def rest_countries(prompt):
    try:
        url1 = "https://restcountries.com/v3.1/all?fields=name"
        response = requests.get(url1)
        if response.status_code == 200:
            data = response.json()
            c_list = [data[i]["name"]["common"] for i in range(len(data))]
            large_name_c = ["República Dominicana", "República Democrática del Congo", "Guinea-Bisáu", "Guinea Ecuatorial", "Samoa Americana"]
        for country in large_name_c:
            if country.lower() in prompt.lower():
                return template(country)
        eng_prompt = es2en(prompt)
        for country in c_list:
            if country.lower() in eng_prompt.lower():
                return template(country)
        else:
            return "No se encontraron datos."
    except Exception as e:
        return "Disculpa. Algo salió mal con tu petición. Revisa tu conexión a Internet o prueba escribiendo de otra manera."