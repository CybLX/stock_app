from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


class zapbot:
    dir_path = os.getcwd()
    dir_hist = dir_path + '/tmp/'
    profile = os.path.join(dir_path + '/WebDriver/',"profile","web")
    url = "https://web.whatsapp.com"
    
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        service = Service(executable_path = r'./WebDriver/chromedriver')

        # Configurando a pasta profile, para mantermos os dados da seção
        self.options.add_argument(
            r"user-data-dir={}".format(self.profile))
        #self.options.add_argument("--disable-infobars")
        #self.options.add_argument('--headless=new')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--enable-popup-blocking")
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(service = service, options = self.options)
        # Abre o whatsappweb
        self.driver.get(self.url)
        print("Scan QR Code, And then Enter")
        input()
        self.driver.minimize_window()

        print("Logged In")

    def ultima_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            mensages = soup.find_all('span', attrs={'class':'_ao3e'})
            ultima = len(mensages) - 1
            return mensages[ultima].text
        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")

    def envia_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """
        try:
            conteudo = self.driver.switch_to.active_element
            conteudo.send_keys(msg)
            conteudo.send_keys(Keys.RETURN)

        except Exception as e:
            print("Erro ao enviar msg", e)

    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            conversa = (self.url + '/send?phone=' + str(contato))
            self.driver.get(conversa)
        except Exception as e:
            raise e
    
    #def envia_media(self, fileToSend):
    #    """ Envia media """
    #    try:
    #        # Clica no botão adicionar
    #        self.driver.find_element(by = By.CSS_SELECTOR, value= "span[data-icon='clip']").click()
    #        # Seleciona input
    #        attach = self.driver.find_element(by = By.CSS_SELECTOR, value="input[type='file']")
    #        # Adiciona arquivo
    #        attach.send_keys(fileToSend)
    #        # sleep(3)
    #        # Seleciona botão enviar
    #        send = self.driver.find_element(by= By.XPATH, value= "//div[contains(@class, 'yavlE')]")
    #        # Clica no botão enviar
    #        send.click()
    #    except Exception as e:
    #        print("Erro ao enviar media", e)
