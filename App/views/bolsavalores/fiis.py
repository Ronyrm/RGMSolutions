import pandas as pd
import io
from App import db
from App.model.bolsavalores.fiis import Fiis,ShemaFiis,FiisDataHora
from App.funcs.getFiis_selenium import getFiis_StatusInvest_Selenium
from App.funcs.funcs import FormatStrToFloat


def getFiis(aParams):
    dados = getFiis_StatusInvest_Selenium(aParams)
    if dados.get("sucesso"):
        return salvaFiisNoBD(dados["csv"])
    else:
        return {"sucesso": False, "erro": "Falha ao capturar os fiis"}

def GetValorFiis(rowValor):
    
    if pd.isna(rowValor):
        vRet = None  
        return vRet
    else:
        vRet = FormatStrToFloat(str(rowValor))
        return vRet

def AddFiisDataHora(fii = Fiis):
    from datetime import date,datetime
    from sqlalchemy import and_
    fiiDtHr = FiisDataHora.query.filter(and_(FiisDataHora.ticker==fii.ticker,
                                      FiisDataHora.data_movimentacao==date.today(),
                                      FiisDataHora.data_movimentacao==datetime.now().time()
                                      )).first()
    if fiiDtHr:
        fiiDtHr.ticker = fii.ticker
        fiiDtHr.valor_cotacao = fii.preco
        fiiDtHr.data_movimentacao = date.today()
        fiiDtHr.hora_movimentacao = datetime.now().time()
    else:
        fiiDtHr = FiisDataHora(
            ticker = fii.ticker,
            valor_cotacao = fii.preco,
            data_movimentacao = date.today(),
            hora_movimentacao = datetime.now().time()
        )
        db.session.add(fiiDtHr)
    db.session.commit()


def salvaFiisNoBD(arqCSV):
    poscur = -1
    sucesso = True
    error = ""
    df = pd.read_csv(io.StringIO(arqCSV),sep=";",decimal=",", encoding="utf-8")
    
    for i, row in df.iterrows():
        poscur = i
        try:
            ticker = row['TICKER'].strip()
            fii = Fiis.query.filter_by(ticker=ticker).first()
            if fii:
                fii.preco = GetValorFiis(row['PRECO'])
                fii.ultimo_dividendo = GetValorFiis(row['ULTIMO DIVIDENDO'])
                fii.dy = GetValorFiis(row['DY'])
                fii.valor_patrimonial_cota = GetValorFiis(row['VALOR PATRIMONIAL COTA'])
                fii.p_vp = GetValorFiis(row['P/VP'])
                fii.liquidez_media_diaria =  GetValorFiis(row['LIQUIDEZ MEDIA DIARIA'])
                fii.percentual_caixa = GetValorFiis(row['PERCENTUAL EM CAIXA'])
                fii.cagr_dividendos_3_anos = GetValorFiis(row['CAGR DIVIDENDOS 3 ANOS'])
                fii.cagr_valor_cota_3_anos = GetValorFiis(row[' CAGR VALOR CORA 3 ANOS'])
                fii.patrimonio = GetValorFiis(row['PATRIMONIO'])
                fii.cotistas = GetValorFiis(row['N COTISTAS'])
                fii.gestao =  GetValorFiis(row["GESTAO"])
                fii.n_cotas = GetValorFiis(row[' N COTAS'])
                db.session.commit()
                AddFiisDataHora(fii)
            else:
                # inserir
                fii = Fiis(
                    ticker=ticker,
                    preco=GetValorFiis(row['PRECO']),
                    ultimo_dividendo=GetValorFiis(row['ULTIMO DIVIDENDO']),
                    dy=GetValorFiis(row['DY']),
                    valor_patrimonial_cota=GetValorFiis(row['VALOR PATRIMONIAL COTA']),
                    p_vp=GetValorFiis(row['P/VP']),
                    liquidez_media_diaria=GetValorFiis(row['LIQUIDEZ MEDIA DIARIA']),
                    percentual_caixa=GetValorFiis(row['PERCENTUAL EM CAIXA']),
                    cagr_dividendos_3a=None if pd.isna(row['CAGR DIVIDENDOS 3 ANOS']) else GetValorFiis(row['CAGR DIVIDENDOS 3 ANOS']),
                    cagr_valor_cota_3a=None if pd.isna(row[' CAGR VALOR CORA 3 ANOS']) else GetValorFiis(row[' CAGR VALOR CORA 3 ANOS']),
                    patrimonio=GetValorFiis(row['PATRIMONIO']),
                    n_cotistas=GetValorFiis(row['N COTISTAS']),
                    gestao= None if pd.isna(row["GESTAO"]) else row["GESTAO"],
                    n_cotas= GetValorFiis(row[' N COTAS'])
                )
                db.session.add(fii)
                db.session.commit()
                AddFiisDataHora(fii)
                
           
        except Exception as e:
            sucesso = False
            error = str(e) 
            print('O Erro:'+error)
        if not sucesso:
            break
    if sucesso:
        try:
            print('Salvei no banco') 
            schema = ShemaFiis()
            
            sFiis = schema.dump(Fiis.query.all(),many=True) 
            return {"sucesso":sucesso,"msg":"Executado com sucesso","fiis":sFiis}
        except Exception as e:
            return {"sucesso":False,"msg":"Falha. Error:"+str(e)}



