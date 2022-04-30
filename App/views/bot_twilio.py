from App import  db
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from App.views import pessoas,mensagewhatsapp
from App.model.mensagewhatsapp import MensageWhatsApp
from twilio.rest import Client
from App.views import several

import re

# -------------------------- BOT WHATSAPP USANDO TWILIO --------------------------
def bottwilio():

    def return_dados_clima(strcity,locale):
        units = 'metric'  # metric = Celsius, imperial = Fahrenheit, default = Kelvin
        # if lat != '' and lon != '':
        #    weather = search_dados_temperatura_lat_lon(lat, lon, units)
        quote = ''
        weather = several.search_dados_temperatura_city(strcity, units)
        if weather["cod"] != '404':
            quote += f'\n👇 *Clima Hoje em {locale}* 👇:\n'
            try:
                weather_cond = weather['weather'][0]
                cond = weather_cond['main'] + ", " + weather_cond['description']
                cond = several.translate(cond)
                import json
                cond = json.loads(cond)
                quote += f'Situação: {cond["traducao"]}\n'
            except:
                quote += ''
            try:
                weather_temp = weather['main']
                temp_max = weather_temp['temp_max']
                temp_min = weather_temp['temp_min']
                temp_atual = weather_temp['temp']
                quote += f'Temperatura Atual: {temp_atual}º\n' \
                         f'Temperatura Máxima: {temp_max}º\n' \
                         f'Temperatura Mínima: {temp_min}º'
            except:
                quote += ''


        return quote

    def return_quote_menumain():
        return f'{"Escolha uma opção:"}\n\n' \
        f'{"1 - Traduzir Textos "}\n' \
        f'{"2 - Rastrear Objeto Correios"}\n' \
        f'{"3 - Busca CEP"}\n' \
        f'{"4 - Previsão de Tempo Por Cidade"}'

    def return_quote_pai():
        return f'{"Escolha uma opção:"}\n' \
               f'{"1 - Meta Calórica "}\n' \
               f'{"2 - Ferramentas"}\n'

    client = Client('9yZpqWzhZov-O6uk733HPs-Bs545GI8HJY2mx5Hf','9yZpqWzhZov-O6uk733HPs')
    resp = MessagingResponse()

    msg = resp.message()

    incoming_msg = request.values.get('Body','')
    responded = False
    if incoming_msg != '':
        phone = request.values.get('WaId','')
        namephone = request.values.get('ProfileName','')

        # busca pessoa se ja ta cadastrada no banco atraves do banco de dados
        pessoa = pessoas.get_pessoa_by_phone(phone)

        if pessoa:
            # ------- PESSOA JA CADASTRADA NO BD, VERIFICADO PELO TELEFONE -------

            # Verifica se ja mandou mensagem -> Chatbot
            msgzap = mensagewhatsapp.getmensagewhatsapp(pessoa.id)


            # PESSOA ACEITOU A SER CADASTRADA OU PESSOA JA ENCONTRA-SE COM O CONTATO SALVO NO BD

            if not msgzap:
                # ETAPA 2 : CADASTRA EMAIL
                pessoa.nome = incoming_msg
                db.session.commit()
                msgzap = MensageWhatsApp(etapa=2,pergunta='Digita seu nome',proceed='S',
                                                  resposta='Digite seu email',idpessoa=pessoa.id)
                db.session.add(msgzap)
                db.session.commit()

                quote = f'{incoming_msg}{", digite seu email:"}'
                msg.body(quote)
                responded = True
            else:

                etp = msgzap.etapa
                # ------------- ETAPA == 2 > EMAIL -------------
                if etp == 2:
                    email_dig = incoming_msg
                    email_exist = False
                    contemarroba = True if re.search('.*@',email_dig) else False
                    quote = ''
                    if email_dig != '' and contemarroba:
                        verificpessoa = pessoas.get_byemailpessoa(email_dig,'AT')
                        if verificpessoa:
                            email_exist = True
                            quote = f'Email Já encontra-se cadastrado na nossa base de dados.\n Forneça  um email válido:'
                    else:
                        quote = f'Email em branco ou inválido.\n Forneça  um email válido:'
                        email_exist = True

                    if not email_exist:
                        pessoa.email = email_dig

                        msgzap.resposta = email_dig

                        msgzap.etapa = 4
                        msgzap.menu = 1
                        msgzap.etapamenu = 'COFIRMATLETA'
                        msgzap.pergunta = f'{"Seu cadastro foi finalizado com sucesso!"}\n'
                        msgtemp = mensagewhatsapp.getmensagewhatsapp_by_phone_idpessoa_null(pessoa.phone)
                        if msgtemp:
                            db.session.delete(msgtemp)

                        db.session.commit()
                        quote = f'{msgzap.pergunta}'
                        quote += f'\n{"Bem vindo "}{pessoa.nome}!\n' \
                                f'{"Deseja cadastar dados  Calórico? Digite:"}\n' \
                                f'{"1 - SIM"}\n' \
                                f'{"2 - Não"}\n' \
                                f'{"0 - Excluir Dados Pessoais"}'
                    else:
                        msgzap.resposta = email_dig
                        msgzap.etapamenu = 'MAIN'
                        msgzap.etapa = 2
                        msgzap.menu = 0
                        db.session.commit()

                    msg.body(quote)
                    responded = True
                # ------------- ETAPA == 4 > CADASTRO FINALIZADO -------------
                if etp == 4:
                    # ETAPA QUE USUARIO CADASTRA SEUS DADOS E FICA AQUI COMO MENU PRINCIPAL
                    etapamenu = msgzap.etapamenu
                    if etapamenu == 'COFIRMATLETA':
                        menu = incoming_msg
                        if menu == '1': # PERMITIU CADASTRAR META CALORICA
                            msgzap.etapa = 5
                            msgzap.menu = 0
                            db.session.commit()
                            quote = f'{"Digite seu peso corporal em Kilogramas:"}'
                        elif menu=='2':
                            msgzap.etapa = 4
                            quote = f'{"Bem vindo "}{pessoa.nome}!\n'
                            quote += return_quote_pai()
                            msgzap.menu = 0
                            msgzap.etapamenu = 'MAINPAI'
                            msgzap.submenu = None
                            db.session.commit()
                        else:
                            pass

                    # MENU PAI
                    if etapamenu == 'MAINPAI':
                        menudig = incoming_msg
                        quote = ''
                        if menudig == '2':
                            msgzap.etapa = 4
                            quote += return_quote_menumain()
                            msgzap.menu = 0
                            msgzap.etapamenu = 'MAIN'
                            msgzap.submenu = None
                            db.session.commit()
                        elif menudig == '1':
                            # AQUI SERÁ A RESPOSTA MENU META CALORICA
                            pass
                        else:
                            quote += return_quote_pai()
                            msgzap.menu = 0
                            msgzap.etapamenu = 'MAINPAI'
                            msgzap.submenu = None
                            db.session.commit()


                    # MENU PRINICIPAL
                    if etapamenu == 'MAIN':
                        menu = incoming_msg
                        quote = ""

                        # Menu Principal
                        if menu == '0':
                            quote = f'{"Bem vindo "}{pessoa.nome}!\n'
                            quote += return_quote_pai()
                            msgzap.menu = 0
                            msgzap.etapamenu = 'MAINPAI'
                            msgzap.submenu = None
                            db.session.commit()

                        # DIGITA 1 == ESCOLHEU MENU TRADUZIR > ETAPA 4
                        elif menu == '1':
                            # SE MENU FOR TRADUZIR(MENU=1) E MANDA USUARIO DIGITAR TEXTO (SUBMENU=1)
                            msgzap.etapamenu = 'TRADUCAO'
                            db.session.commit()
                            quote = f'{"Digite o Texto que deseja traduzir:"}\n'

                        # DIGITOU MENU 2 RASTREAR OBJETOS PELOS CORREIOS
                        elif menu == '2':
                            msgzap.etapamenu = 'TRACKER'
                            db.session.commit()
                            quote = f'{"Digite o código do rastreamento abaixo:"}\n'

                        # DIGITOU MENU 3 BUSCA DADOS LOCALIDADE CEP
                        elif menu == '3':
                            msgzap.etapamenu = 'CEP'
                            db.session.commit()
                            quote = f'{"Digite o CEP que deseja:"}\n'
                        # DIGITOU MENU 4 BUSCA DADOS CLIMATICOS PELO NOME CIDADE E SIGLA UF
                        elif menu == '4':
                            msgzap.etapamenu = 'CLIMA'
                            db.session.commit()
                            quote = f'{"Digite a Cidade,Estado(MG):"}\n'

                        elif not re.search('[0-4]',incoming_msg):
                            msgzap.menu = 1
                            msgzap.etapamenu = 'MAIN'
                            msgzap.submenu = None
                            db.session.commit()
                            quote = f'Não entendemos o que você quer! Forneça o Menu correto!\n'
                            quote += return_quote_menumain()

                    # USUARIO ESCOLHEU TRADUZIR TEXTOS DIGITOU 1
                    if etapamenu == 'TRADUCAO':
                        txttranslate = incoming_msg
                        if txttranslate == '0':
                            msgzap.menu = 1
                            msgzap.etapamenu = 'MAIN'
                            msgzap.submenu = None
                            db.session.commit()
                            quote = return_quote_menumain()
                        else:
                            msgzap.menu = 1
                            db.session.commit()
                            jsontranslate = several.translate(txttranslate)
                            import json
                            jsontranslate = json.loads(jsontranslate)

                            quote = f'{jsontranslate["traducao"]}'
                    # USUARIO ESCOLHEU RASTREAR ENCOMENDAS 2
                    if etapamenu == 'TRACKER':
                        codtrack = incoming_msg
                        if codtrack == '0':
                            msgzap.menu = 1
                            msgzap.etapamenu = 'MAIN'
                            msgzap.submenu = None
                            db.session.commit()
                            quote = return_quote_menumain()
                        else:
                            msgzap.menu = 1
                            db.session.commit()
                            datatrack = several.search_tracker_correios(codtrack)
                            quote = f'{"👇 Resultado - Última Atualização"}\n'
                            if datatrack['tot']>0:
                                datatrack = datatrack['data']
                                if len(datatrack) > 1:
                                    for rowindice in datatrack:
                                        for row in datatrack[rowindice]:
                                            data = datatrack[rowindice][row]
                                            data = re.sub('. Clique aqui Minhas Importações',f' nos sites dos correios:\n' \
                                                          f'{"https://www2.correios.com.br/sistemas/rastreamento/default.cfm?objetos="+codtrack}',data)
                                            #data = re.sub('/','-',data)
                                            quote += f'{data}\n'
                                        break
                                else:
                                    quote += datatrack[0]
                            else:
                                quote += 'Código Inválido ou Objeto ainda não postado'
                    # USUARIO ESCOLHEU BUSCAR CEP DIGITOU 3
                    if etapamenu == 'CEP':
                        codCEP = incoming_msg
                        if codCEP == '0':
                            msgzap.menu = 1
                            msgzap.etapamenu = 'MAIN'
                            msgzap.submenu = None
                            db.session.commit()
                            quote = return_quote_menumain()
                        else:
                            msgzap.menu = 1
                            db.session.commit()
                            import json
                            jsondata = several.busca_dados_CEP(codCEP)
                            erro = False
                            try:
                                erro = jsondata["erro"]
                            except:
                                erro = False

                            if not erro:
                                strcyte = ''
                                quote = f'{"*Resultado:* 👇"}\n\n'
                                quote += f'Cep: {jsondata["cep"]}\n'
                                if jsondata["logradouro"] != '':
                                    quote += f'Rua: {jsondata["logradouro"]}\n'
                                    #strcyte += jsondata["logradouro"]+' '
                                if jsondata["bairro"] != '':
                                    quote += f'Bairro: {jsondata["bairro"]}\n'

                                if jsondata["complemento"] != '':
                                    quote += f'Complemento: {jsondata["complemento"]}\n'
                                if jsondata["localidade"] != '':
                                    quote += f'Cidade: {jsondata["localidade"]}, {jsondata["uf"]}\n'
                                    strcyte += jsondata["localidade"]+', '+jsondata["uf"]
                                if jsondata["ddd"] != '':
                                    quote += f'DDD: {jsondata["ddd"]}, Nº IBGE: {jsondata["ibge"]}\n'

                                #BUSCA LATITUDE E LONGITUDE
                                strcyte +=', BR'
                                location = several.search_latitude_longitude_geolocator(strcyte)
                                lat = ''
                                lon = ''
                                if location != None:
                                    lat = location.raw['lat']
                                    lon = location.raw['lon']
                                    quote += f'Latitude: {lat}, Longitude: {lon}\n'

                                # BUSCA TEMPERATURA
                                quote = return_dados_clima(strcyte,jsondata["localidade"]+', '+jsondata["uf"])
                            else:
                                quote = 'Nenhum dados foi encontrado para o cep digitado: '+ codCEP
                    # USUARIO ESCOLHEU BUSCAR CLIMA DIGITOU 4
                    if etapamenu == 'CLIMA':
                        desccity = incoming_msg
                        if desccity == '0':
                            msgzap.menu = 1
                            msgzap.etapamenu = 'MAIN'
                            msgzap.submenu = None
                            db.session.commit()
                            quote = return_quote_menumain()
                        else:
                            quote =''
                            if len(desccity) > 0:
                                desccity +=', BR'
                                quote = return_dados_clima(desccity,re.sub(', BR',', Brasil',desccity))
                                if quote == '':
                                    quote = f'\nNenhum registro encontrado correspondente a sua cidade.' \
                                            f' Verifique e Tente Novamente!'

                            msgzap.menu = 1
                            db.session.commit()


                    if etapamenu != 'MAIN':
                        quote += f'\n\nDigite 0, caso queira voltar ao Menu anterior'
                    msg.body(quote)
                    responded = True
                if etp == 5:
                    valdig = incoming_msg
                    quote = ''
                    if valdig == '99':
                        msgzap.menu = 1
                        msgzap.etapa = 4
                        msgzap.etapamenu = 'MAIN'
                        msgzap.submenu = None
                        db.session.commit()
                        quote = return_quote_menumain()
                    else:
                        menu = msgzap.menu
                        msgzap.etapa = 5
                        from App.views import atleta
                        atleta = atleta.get_atleta_by_idpessoa(pessoa.id)
                        # captura o peso digitado
                        if menu == 0:
                            if not atleta:
                                from App.funcs.funcs import gera_keyacess
                                keyacess = gera_keyacess()
                                try:
                                    from App.model.atleta import Atleta
                                    atleta = Atleta(username=pessoa.username, name=pessoa.nome, password=keyacess,
                                                    email=pessoa.email,idpessoa=pessoa.id, bloqueado='S',
                                                    keyacess=keyacess, phone=pessoa.phone,
                                                    profilenamephone=pessoa.profilenamephone,peso=valdig)
                                    db.session.add(atleta)
                                except:
                                    pass
                            else:
                                atleta.peso = valdig
                            msgzap.menu = 1
                            quote = f'{"Agora digite sua altura em centímetros(CM):"}'
                        #captura data de nascimento digitada
                        if menu == 1:
                            atleta.altura = valdig
                            msgzap.menu = 2
                            quote = f'Seu Sexo:\n' \
                                    f'Digite 0 para Masculino\n' \
                                    f'Digite 1 para Feminino'

                        if menu == 2:
                            msgzap.menu = 3
                            genero = 'M'
                            if valdig == '1':
                                genero = 'F'
                            atleta.genero = genero

                            quote = f'{"Agora digite sua data de nascimento(dd/mm/aaaa):"}'
                        if menu == 3:
                            try:
                                dia = valdig[0:2]
                                mes = valdig[3:5]
                                ano = valdig[6:10]
                                atleta.dtnascimento = ano+'-'+mes+'-'+dia

                                from App.funcs.funcs import retorna_idade
                                try:
                                    idade = retorna_idade(int(ano),int(mes),int(dia))
                                except:
                                    idade = 0
                                msgzap.etapa = 4
                                msgzap.etapamenu = 'MAIN'
                                msgzap.submenu = None
                                db.session.commit()

                                # enviar email confirmação
                                try:
                                    from App.funcs.funcs import gera_keyacess
                                    keyacess = gera_keyacess()
                                    recipient = []
                                    recipient.append(atleta.email)
                                    from App.views.atleta import sendEmail_verificationacess
                                    envio = sendEmail_verificationacess(recipient, keyacess, atleta.name, atleta.id)
                                except:
                                    envio = False

                                msgidd = "Sua idade é: "+str(idade)+" anos. " if idade > 0 else ''
                                quote = f'\n{msgidd}Cadastro Finalizado\n'
                                if envio:
                                    quote +=f'\nFoi enviado um email para sua caixa de email, verifique para desbloquer o acesso ao sistema\n'
                                quote += return_quote_menumain()
                                msgzapdel = mensagewhatsapp.getmensagewhatsapp_by_phone_idpessoa_null(pessoa.phone)
                                if msgzapdel:
                                    db.session.delete(msgzapdel)
                                    db.session.commit()
                            except:
                                msgzap.etapa = 4
                                msgzap.menu = 1
                                msgzap.etapamenu = 'COFIRMATLETA'

                                db.session.commit()
                                msg.body(quote)
                                quote = f'Erro ao cadastrar dados no banco de dados, tente novamente\n'
                                quote += f'\n{"Bem vindo "}{pessoa.nome}!\n' \
                                        f'{"Deseja cadastar dados  Calórico? Digite:"}\n' \
                                        f'{"1 - SIM"}\n' \
                                        f'{"2 - Não"}\n' \
                                        f'{"0 - Excluir Dados Pessoais"}'

                        db.session.commit()


                    msg.body(quote)
                    responded = True
        else:
            # -------- CONTATO NÃO CADASTRADO NO BD --------
            # busca se ja enviou mesma para o contato algum momento
            msgzap = mensagewhatsapp.getmensagewhatsapp_by_phone(phone)
            if not msgzap:
                #     --------      PRIMEIRA COMUNICAÇÃO     --------
                # Etapa 0 -> Primeira Mensagem


                msgzap = MensageWhatsApp(etapa=0, pergunta=phone, proceed='S',
                                         resposta=namephone)
                db.session.add(msgzap)
                db.session.commit()

                quote = f'{"Seja Bem-Vindo "} {namephone}{", ao SisNutri!"}\n ' \
                        f'{"Deseja cadastrar em nossa base de dados?"}\n{"Digite 1 se SIM"}\n' \
                        f'{"Digite 2 se Não"}'

                msg.body(quote)
                responded = True
            else:
                # ---- CONTATO NÃO CADASTRADO POREM JA COMUNICOU ALGUMA VEZ
                msgtemp = msgzap.etapa

                if msgtemp == 0:
                    # DIGITOU 1, ACEITOU A CADASTRAR NO BD
                    if incoming_msg == '1':
                        from App.model.pessoas.pessoa import Pessoa
                        if namephone == '':
                            namephone = None
                        pessoa = Pessoa(profilenamephone=namephone,tipopessoa='AT',phone=phone,username=namephone)
                        try:
                            db.session.add(pessoa)
                            db.session.commit()
                            quote = f'{"Seja Bem-Vindo"} {namephone}\n {"Digite seu Nome completo:"}'
                            msg.body(quote)
                            responded = True

                        except:
                            quote = f'{"Não foi possível registrar você em nossa base de dados, contate-nos!"}'
                            msg.body(quote)
                            responded = True
                    # DIGITOU 2, Ou outra coisa, Exclui mensagem.
                    else:

                        db.session.delete(msgzap)
                        db.session.commit()
                        quote = f'{"Agradecemos seu contato "} {namephone}\n ' \
                                f'{"Caso mude de idéia, entre em contato conosoco novamente!"}'

                        msg.body(quote)
                        responded = True

        if not responded:
            quote = f'{"Olá não entendi o que vc quer, so conheço citação nesse momento,desculpe"}'
            msg.body(quote)

    return str(resp)