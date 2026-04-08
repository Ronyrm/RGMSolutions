SELECT 
    e.dt_ult_cotacao,
    e.id,
    e.papel,e.val_liq_corrent,val_ev_ebitda,
	 e.val_mercado,e.avgvolume, 
    e.`name` AS empresa,
    s.`name` AS setor,
    ss.`name` AS subsetor,
    
    e.val_cotacao AS Preco_Atual,
    preco_garam.val_preco_justo AS Preco_Justo_Garham,
    ROUND(((preco_garam.val_preco_justo - e.val_cotacao) / preco_garam.val_preco_justo) * 100,2) AS Desconto,
    e.val_cotacao,
    e.val_cotacao_anterior,
    e.val_dif_cotacao,
    e.precoatual,
    e.precograham,
    e.lpamedio ,
    e.val_vpa AS  vpa_g,
    ROUND(((e.precograham - e.val_cotacao) / e.precograham) * 100,2) AS DescontoGraham,
    
    e.precobazin,
    e.val_divyeild_12ult_meses,
    ROUND(((e.precobazin - e.val_cotacao) / e.precobazin)  * 100,2) AS Desconto_Bazin,
    
    

    
    
    
   COALESCE(ROUND((LEAST(((preco_garam.val_preco_justo - e.val_cotacao) / preco_garam.val_preco_justo) * 100,50) *0.4) + 
	 (LEAST(e.val_roe,30)*0.3)  + (e.perc_divyield * 0.2),2) +
	 (CASE 
     WHEN e.val_liq_corrent >= 1.5 THEN 5
     WHEN e.val_liq_corrent >= 1.2 THEN 3
     ELSE -2
    END) -
    (CASE 
     WHEN e.val_ev_ebitda > 10 THEN 3
     WHEN e.val_ev_ebitda > 8 THEN 1
     ELSE 0
    END) -
	 (CASE 
     WHEN e.val_p_vp > 3 THEN 3
     WHEN e.val_p_vp > 2 THEN 1
     ELSE 0
    END) +
	 ((((e.precobazin - e.val_cotacao) / e.precobazin)  * 100) * 0.2),2) AS Score,
	 
    e.val_lpa,e.val_vpa, e.val_p_l AS 'p/l', e.val_p_vp,
    e.perc_divyield,
	 e.val_divyield,
   e.val_roe,
   (((preco_garam.val_preco_justo - e.val_cotacao) / preco_garam.val_preco_justo) * 100) AS valorteste,
    
	 case 
	   when ((((preco_garam.val_preco_justo - e.val_cotacao) / preco_garam.val_preco_justo) * 100) >= 40) AND 
           (e.val_roe >= 15) then 'OPORTUNIDADE FORTE'
      When ((((preco_garam.val_preco_justo - e.val_cotacao) / preco_garam.val_preco_justo) * 100) >= 30) AND 
           (e.val_roe >= 12) then 'BOA OPORTUNIDADE'	 
      when ((((preco_garam.val_preco_justo - e.val_cotacao) / preco_garam.val_preco_justo) * 100) >= 20)  
        then 'RAZOÁVEL'
      else 'CARA / EVITAR' 
	end as Classificacao,
      
   
      
    c_primeira.dt_cotacao AS primeira_data_2026,
    COALESCE(c_primeira.val_fechamento, 0) AS primeira_cot_2026,
    c_ultima.dt_cotacao AS ultima_data_2026,
    COALESCE(c_ultima.val_fechamento, 0) AS ultima_cot_2026,
    Round(((c_ultima.val_fechamento - c_primeira.val_fechamento) /  c_primeira.val_fechamento) * 100,2) AS perc_variacao_2026
    
    
FROM empresas_bolsa e
LEFT JOIN (
    SELECT 
        idpapel,
        dt_cotacao,
        val_fechamento,
        ROW_NUMBER() OVER (PARTITION BY idpapel ORDER BY dt_cotacao ASC) rn
    FROM cotacao_prices_history_bolsa
    WHERE EXTRACT(YEAR FROM dt_cotacao) = 2026 AND EXTRACT(month FROM dt_cotacao) = 1
) c_primeira ON c_primeira.idpapel = e.id AND c_primeira.rn = 1 
LEFT JOIN (
    SELECT 
        idpapel,
        dt_cotacao,
        val_fechamento,
        ROW_NUMBER() OVER (PARTITION BY idpapel ORDER BY dt_cotacao DESC) rn
    FROM cotacao_prices_history_bolsa
    WHERE EXTRACT(YEAR FROM dt_cotacao) = 2026 AND EXTRACT(month FROM dt_cotacao) = 3
) c_ultima ON c_ultima.idpapel = e.id AND c_ultima.rn = 1 
LEFT JOIN (
     SELECT e.id,
     ROUND(coalesce(SQRT(22.5 * e.val_lpa * e.val_vpa),0),2) AS val_preco_justo
     FROM empresas_bolsa e
     
) preco_garam on preco_garam.id = e.id
INNER JOIN setores_bolsa s ON s.id = e.idsetor
INNER JOIN sub_setores_bolsa ss ON ss.id =e.idsubsetor
WHERE  e.val_roe>15 AND e.perc_divyield BETWEEN 6 AND 15

/*(e.papel IN ('BBSE3','ITSA4','PETR4','WEGE3','ENGI4','VULC3','SAPR4','RECV3','CXSE3','BRAV3','BBAS3',
'AUAU3','BEEF3','CYRE3','AXIA3','CMIG4','BBDC3','PRIO3','AMER3')) /

HAVING preco_garam.val_preco_justo > 0  
/*AND e.val_divyield > 0 AND desconto > 15*/

ORDER BY SCORE DESC,ss.`name`