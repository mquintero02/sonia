import pywhatkit
import requests

def pruebaws():

    try:
        request = requests.get("https://google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        print("Sin conexión a internet.")
    else:
        print("Con conexión a internet.")
        
        pywhatkit.sendwhatmsg_instantly("+584149153212", "una linea")
        pywhatkit.sendwhatmsg_instantly("+584149153212", "fdsafsd fdsaf \n con varias lineas \n fdsafds probar")

pruebaws()
