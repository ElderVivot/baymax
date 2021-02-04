SELECT emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini = DATE('2019-11-01'), dfin = YMD( YEAR(today()), MONTH(today())+1, 0 ),
       mes = month(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       ano = year(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       comp = YMD(ano, mes, 1),
       tipo = 'SAIDA',
       qtd_notas_operacao = SUM(CASE WHEN YMD(YEAR(sai.ddoc_sai), MONTH(sai.ddoc_sai), 1) = comp AND sai.segi_sai <= 1 THEN 1 ELSE 0 END),
       qtd_notas_operacao_dori = SUM(CASE WHEN YMD(YEAR(sai.dorig_sai), MONTH(sai.dorig_sai), 1) = comp AND sai.segi_sai <= 1 THEN 1 ELSE 0 END)
       
  FROM bethadba.geempre AS emp
       INNER JOIN bethadba.efsaidas AS sai
            ON    sai.codi_emp = emp.codi_emp,
       dbo.rowgenerator AS linha

 WHERE emp.codi_emp = #
   AND linha.row_num <= months( dini, dfin ) + 1
   AND ( YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 ) ), 1 ) BETWEEN dini AND dfin )
GROUP BY emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini, dfin, mes, ano, comp, tipo

UNION ALL

SELECT emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini = DATE('2019-11-01'), dfin = YMD( YEAR(today()), MONTH(today())+1, 0 ),
       mes = month(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       ano = year(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       comp = YMD(ano, mes, 1),
       tipo = 'ENTRADA',
       qtd_notas_operacao = SUM(CASE WHEN YMD(YEAR(ent.data_entrada), MONTH(ent.data_entrada), 1) = comp AND ent.segi_ent <= 1 THEN 1 ELSE 0 END),
       qtd_notas_operacao_dori = SUM(CASE WHEN YMD(YEAR(ent.dorig_ent), MONTH(ent.dorig_ent), 1) = comp AND ent.segi_ent <= 1 THEN 1 ELSE 0 END)
       
  FROM bethadba.geempre AS emp
       INNER JOIN bethadba.efentradas AS ent
            ON    ent.codi_emp = emp.codi_emp,
       dbo.rowgenerator AS linha

 WHERE emp.codi_emp = #
   AND linha.row_num <= months( dini, dfin ) + 1
   AND ( YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 ) ), 1 ) BETWEEN dini AND dfin )
GROUP BY emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini, dfin, mes, ano, comp, tipo

UNION ALL

SELECT emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini = DATE('2019-11-01'), dfin = YMD( YEAR(today()), MONTH(today())+1, 0 ),
       mes = month(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       ano = year(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       comp = YMD(ano, mes, 1),
       tipo = 'SERVICO',
       qtd_notas_operacao = SUM(CASE WHEN YMD(YEAR(ser.dser_ser), MONTH(ser.dser_ser), 1) = comp AND ser.segi_ser <= 1 THEN 1 ELSE 0 END),
       qtd_notas_operacao_dori = SUM(CASE WHEN YMD(YEAR(ser.dorig_ser), MONTH(ser.dorig_ser), 1) = comp AND ser.segi_ser <= 1 THEN 1 ELSE 0 END)
       
  FROM bethadba.geempre AS emp
       INNER JOIN bethadba.efservicos AS ser
            ON    ser.codi_emp = emp.codi_emp,
       dbo.rowgenerator AS linha

 WHERE emp.codi_emp = #
   AND linha.row_num <= months( dini, dfin ) + 1
   AND ( YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 ) ), 1 ) BETWEEN dini AND dfin )
GROUP BY emp.codi_emp, emp.nome_emp, emp.cgce_emp, dini, dfin, mes, ano, comp, tipo

ORDER BY 1, comp