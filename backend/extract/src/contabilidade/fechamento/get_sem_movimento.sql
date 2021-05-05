SELECT emp.codi_emp,
       dini = DATE('#'),
       dfin = DATE('#'),
       cgce_raiz = SUBSTR(emp.cgce_emp, 1, 8),
       parcta.fechamento_data AS dt_fechamento_contabil,
       parcta.dini_par AS dt_periodo_ini_trabalho,
       parcta.dfin_par AS dt_periodo_fim_trabalho,
       parcta.lant_par AS lan_permitido_fora_trabalho,
       entradas = (SELECT COUNT(*)
                            FROM BETHADBA.EFENTRADAS AS ent
                                 INNER JOIN bethadba.geempre AS emp2
                                      ON    emp2.codi_emp = ent.codi_emp
                           WHERE SUBSTR(emp2.cgce_emp,1,8) = cgce_raiz
                             AND ent.dent_ent BETWEEN dini AND dfin
                             AND ent.SEGI_ENT <= 1  ),
       saidas = (SELECT COUNT(*)
                         FROM BETHADBA.EFSAIDAS AS sai
                                 INNER JOIN bethadba.geempre AS emp2
                                      ON    emp2.codi_emp = sai.codi_emp
                           WHERE SUBSTR(emp2.cgce_emp,1,8) = cgce_raiz
                          AND sai.ddoc_sai BETWEEN dini AND dfin
                          AND sai.SEGI_SAI <= 1),
       servicos = (SELECT COUNT(*)
                          FROM BETHADBA.EFSERVICOS AS ser
                                 INNER JOIN bethadba.geempre AS emp2
                                      ON    emp2.codi_emp = ser.codi_emp
                           WHERE SUBSTR(emp2.cgce_emp,1,8) = cgce_raiz
                           AND ser.ddoc_ser BETWEEN dini AND dfin
                           AND ser.SEGI_SER <= 1 ),
       red_z = (SELECT COUNT(*)
                          FROM bethadba.EFECF_REDUCAO_Z AS red_z
                                 INNER JOIN bethadba.geempre AS emp2
                                      ON    emp2.codi_emp = red_z.codi_emp
                           WHERE SUBSTR(emp2.cgce_emp,1,8) = cgce_raiz
                           AND red_z.data_reducao BETWEEN dini AND dfin),
       total_notas = entradas + saidas + servicos + red_z,
       lan_contabil = (SELECT count(1)
                        FROM bethadba.ctlancto AS lan
                             INNER JOIN bethadba.geempre AS emp2
                                  ON    emp2.codi_emp = lan.codi_emp
                       WHERE SUBSTR(emp2.cgce_emp,1,8) = cgce_raiz
                         AND lan.data_lan BETWEEN dini AND dfin),
         ( SELECT COUNT(*)
             FROM bethadba.fobasesserv AS bas
                  INNER JOIN bethadba.geempre AS emp2
                       ON    emp2.codi_emp = bas.codi_emp
            WHERE SUBSTR(emp2.cgce_emp,1,8) = cgce_raiz
              AND bas.competencia BETWEEN dini AND dfin ) AS calc_folha                                                                  

FROM BETHADBA.GEEMPRE AS emp
     LEFT OUTER JOIN bethadba.ctparmto AS parcta
                  ON     parcta.codi_emp = emp.codi_emp

WHERE emp.codi_emp = #