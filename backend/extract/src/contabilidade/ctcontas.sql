SELECT par.codi_emp, con.codi_cta, con.nome_cta, con.clas_cta, con.tipo_cta, con.grdre_cta, con.data_cta,
       con.situacao_cta

  FROM bethadba.ctparmto AS par
       LEFT OUTER JOIN bethadba.ctcontas AS con
                 ON    con.codi_emp = CASE WHEN par.codi_pad IS NOT NULL THEN par.codi_pad ELSE par.codi_emp END
                   
 WHERE par.codi_emp = #

ORDER BY par.codi_emp, con.codi_cta