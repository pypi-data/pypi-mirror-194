import os
import requests
from bs4 import BeautifulSoup
import datetime
import locale

def hello():
    print("Hi {0}".format(os.getlogin()))
    print("Thank you for using my python library")  

def lunch_jidelna_cz():
    locale.setlocale(locale.LC_ALL, "cs_CZ.utf8")  # nastavení české lokalizace
    # získání dnešního data
    dnes = datetime.date.today()
    # získání zítřejšího data
    zitra = dnes + datetime.timedelta(days=1)
    # formátování data
    format_datumu = "%A %d.%-m.%Y"
    dnesni_datum = dnes.strftime(format_datumu)
    zitresi_datum = zitra.strftime(format_datumu)
    # získání HTML obsahu stránky
    cantine_id = int(input("Entry your school cantine code (CZ jidelna.cz): "))
    url = "https://www.jidelna.cz/jidelni-listek/?jidelna={0}".format(cantine_id)
    response = requests.get(url)
    html = response.content
    # vytvoření objektu BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    # najití div elementu s trídou jidelniListek
    jidelni_listek_div = soup.find("div", {"class": "jidelniListek"})
    nazev_jidelny = soup.find("div", {"id": "headerJidelny"})
    nazev_jidelny =  nazev_jidelny.find("p")
    print(nazev_jidelny.text)
    # vypsání jednotlivých dnů a jídel
    def up_next():
       for den_div in jidelni_listek_div.find_all("div", {"class": "den"}):
        datum_div = den_div.find("div", {"class": "datum"})
        datum_text = datum_div.text.strip()
        den = str(datum_text).split()[0]+" "+str(datum_text).split()[1]+str(datum_text).split()[2]+str(datum_text).split()[3]
        i = 1
        # vypsání jídel jen pro dnešek a zítřek
        if den == dnesni_datum or den == zitresi_datum:
            print("=" * 50)
            if den == dnesni_datum:
                print(den, "- dnes")
            if den == zitresi_datum:
                print(den, "- zítra")    
            for menu_div in den_div.find_all("div", {"class": "menu"}):
                print(i)
                i = i + 1
                for menu_jidla_div in menu_div.find_all("div", {"class": "menuJidla"}):
                    for jidlo_row in menu_jidla_div.find_all("div", {"class": "row"}):
                        popiska_div = jidlo_row.find("div", {"class": "popiskaJidla"})
                        text_div = jidlo_row.find("div", {"class": "textJidla"})
                        popiska = popiska_div.text.strip()
                        text = text_div.text.strip()
                        print(f"{popiska} - {text}")  # vypsání názvu jídla s popiskou
                    print()  # výpis prázdného řádku pro oddělení jednotlivých jídel
    def all():
     for den_div in jidelni_listek_div.find_all("div", {"class": "den"}):
        datum_div = den_div.find("div", {"class": "datum"})
        datum_text = datum_div.text.strip()
        den = str(datum_text).split()[0]+" "+str(datum_text).split()[1]+str(datum_text).split()[2]+str(datum_text).split()[3]
        i = 1
        # vypsání jídel jen pro dnešek a zítřek
        print("=" * 50)
        print(den)    
        for menu_div in den_div.find_all("div", {"class": "menu"}):
                print(i)
                i = i + 1
                for menu_jidla_div in menu_div.find_all("div", {"class": "menuJidla"}):
                    for jidlo_row in menu_jidla_div.find_all("div", {"class": "row"}):
                        popiska_div = jidlo_row.find("div", {"class": "popiskaJidla"})
                        text_div = jidlo_row.find("div", {"class": "textJidla"})
                        popiska = popiska_div.text.strip()
                        text = text_div.text.strip()
                        print(f"{popiska} - {text}")  # vypsání názvu jídla s popiskou
                print()  # výpis prázdného řádku pro oddělení jednotlivých jídel
    answer = input("Do you want all of list or only what up next type([all, up_next]): ")
    if answer not in ["all", "up_next"]:
        print("Jakubsulla-error : bad user input")        
        exit()
    if answer == "all":
        all()
    if answer == "up_next":
        up_next()    