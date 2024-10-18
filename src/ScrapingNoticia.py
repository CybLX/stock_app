import bs4
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from time import sleep

class web:
    dir_path = os.getcwd()
    dir_hist = dir_path + '/tmp/'
    profile = os.path.join(dir_path + '/WebDriver/bin/',"profile","ativos")
    

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir={}".format(self.profile))
        options.add_argument("--disable-infobars")
        options.add_argument("--enable-popup-blocking")

        self.driver = webdriver.Chrome(options)
        #self.driver.minimize_window()


    def news(self,target,keywords = None, max_news = 5):
        #max_news = 10  # max number of articles
        #keywords = ['MRFG3','Marfrig']
        
        self.driver.get('https://news.google.com/')
        try:
            sleep(3)
            self.driver.find_element(By.XPATH, value='//*[@id="gb"]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]').send_keys(target)
            self.driver.find_element(By.XPATH,value='//*[@id="gb"]/div[2]/div[2]/div/form/button[4]').click()
            sleep(3)
            webcontent = bs4.BeautifulSoup(self.driver.page_source, "html.parser")

            articles_list = {}
            dados = []     

            for ictr,i in enumerate(webcontent.find_all(class_="lBwEZb BL5WZb GndZbb")):
               #if len(articles_list) == max_news: break   # exit outer loop
               for link in i.find_all(class_ = 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc'): 
                noticia_link = str(link.find('a')['href'])[1:]
                texto = link.text
                data = link.find('time')['datetime'][0:10]
                time = link.find('time')['datetime'][11:19]
                x = pd.DataFrame({'title' :[texto],
                                'link' : ["https://news.google.com"+noticia_link],
                                'data' : [data],
                                'time': [time],
                                'Publicado a': [datetime.today() - pd.to_datetime(data+' '+time)]})
                dados.append(x)                        
                
                if keywords is not None :
                    
                    if any(keyword_ in texto for keyword_ in keywords):
                        articles_list.update({texto : "https://news.google.com"+noticia_link})
                        if len(articles_list) == max_news: break  # exit inner loop                    
                else:
                    pass

            dados = pd.concat(dados).reset_index(drop = True)
            self.driver.close()
            #hj = dados.loc[dados['data'] == datetime.today().strftime('%Y-%m-%d')]
            return dados,articles_list
        except Exception as e:  
            print("Mr. Jack: Erro_News meu véio. --> ",e)
#%%
