SELECT pro.codi_emp, codigo_nota = pro.codi_ent, numero = ent.nume_ent, cli_for = forn.nome_for, chave_nfe = ent.chave_nfe_ent, 
       emissao = ent.ddoc_ent, saida_entrada = ent.dent_ent, codi_pdi = pro.codi_pdi, desc_pdi = procad.desc_pdi, cfop = pro.cfop_mep, 
       qtd = pro.qtde_mep, vunit = pro.valor_unit_mep, vtot = pro.vpro_mep , pro.vipi_mep, pro.bcal_mep, pro.cst_mep, 
       pro.vdes_mep, pro.bicms_mep, pro.bicmsst_mep, pro.aliicms_mep, pro.valor_icms_mep, pro.valor_subtri_mep, 
       pro.vfre_mep, pro.vseg_mep, pro.vdesace_mep,
       --estes dois campos sao apenas pra filtros na hora de deletar dados daquele ano-mes
       yearFilter = #, monthFilter = #

  FROM bethadba.efmvepro AS pro 
       INNER JOIN bethadba.efentradas AS ent 
            ON    ent.codi_emp = pro.codi_emp 
              AND ent.codi_ent = pro.codi_ent 
       INNER JOIN bethadba.effornece AS forn 
            ON    forn.codi_emp = ent.codi_emp 
              AND forn.codi_for = ent.codi_for 
       INNER JOIN bethadba.efprodutos AS procad 
            ON    procad.codi_emp = pro.codi_emp 
              AND procad.codi_pdi = pro.codi_pdi 

 WHERE ent.codi_emp = #
   AND year(ent.ddoc_ent) = #
   AND month(ent.ddoc_ent) = #
ORDER BY pro.codi_emp, pro.codi_ent, pro.nume_mep