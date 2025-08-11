from traducir import en2es
import requests


def process_ip_data(data):
    output_string = f"--- Datos de IP: {data.get('ip', 'No disponible')} ---\n"

    # 1. IP
    output_string += f"IP: {data.get('ip', 'No disponible')}\n"
    output_string += f"Tipo: {data.get('type', 'No disponible')}\n"

    # 2. Localización Geográfica
    output_string += f"Continente: {en2es(data.get('continent', 'No disponible'))} ({data.get('continent_code', 'No disponible')})\n"
    output_string += f"País: {en2es(data.get('country', 'No disponible'))} ({data.get('country_code', 'No disponible')})\n"
    output_string += f"Región: {en2es(data.get('region', 'No disponible'))} ({data.get('region_code', 'No disponible')})\n"
    output_string += f"Ciudad: {en2es(data.get('city', 'No disponible'))}\n"
    output_string += f"Código Postal: {data.get('postal', 'No disponible')}\n"
    output_string += f"Latitud: {data.get('latitude', 'No disponible')}, Longitud: {data.get('longitude', 'No disponible')}\n"

    # 3. Capital y Fronteras (desde los datos del país, si están disponibles)
    output_string += f"Capital del País: {en2es(data.get('capital', 'No disponible'))}\n"
    borders = data.get('borders')
    if borders:
        output_string += f"Fronteras: {borders.replace(',', ', ')}\n"
    else:
        output_string += "Fronteras: No disponibles\n"

    # 4. Bandera
    flag_info = data.get('flag', {})
    if flag_info:
        output_string += f"Bandera (URL): {flag_info.get('img', 'No disponible')}\n"
        output_string += f"Bandera (Emoji): {flag_info.get('emoji', 'No disponible')}\n"
    else:
        output_string += "Bandera: No disponible\n"

    # 5. Conexión
    connection_info = data.get('connection', {})
    if connection_info:
        output_string += "Información de Conexión:\n"
        output_string += f"  - ASN: {connection_info.get('asn', 'No disponible')}\n"
        output_string += f"  - Organización: {connection_info.get('org', 'No disponible')}\n"
        output_string += f"  - ISP: {connection_info.get('isp', 'No disponible')}\n"
        output_string += f"  - Dominio: {connection_info.get('domain', 'No disponible')}\n"
    else:
        output_string += "Información de Conexión: No disponible\n"

    # 6. Zona Horaria
    timezone_info = data.get('timezone', {})
    if timezone_info:
        output_string += "Zona Horaria:\n"
        output_string += f"  - ID: {timezone_info.get('id', 'No disponible')}\n"
        output_string += f"  - Abreviatura: {timezone_info.get('abbr', 'No disponible')}\n"
        output_string += f"  - UTC: {timezone_info.get('utc', 'No disponible')}\n"
        output_string += f"  - Hora Actual: {timezone_info.get('current_time', 'No disponible')}\n"
    else:
        output_string += "Zona Horaria: No disponible\n"

    # 7. Moneda
    currency_info = data.get('currency', {})
    if currency_info:
        output_string += "Moneda:\n"
        output_string += f"  - Nombre: {en2es(currency_info.get('name', 'N/A'))}\n"
        output_string += f"  - Código: {currency_info.get('code', 'N/A')}\n"
        output_string += f"  - Símbolo: {currency_info.get('symbol', 'N/A')}\n"
    else:
        output_string += "Moneda: No disponible\n"

    # 8. Seguridad
    security_info = data.get('security', {})
    if security_info:
        output_string += "Seguridad:\n"
        output_string += f"  - Anónimo: {en2es(str(security_info.get('anonymous', 'N/A')))}\n"
        output_string += f"  - Proxy: {en2es(str(security_info.get('proxy', 'N/A')))}\n"
        output_string += f"  - VPN: {en2es(str(security_info.get('vpn', 'N/A')))}\n"
        output_string += f"  - TOR: {en2es(str(security_info.get('tor', 'N/A')))}\n"
        output_string += f"  - Hosting: {en2es(str(security_info.get('hosting', 'N/A')))}\n"
    else:
        output_string += "Seguridad: No disponible\n"

    return output_string

def get_ip_info(ip_address):
    url = f"http://ipwho.is/{ip_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return process_ip_data(data)
            else:
                return f"Error de la API: {data.get('message', 'Error desconocido')}"
        else:
            return f"Error al obtener datos: Estado HTTP {response.status_code}"
    except:
        return f"Ocurrió un error inesperado."