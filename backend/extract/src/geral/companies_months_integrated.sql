SELECT emp.codi_emp, emp.nome_emp, emp.cgce_emp, 
       CASE WHEN emp.tins_emp NOT IN (1) THEN emp.cgce_emp ELSE SUBSTR(emp.cgce_emp, 1, 8) END cgce_matriz,
       dini = DATE('2019-11-01'), dfin = YMD( YEAR(today()), MONTH(today())+1, 0 ),
       mes = month(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       ano = year(YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 )), 1 ) ),
       comp = YMD(ano, mes, 1),
       qtd_lan_ti_importado_dlan = SUM(CASE WHEN YMD(YEAR(lan.data_lan), MONTH(lan.data_lan), 1) = comp AND lan.codi_usu IN ('ELDER.DIAS', 'MIRLA', 'AUGUSTO.MACHADO') AND lan.origem_reg = 2 AND lan.orig_lan = 1 AND ( condeb.clas_cta LIKE '111%' OR concre.clas_cta LIKE '111%' ) THEN 1 ELSE 0 END),
       qtd_lan_ti_importado_dori = SUM(CASE WHEN YMD(YEAR(lan.dorig_lan), MONTH(lan.dorig_lan), 1) = comp AND lan.codi_usu IN ('ELDER.DIAS', 'MIRLA', 'AUGUSTO.MACHADO') AND lan.origem_reg = 2 AND lan.orig_lan = 1 AND ( condeb.clas_cta LIKE '111%' OR concre.clas_cta LIKE '111%' ) THEN 1 ELSE 0 END),
       qtd_lan_operacao = SUM(CASE WHEN YMD(YEAR(lan.data_lan), MONTH(lan.data_lan), 1) = comp AND lan.codi_usu NOT IN ('ELDER.DIAS', 'MIRLA', 'AUGUSTO.MACHADO') AND lan.orig_lan = 1 AND ( condeb.clas_cta LIKE '11102%' OR concre.clas_cta LIKE '11102%' OR condeb.clas_cta LIKE '11103%' OR concre.clas_cta LIKE '11103%' ) THEN 1 ELSE 0 END),
       qtd_lan_operacao_dori = SUM(CASE WHEN YMD(YEAR(lan.dorig_lan), MONTH(lan.dorig_lan), 1) = comp AND lan.codi_usu NOT IN ('ELDER.DIAS', 'MIRLA', 'AUGUSTO.MACHADO') AND lan.orig_lan = 1 AND ( condeb.clas_cta LIKE '11102%' OR concre.clas_cta LIKE '11102%' OR condeb.clas_cta LIKE '11103%' OR concre.clas_cta LIKE '11103%' ) THEN 1 ELSE 0 END)
       
  FROM bethadba.geempre AS emp
       INNER JOIN bethadba.ctlancto AS lan
            ON    lan.codi_emp = emp.codi_emp
       LEFT JOIN bethadba.ctcontas AS condeb
           ON    condeb.codi_emp = lan.codi_emp
             AND condeb.codi_cta = lan.cdeb_lan
       LEFT JOIN bethadba.ctcontas AS concre
           ON    concre.codi_emp = lan.codi_emp
             AND concre.codi_cta = lan.ccre_lan,
       dbo.rowgenerator AS linha

 WHERE emp.codi_emp = #
   AND linha.row_num <= months( dini, dfin ) + 1
   AND ( YMD( Year(months(dini, linha.row_num -1 )), month(months(dini, linha.row_num -1 ) ), 1 ) BETWEEN dini AND dfin )
GROUP BY emp.codi_emp, emp.nome_emp, emp.cgce_emp, cgce_matriz, dini, dfin, mes, ano, comp
ORDER BY emp.codi_emp, comp