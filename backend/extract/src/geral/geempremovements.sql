SELECT emp.codi_emp,
       dini = YMD(YEAR(today()), MONTH(today()) - 3, 1),
       dfin = YMD(YEAR(today()), MONTH(today()), 0),
       lan_manual = COALESCE(( SELECT SUM( CASE WHEN lote.tipo = 'X' THEN 1
                                       ELSE 0.5
                                  END )
                          FROM bethadba.ctlancto AS l
                               INNER JOIN bethadba.ctlanctolote AS lote
                                    ON    lote.codi_emp = l.codi_emp
                                      AND lote.codi_lote = l.codi_lote 
                         WHERE l.CODI_EMP = emp.CODI_EMP
                           AND l.dorig_lan BETWEEN dini AND dfin
                           AND l.orig_lan IN (1)
                           AND l.origem_reg = 0 ), 0),
       lan_importado = COALESCE(( SELECT SUM( CASE WHEN lote.tipo = 'X' THEN 1
                                       ELSE 0.5
                                  END )
                          FROM bethadba.ctlancto AS l
                               INNER JOIN bethadba.ctlanctolote AS lote
                                    ON    lote.codi_emp = l.codi_emp
                                      AND lote.codi_lote = l.codi_lote 
                         WHERE l.CODI_EMP = emp.CODI_EMP
                           AND l.dorig_lan BETWEEN dini AND dfin
                           AND l.orig_lan IN (1)
                           AND l.origem_reg = 2 ), 0),
       entradas_manual = (SELECT COUNT(*)
                            FROM BETHADBA.EFENTRADAS AS ent 
                           WHERE ent.CODI_EMP = emp.CODI_EMP
                             AND ent.dent_ent BETWEEN dini AND dfin
                             AND ent.SEGI_ENT <= 1
                             AND ent.origem_reg = 0 ),
       entradas_importada = (SELECT COUNT(*)
                            FROM BETHADBA.EFENTRADAS AS ent 
                           WHERE ent.CODI_EMP = emp.CODI_EMP 
                             AND ent.dent_ent BETWEEN dini AND dfin
                             AND ent.SEGI_ENT <= 1
                             AND ent.origem_reg <> 0 ),
       entradas = entradas_manual + entradas_importada,
       saidas_manual = (SELECT COUNT(*)
                         FROM BETHADBA.EFSAIDAS AS sai 
                        WHERE sai.CODI_EMP =  emp.CODI_EMP 
                          AND sai.dsai_sai BETWEEN dini AND dfin
                          AND sai.SEGI_SAI <= 1
                          AND sai.origem_reg = 0 ),
       saidas_importada = (SELECT COUNT(*)
                         FROM BETHADBA.EFSAIDAS AS sai 
                        WHERE sai.CODI_EMP =  emp.CODI_EMP 
                          AND sai.dsai_sai BETWEEN dini AND dfin
                          AND sai.SEGI_SAI <= 1
                          AND sai.origem_reg <> 0 ),
       saidas = saidas_manual + saidas_importada,
       servicos_manual = (SELECT COUNT(*)
                          FROM BETHADBA.EFSERVICOS AS ser 
                         WHERE ser.CODI_EMP =  emp.CODI_EMP
                           AND ser.dser_ser BETWEEN dini AND dfin
                           AND ser.SEGI_SER <= 1
                           AND ser.origem_reg = 0 ),
       servicos_importada = (SELECT COUNT(*)
                          FROM BETHADBA.EFSERVICOS AS ser 
                         WHERE ser.CODI_EMP =  emp.CODI_EMP
                           AND ser.dser_ser BETWEEN dini AND dfin
                           AND ser.SEGI_SER <= 1
                           AND ser.origem_reg <> 0 ),
       servicos = servicos_manual + servicos_importada,
       COALESCE( ( SELECT SUM( DSDBA.BI_DIF_S( DSDBA.DT_TIMESTAMP( loguser.data_log, loguser.TINI_LOG ), DSDBA.DT_TIMESTAMP( loguser.DFIM_LOG, loguser.TFIM_LOG ) ))
                     FROM BETHADBA.GELOGUSER AS loguser 
                    WHERE loguser.codi_emp = emp.codi_emp
                      and YMD( year(loguser.data_log), month(loguser.data_log), 1 ) BETWEEN dini AND dfin
			                AND loguser.sist_log IN (1) ), 0) AS tempo_acesso_contabil,
       COALESCE( ( SELECT SUM( DSDBA.BI_DIF_S( DSDBA.DT_TIMESTAMP( loguser.data_log, loguser.TINI_LOG ), DSDBA.DT_TIMESTAMP( loguser.DFIM_LOG, loguser.TFIM_LOG ) ))
                     FROM BETHADBA.GELOGUSER AS loguser 
                    WHERE loguser.codi_emp = emp.codi_emp
                      and YMD( year(loguser.data_log), month(loguser.data_log), 1 ) BETWEEN dini AND dfin
			                AND loguser.sist_log IN (5) ), 0) AS tempo_acesso_fiscal,
       ( SELECT LIST( usu.i_usuario )
             FROM bethadba.usconfusuario AS usu
                  INNER JOIN bethadba.usconfempresas AS usuconfemp
                       ON    usuconfemp.tipo = usu.tipo
                         AND usuconfemp.i_confusuario = usu.i_confusuario
            WHERE usu.tipo = 3
              AND emp.codi_emp = usuconfemp.i_empresa
              AND usuconfemp.modulos <> ''
              AND usu.i_confusuario IN ( 16, 19, 36, 67, 72 ) ) AS grupos_contabil,
       ( SELECT LIST( usu.i_usuario )
             FROM bethadba.usconfusuario AS usu
                  INNER JOIN bethadba.usconfempresas AS usuconfemp
                       ON    usuconfemp.tipo = usu.tipo
                         AND usuconfemp.i_confusuario = usu.i_confusuario
            WHERE usu.tipo = 3
              AND emp.codi_emp = usuconfemp.i_empresa
              AND usuconfemp.modulos <> ''
              AND usu.i_confusuario IN ( 8, 9, 36, 66, 72 ) ) AS grupos_fiscal
       
  FROM bethadba.geempre AS emp
  
 WHERE emp.codi_emp = #