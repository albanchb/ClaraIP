import requests
import ipaddress
import sys
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

def install_dependencies():
    """
    Vérifie et installe les dépendances nécessaires.
    """
    required_packages = ["requests", "colorama"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(Fore.YELLOW + f"Installation de la dépendance manquante : {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

def display_banner():
    """
    Affiche la bannière de l'application.
    """
    banner = r"""
  ____ _                  
 / ___| | __ _ _ __ __ _ 
| |   | |/ _` | '__/ _` |
| |___| | (_| | | | (_| |
 \____|_|\__,_|_|  \__,_|
    """
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.YELLOW + Style.BRIGHT + "Welcome to Clara, a IP scanner\n")

def is_private_ip(ip):
    """
    Vérifie si une adresse IP est privée (IPv4 ou IPv6).
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return True  

def analyze_ip(ip_address):
    """
    Analyse une adresse IP via l'API DDoR.
    """
    token = "tonapikey"
    url = f"https://ipinfo.io/{ip_address}?token={token}"

    if is_private_ip(ip_address):
        return {"Erreur": "L'adresse IP est privée ou invalide, elle ne peut pas être localisée."}

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        ip_info = {
            "Adresse IP": data.get("ip", "Non disponible"),
            "Hostname": data.get("hostname", "Non disponible"),
            "Ville": data.get("city", "Non disponible"),
            "Région": data.get("region", "Non disponible"),
            "Pays": data.get("country", "Non disponible"),
            "Localisation (lat, lon)": data.get("loc", "Non disponible"),
            "Organisation (FAI)": data.get("org", "Non disponible"),
            "Code Postal": data.get("postal", "Non disponible"),
            "Fuseau Horaire": data.get("timezone", "Non disponible"),
        }

        return ip_info

    except requests.exceptions.HTTPError as http_err:
        return {"Erreur": f"HTTP Error : {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"Erreur": f"Request Error : {req_err}"}

if __name__ == "__main__":
    display_banner()

    while True:
        print(Fore.GREEN + "=== Analyseur d'adresse IP avec l'API DDoR ===")
        ip = input(Fore.BLUE + "Entrez une adresse IP (IPv4 ou IPv6) à analyser ou 'q' pour quitter : ").strip()
        
        if ip.lower() == 'q':  
            print(Fore.YELLOW + "Merci d'avoir utilisé Clara ! À bientôt.")
            break

        result = analyze_ip(ip)

        print(Fore.GREEN + "\n=== Résultats de l'analyse ===")
        for key, value in result.items():
            if "Erreur" in key:
                print(Fore.RED + f"{key} : {value}")
            else:
                print(Fore.YELLOW + f"{key} : {value}")
        
        print(Fore.CYAN + "\nAnalyse terminée. Vous pouvez entrer une nouvelle IP ou 'q' pour quitter.")
