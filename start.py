#%%
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd
from src.invest import controle, Dataset_Update
from src.zapzap import zapbot

def life():
    ctrl = controle()
    bot = zapbot()
    bot.abre_conversa(input("Insira seu numero de telefone: "))
    sleep(5)
    bot.envia_msg("Olá, Mr!" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "Escolha suas opcoes:" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "- /check" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "- /update" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "- /monitor" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)  + "- /pesquisa" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)  + "- /help" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)  +  "- /quit" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT))

    msg = ''
    pause = True
    print(msg)
    while pause:
        msg = bot.ultima_msg()
        if msg == '/check':
            sleep(2)
            bot.envia_msg('Aguarde um momento, checando....')
            sleep(2)
            
            ds = Dataset_Update(driver = ctrl.driver)

            buffer = []
            for i in ctrl.http.keys():
                statement = ds[i]
                if type(statement) != str:
                    buffer.append(statement)
                else: pass

            buffer = pd.concat(buffer, axis = 0)

            string = ""
            for atv in buffer.index: 
                strings = '*{} : {}*'.format(atv,buffer.loc[atv,'cotacao'])
                strings += ' ' +  (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
                string += strings
            bot.envia_msg(string)
            bot.envia_msg("Algo a mais, senhor?")

        elif msg == '/update':
            # Setup ativos          br.investing is blocked by the cloudflare anti-bot system :'(  --> diario.Update = 1 is broken
            bot.envia_msg('Procurando e Atualizando, aguarde um momento')
            ctrl.diario(update = 1, ativo = None)
            bot.envia_msg('*Banco de Dados atualizado*')
            bot.envia_msg("Algo a mais, senhor?")

        elif msg == '/help':
            bot.envia_msg("Olá, Mr!" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "Escolha suas opcoes:" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "- /check" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "- /update" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + "- /monitor" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)  + "- /pesquisa" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)  + "- /help" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)  +  "- /quit" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT))
        
        elif msg == '/monitor':
            keys = list(ctrl.http.keys())
            query = '*Selecione um dos ativos para previsao:* ' + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)

            for i in keys:
                query += i + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
            bot.envia_msg(query)
            
            string = 'Aguardando uma selecao:'
            bot.envia_msg(string)
            t = 0
            while t != 10:
                option = bot.ultima_msg()

                if option == string:
                    t += 1
                    sleep(2)
                else:
                    bot.envia_msg(f'Iniciando Sincronizacao diaria: {option}')
                    result = ctrl.diario(update = 0, ativo = option)
                    bot.envia_msg('Sem atividades bruscas, realizando previsao dos proximos dias uteis')

                    query = f"Previsoes de {option}" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT) + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
                    for day, pred in result:
                        query += f"*{day}* : {pred}" + (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
                    
                    bot.envia_msg(query)
                    t = 10
            bot.envia_msg("Algo a mais, senhor?")

        elif msg == "/pesquisa":

            #de_hj = dados[dados['data'] == date.today()]
            
            string = "O que busca meu véio?"
            bot.envia_msg(string)
            t = 0
            while t != 10:
                option = bot.ultima_msg()

                if option == string:
                    t += 1
                    sleep(2)
                else:
                    string = f"Pesquisando sobre {option}"
                    bot.envia_msg(string)
                    dados, artigos = ctrl.news(target = option)
                    dados['data'] = pd.to_datetime(dados['data'], format= '%Y-%m-%d')
                    filtro = dados[dados['Publicado a'].dt.days < 2]
                    
                    if filtro.empty:
                        filtro = dados[dados['Publicado a'].dt.days < 4]
                        if filtro.empty:
                            bot.envia_msg('Sem noticias nos ultimos 4 dias')
                        bot.envia_msg("Algo a mais, senhor?")
                        t = 10
                    else:
                        filtro = filtro[0:5].sort_values(by = ['Publicado a'])                 
                        filtro = list(zip(filtro.title, filtro.link))
                        bot.envia_msg("Segue os links, chefe:")
                        for title, link in filtro:
                            string = ""
                            string += title
                            string += (Keys.SHIFT) + (Keys.ENTER) + (Keys.SHIFT)
                            string += link
                            bot.envia_msg(string)
                        sleep(2)
                        bot.envia_msg("Algo a mais, senhor?")
                        t = 10
        elif msg == "/quit":
            bot.envia_msg("Até logo!")
            bot.envia_msg("Caso queria ativar novamente, solicite atendimento")
            ctrl.driver.quit()
            bot.driver.quit()
            pause = False
            break

life()

# %%
