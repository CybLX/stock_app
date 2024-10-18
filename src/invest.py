from selenium.webdriver.common.by import By
from torch.utils.data import Dataset
from datetime import date, datetime
from unidecode import unidecode
from selenium import webdriver
from datetime import datetime
import pandas as pd
import calendar
import sqlite3
import pickle
import bs4
import re
import os







class controle:
    dir_path = os.getcwd()
    dir_hist = dir_path + '/tmp/'
    profile = os.path.join(dir_path + '/WebDriver/bin/',"profile","ativos")
    
    # Setup ativos          br.investing is blocked by the cloudflare anti-bot system :'(  --> Update type = 1 is broken                     
    # LIST OF SITES TO CHECK DATABASE AND UPDATE IT
    http = {'Table Name' : 'External Link',
            "MRFG3"      : 'Some site .com'}
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir={}".format(self.profile))
        options.add_argument("--disable-infobars")
        options.add_argument("--enable-popup-blocking")

        self.driver = webdriver.Chrome(options = options)
        self.driver.minimize_window()
    
    def news(self,target,keywords = None, max_news = 5):
        #max_news = 10  # max number of articles
        #keywords = ['MRFG3','Marfrig']
        
        
        
        try:
            self.driver.get(f'https://news.google.com/search?q={target}')
            webcontent = bs4.BeautifulSoup(self.driver.page_source, "html.parser")

            articles_list = {}
            dados = []     
                                                                
            for ictr,i in enumerate(webcontent.find_all(class_="PO9Zff Ccj79 kUVvS")):
               #if len(articles_list) == max_news: break   # exit outer loop
               for link in i.find_all(class_ = 'IFHyqb DeXSAc'):  #JtKRv
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
            #hj = dados.loc[dados['data'] == datetime.today().strftime('%Y-%m-%d')]
            return (dados, articles_list)
        except Exception as e:  
            print("Mr.: Erro_News meu véio. --> ",e)


    def diario(self, ativo, update = 1, bach_size = 5):
        #br.investing is blocked by the cloudflare anti-bot system :'(  --> Update type = 1 is broken   
        if update == 1:
            print('\n'+ '*'*20 +'\n' + 'BUSCANDO ATUALIZACOES' + '\n' +"*"*20)        
            for ativo in self.http.keys():
                self.driver.get(self.http[ativo])
                elem = self.driver.find_element(by=By.XPATH , value = '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/table')
                soup = bs4.BeautifulSoup(elem.get_attribute('innerHTML'), 'html.parser')

                colum = []
                for row in soup.findAll("th"):
                    colum.append(unidecode(row.text.lower()))

                count = 0
                download = []
                save = []
                for i in soup.find('tbody').find_all('td'):
                    save.append(i.text)
                    count += 1
                    if count == 7: 
                        download.append(save)
                        save = []
                        count = 0

                download = pd.DataFrame(download, columns = ['date','last','first','max','min','vol','var'])
                self.check_update(download = download, ativo = ativo)
            print('\n'+ '*'*20 +'\n' + 'BANCO DE DADOS ATUALIZADO' + '\n' +"*"*20)
            
        
        elif update == 0:
            print('\n'+ '*'*20 +'\n' + 'INICIALIZANDO SINCRONIZACAO DE BUFFERS...' + '\n' +"*"*20)
            print('\n' +'controle diario nivel 0' + '\n')
            
            # Set the batch
            myds = Dataset_Update(driver = self.driver)
            
            batchS = 0
            batch  =  []           
            while batchS != bach_size:
                #collect statment
                for ativo in self.http.keys():
                    st = myds[ativo]
                    
                    # check for error
                    if isinstance(st, str):
                        pass
                    else:
                        batch.append(st)
                batchS += 1

            batch = pd.concat(batch, axis = 0, ignore_index = False)

            preds = self.load_predict(ativo)
            
            return preds

    @staticmethod
    def load_predict(ativo): # It's not a real prediction! Initialize your model and override this function.

        with open(f'./models/{ativo}/{ativo}_forecast.pkl', 'rb') as f:
            forecast = pickle.load(f)
        with open(f'./models/{ativo}/{ativo}_history.pkl', 'rb') as f:
            history = pickle.load(f)
        day = 1
        preds = []
        for yhat in forecast:
            inverted = yhat + history[-365]
            preds.append((day, round(float(inverted[0]),3)))
            print('Day %d: %f' % (day, inverted))
            day += 1
        return preds 
         
    @staticmethod
    def check_update(download, ativo):
        download = controle.tratamento(download = download)
        
        connection = sqlite3.connect('./tmp/invst.db')
        hist_collect = pd.read_sql(f"SELECT date FROM '{ativo}'", connection)

        update_checks = []
        for my_date in list(download['date']):
            if my_date in list(hist_collect.date) or my_date == str(date.today()):
                pass
            else:
                update_checks.append(my_date)

        if len(update_checks) == 0 :
                    print('*'*20 + '\n' + 'SEM ATUALIZACAO de {}'.format(ativo) + '\n' +  '*'*20)
                    connection.commit()

        else:
            pack_atualiza = []

            for d in update_checks:
                pack = download.loc[download['date'] == d].copy()
                pack['weekday'] = calendar.day_name[date.fromisoformat(d).weekday()] 
                pack_atualiza.append(pack)
            atualizado = pd.concat(pack_atualiza, axis=0).sort_values(by = 'date').reset_index(drop = True)
            atualizado = atualizado.set_index('date')
            atualizado.to_sql('{}'.format(ativo), con = connection, if_exists = 'append')
            connection.commit()
            print('*'*20 + '\n' + 'ATUALIZADO: {}'.format(ativo) + '\n' + '*'*20)

    @staticmethod
    def replace_multiply(value : str):
        prefix_to_power = {'K' : 10e3, 'M' : 10e6}
        if pd.notna(value):
            if value != "":
                prefix = value[-1]

                if prefix in prefix_to_power.keys():
                    valor_numerico = float(value[:-1])
                    value = prefix_to_power[prefix] * valor_numerico
            else:
                value = 0
        return value
    
    @staticmethod
    def tratamento(download):
        download.replace({",":"."}, regex = True, inplace = True)
        download.replace({"%":""}, regex =True, inplace=True)
        download['vol'] = download['vol'].apply(controle.replace_multiply)
        download.fillna(0, inplace = True)
        download['date'] = pd.to_datetime(download['date'], format= '%d.%m.%Y').dt.date
        download = download.astype({'date' : str, "last" : float, "first" : float, 'max' : float, 'min':float,'vol' : int, 'var': float })
        return download
    



class Dataset_Update(Dataset):
            
    def __init__(self, driver):
        self.driver = driver
        self.statement = None
    def __getitem__(self, index):

        try:
            self.driver.get('https://www.google.com/finance/quote/{}:BVMF'.format(index))
            cota_atual = self.driver.find_element(by = By.CLASS_NAME, value = 'rPF6Lc').text
        
        except Exception as error:
            self.statement = f"{index} not found on google finance!"
            print(repr(error) + ": " + self.statement )
        else:
            cota_atual = cota_atual.replace(',','.')
            cota_atual = cota_atual.split(sep = '\n')
            cota_atual = [float(re.sub("[^0-9.-]","",s)) for s in cota_atual]
            self.statement = pd.DataFrame({'cotacao' : cota_atual[0],
                                        'var' : cota_atual[1],
                                        'now-last' : cota_atual[2],
                                        'hora' : [datetime.now().hour],
                                        'minuto':[datetime.now().minute],
                                        'segundo':[datetime.now().second]}, index= [index])                  
        finally:
            return self.statement
