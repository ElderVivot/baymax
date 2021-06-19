SELECT emp.codi_emp, emp.apel_emp, emp.nome_emp, emp.razao_emp, emp.cgce_emp, emp.tins_emp, emp.stat_emp, emp.dcad_emp, emp.dina_emp,
       emp.dtinicio_emp, emp.dddf_emp, emp.fone_emp, emp.email_emp, emp.i_cnae20, emp.ramo_emp, emp.rleg_emp, emp.esta_emp, 
       par.codi_pad AS codi_emp_plano_contas,
       COALESCE( mun.nome_municipio, '' ) AS nome_municipio_emp,
       COALESCE( vig.rfed_par, 0 ) AS regime_emp,
       COALESCE( CASE WHEN regime_emp IS NULL THEN ''
                      WHEN regime_emp IN (2,4) THEN vig.simplesn_regime_par
                      ELSE federais_regime_par
                 END, 'C' ) AS regime_caixa_emp,       
       ( SELECT LIST( usu.i_usuario )
             FROM bethadba.usconfusuario AS usu
                  INNER JOIN bethadba.usconfempresas AS usuconfemp
                       ON    usuconfemp.tipo = usu.tipo
                         AND usuconfemp.i_confusuario = usu.i_confusuario
            WHERE usu.tipo = 3
              AND emp.codi_emp = usuconfemp.i_empresa
              AND usuconfemp.modulos <> ''
              AND usu.i_confusuario IN ( 16, 19, 36, 67, 72, 113 ) ) AS grupos_contabil,
       ( SELECT COUNT( 1 )
             FROM bethadba.usconfusuario AS usu
                  INNER JOIN bethadba.usconfempresas AS usuconfemp
                       ON    usuconfemp.tipo = usu.tipo
                         AND usuconfemp.i_confusuario = usu.i_confusuario
            WHERE usu.tipo = 3
              AND emp.codi_emp = usuconfemp.i_empresa
              AND usuconfemp.modulos <> ''
              AND usu.i_confusuario IN ( 16, 19, 36, 67, 72, 113 ) ) AS qtd_grupos_contabil,
       competence = DATE('#'),
       ( SELECT count()
           FROM bethadba.geempre AS emp2
          WHERE SUBSTR(emp2.cgce_emp, 1, 8) = SUBSTR(emp.cgce_emp, 1, 8)
            AND ( emp2.dina_emp IS NULL 
                  OR CASE WHEN regime_emp IN (2,4) THEN MONTHS(emp2.dina_emp,11) ELSE MONTHS(emp2.dina_emp,2) END >= competence )
            AND ( emp2.dcad_emp IS NULL OR emp2.dcad_emp <= competence )
            AND emp2.cgce_emp <> ''
            AND emp2.cgce_emp IS NOT NULL ) AS qtd_fiais_e_matriz
  FROM bethadba.geempre AS emp
       LEFT OUTER JOIN bethadba.gemunicipio AS mun
                 ON    mun.codigo_municipio = emp.codigo_municipio
       LEFT OUTER JOIN bethadba.efparametro_vigencia AS vig
                 ON    vig.codi_emp = emp.codi_emp
       LEFT OUTER JOIN bethadba.ctparmto AS par
                 ON    par.codi_emp = emp.codi_emp
 WHERE SUBSTR(emp.cgce_emp, 9, 4) = '0001'
   AND emp.dcad_emp <= competence
   AND ( emp.dina_emp IS NULL
         OR CASE WHEN regime_emp IN (2,4) THEN MONTHS(emp.dina_emp,11) ELSE MONTHS(emp.dina_emp,2) END >= competence )
   AND ( vig.vigencia_par = ( SELECT MAX(vig2.vigencia_par)
                                FROM bethadba.efparametro_vigencia AS vig2
                               WHERE vig2.codi_emp = vig.codi_emp
                                 AND vig2.vigencia_par <= competence )
         OR vig.vigencia_par IS NULL )
ORDER BY emp.codi_emp