from bs4 import BeautifulSoup
from decouple import config
import requests

def proccessFile(soup):
    # Obtener los headers
    html_headers = soup.find_all('th')
    headers = []
    for header in html_headers:
        headers.append(header.text)

    main_headers = headers[:2]
    secundary_headers = headers[3:]

    # Filas de datos
    data_body = soup.find_all('tr')
    data = data_body[5:]

    salida = []

    for row in data:
        values = row.findAll('td')
        utc_3 = values[0].text
        dir_viento = values[1].text
        mag_viento = values[2].text
        fuerza_viento = values[3].text
        dir_oleaje = values[4].text
        tp_oleaje = values[5].text
        hm_oleaje = values[6].text

        salida.append([utc_3,dir_viento,mag_viento,fuerza_viento,dir_oleaje,tp_oleaje,hm_oleaje])

    return salida

def collectData():

    # MAIN
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    try:
        print('Extrayendo datos de la URL...')
        html_text = requests.get(config('URL'), headers=headers).content
        soup = BeautifulSoup(html_text, 'lxml')
        print('----- Extraccion finalizada ----- \n')
        return proccessFile(soup)

    except Exception as e:
        print('ERROR:', e.__str__())
