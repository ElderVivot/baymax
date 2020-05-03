SELECT lan.codi_emp, lan.fili_lan, lan.codi_lote, lan.nume_lan, lote.tipo, lan.data_lan, lan.vlor_lan,
       lan.cdeb_lan, nome_cta_deb = con_deb.nome_cta, clas_cta_deb = con_deb.clas_cta,
       lan.ccre_lan, nome_cta_cre = con_cre.nome_cta, clas_cta_cre = con_cre.clas_cta,
       lan.codi_his, lan.chis_lan, lan.codi_usu, lan.orig_lan, lan.origem_reg, lan.dorig_lan,
       --estes dois campos sao apenas pra filtros na hora de deletar dados daquele ano-mes
       yearFilter = #, monthFilter = #

  FROM bethadba.ctlancto AS lan
       INNER JOIN bethadba.ctlanctolote AS lote
            ON    lote.codi_emp = lan.codi_emp
              AND lote.codi_lote = lan.codi_lote
       INNER JOIN bethadba.ctparmto AS par
            ON    par.codi_emp = lan.codi_emp
       LEFT OUTER JOIN bethadba.ctcontas AS con_deb
                 ON    con_deb.codi_emp = CASE WHEN par.codi_pad IS NOT NULL THEN par.codi_pad ELSE par.codi_emp END
                   AND con_deb.codi_cta = lan.cdeb_lan
       LEFT OUTER JOIN bethadba.ctcontas AS con_cre
                 ON    con_cre.codi_emp = CASE WHEN par.codi_pad IS NOT NULL THEN par.codi_pad ELSE par.codi_emp END
                   AND con_cre.codi_cta = lan.ccre_lan

 WHERE lan.codi_emp = #
   AND year(lan.data_lan) = #
   AND month(lan.data_lan) = #

ORDER BY lan.codi_emp, lan.codi_lote, lan.nume_lan