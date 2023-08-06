# import Asclepius dependencies
from asclepius.instelling import GGZ, ZKH
from asclepius.medewerker import Medewerker

# import other dependencies
from selenium import webdriver
from typing import Union
from time import sleep

class PortaalDriver:
    driver = 'C:\Program Files (x86)\chromedriver.exe'
    
    def __init__(self, da: bool = False, bi: bool = False, zpm: bool = False):
        self.driver = PortaalDriver.driver
        self.portaal = None

        # Wat te testen
        self.da = da
        self.bi = bi
        self.zpm = zpm
    
    def open_portaal(self):
        self.portaal = webdriver.Chrome(self.driver)
        return None
    
    def inloggen(self, instelling: Union[GGZ, ZKH], gebruiker: Medewerker):
        # temp
        self.open_portaal()
        
        # haal de loginpagina op
        self.portaal.get(instelling.login)
        sleep(2)
        
        # vind invoer op de pagina
        username = self.portaal.find_element_by_name('username')
        password = self.portaal.find_element_by_name('password')
        submit = self.portaal.find_element_by_name('submit')
        
        # verstuur de informatie van de gebruiker
        username.send_keys(gebruiker.gebruikersnaam)
        password.send_keys(gebruiker.wachtwoord)
        submit.click()
        sleep(2)
        return

    # DAILY AUDIT FUNCTIES

    def download_da_excel(self, instelling: Union[GGZ, ZKH], test: bool = False):
        if test:
            da_link = instelling.daily_audit_test
            da_download_link = instelling.da_test_excel_download
        else:
            da_link = instelling.daily_audit
            da_download_link = instelling.da_excel_download
        
        self.portaal.get(da_link)
        sleep(2)
        if (not test) and (instelling.huidige_omgeving == "productie"):
            quickremove = self.portaal.find_element_by_class_name('quickRemove')
            quickremove_list = quickremove.find_elements_by_tag_name("li")
            for quickremove_item in quickremove_list:
                if quickremove_item.text == " Behandeld: Ja" or quickremove_item.text == " Behandeld: Nee":
                    delete_behandeld = quickremove_item.find_element_by_class_name('delete')
                    delete_behandeld.click()
                    sleep(3)
                    break
        self.portaal.get(da_download_link)
        sleep(5)
        return None

    def download_bi_excel(self, instelling: Union[GGZ, ZKH]):
        self.portaal.get(instelling.bi_prestatiekaart)
        sleep(2)
        self.portaal.get(instelling.bi_excel_download)
        sleep(5)
        return None

    def download_zpm_excel(self, instelling: Union[GGZ, ZKH]):
        self.portaal.get(instelling.zpm_prestatiekaart)
        sleep(2)
        self.portaal.get(instelling.zpm_excel_download)
        sleep(5)
        return None


    def webscraper_portaal(self, instelling: Union[GGZ, ZKH], gebruiker: Medewerker):
        # inloggen op het portaal
        self.inloggen(instelling, gebruiker)
        
        if self.bi and instelling.bi:
            # download excel BI prestatiekaart
            self.download_bi_excel(instelling)
            gebruiker.webscraper_hernoem_bestand(instelling, 'bi')
        else:
            pass

        if self.zpm and instelling.zpm:
            # download excel ZPM prestatiekaart
            self.download_zpm_excel(instelling)
            gebruiker.webscraper_hernoem_bestand(instelling, 'zpm')
        else:
            pass

        if self.da and instelling.da:
            # download excel controle/norm in productie
            self.download_da_excel(instelling, False)
            gebruiker.webscraper_hernoem_bestand(instelling, 'da', False)
        
            sleep(1)
        
            # download excel controle/norm in test
            self.download_da_excel(instelling, True)
            gebruiker.webscraper_hernoem_bestand(instelling, 'da', True)
        else:
            pass

        # sluit het portaal af
        self.portaal.close()
        return None

    def webscraper(self, instelling: Union[GGZ, ZKH], gebruiker: Medewerker):

        # download excels uit acceptatie omgeving
        instelling.kies_omgeving('acceptatie')
        self.webscraper_portaal(instelling, gebruiker)

        # download excels uit productie omgeving
        instelling.kies_omgeving('productie')
        self.webscraper_portaal(instelling, gebruiker)
        return None