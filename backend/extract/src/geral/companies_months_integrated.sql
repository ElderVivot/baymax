SELECT emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini = DATE('2019-11-01'), dfin = YMD( YEAR(today()), MONTH(today()), 0 ),
       mes = month(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       ano = year(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       comp = YMD(ano, mes, 1),
       ( SELECT COUNT(1)
           FROM bethadba.ctlancto AS lan
          WHERE lan.codi_emp = emp.codi_emp
            AND year(lan.data_lan) = ano
            AND month(lan.data_lan) = mes
            AND lan.codi_usu IN ('ELDER.DIAS', 'MIRLA')
            AND lan.origem_reg = 2 ) AS qtd_por_mes,
       ( SELECT count()
           FROM bethadba.geempre AS emp2
          WHERE SUBSTR(emp2.cgce_emp, 1, 8) = SUBSTR(emp.cgce_emp, 1, 8)
            AND ( emp2.dina_emp IS NULL OR emp2.dina_emp > comp ) ) AS qtd_fiais_e_matriz
  FROM bethadba.geempre AS emp,
       dbo.rowgenerator AS linha
 WHERE ( qtd_por_mes > 0 )
   AND linha.row_num <= months( dini, dfin ) + 1
   AND ( YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 ) ), 1 ) BETWEEN dini AND dfin )
ORDER BY emp.codi_emp, comp