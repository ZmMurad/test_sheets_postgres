import requests
import xml.etree.ElementTree as ET


def get_currency_rate(char_code_currency="USD"):
    """
    :param char_code_currency: can see here - https://www.cbr.ru/scripts/XML_daily.asp
    :return: float_number
    """
    return float(
    ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text).find(
    './Valute[CharCode="USD"]/Value').text.replace(',', '.')
    )


