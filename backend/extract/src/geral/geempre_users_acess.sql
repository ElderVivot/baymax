  SELECT i_confusuario = usu.i_confusuario,
         usua_log = con.usua_log,
         CASE WHEN con.sist_log = 1 THEN 'Contabilidade'
              WHEN con.sist_log = 2 THEN 'Contabilidade Livro Caixa'
              WHEN con.sist_log = 3 THEN 'Honorários'
              WHEN con.sist_log = 4 THEN 'Patrimônio'
              WHEN con.sist_log = 5 THEN 'Fiscal'
              WHEN con.sist_log = 6 THEN 'Lalur'
              WHEN con.sist_log = 7 THEN 'Atualiza'
              WHEN con.sist_log = 8 THEN 'Protocolo'
              WHEN con.sist_log = 9 THEN 'Administrar'
              WHEN con.sist_log = 10 THEN 'Domínio Cliente'
              WHEN con.sist_log = 11 THEN 'Contabilidade Gerencial'
              WHEN con.sist_log = 12 THEN 'Folha'
              WHEN con.sist_log = 13 THEN 'Ponto'
              WHEN con.sist_log = 14 THEN 'Auditoria'
              WHEN con.sist_log = 15 THEN 'Registro'
              WHEN con.sist_log = 19 THEN 'Processos'
              ELSE ''
         END AS nome_modulo,
         SUM( DSDBA.BI_DIF_S( DSDBA.DT_TIMESTAMP( con.data_log, con.tini_log ), DSDBA.DT_TIMESTAMP( con.dfim_log, con.tfim_log ) ) )  AS tempo_total

    FROM bethadba.geloguser AS con
         INNER JOIN bethadba.usconfusuario AS usu
              ON    usu.i_usuario = con.usua_log
    
   WHERE con.codi_emp = #
     AND usu.tipo = 1
     AND YEAR(con.data_log) = #
     AND MONTH(con.data_log) = #
     AND con.sist_log IN (1, 2, 5, 12)

GROUP BY i_confusuario,
         usua_log,
         codi_emp,
         nome_modulo 

ORDER BY codi_emp, nome_modulo, tempo_total DESC, usua_log