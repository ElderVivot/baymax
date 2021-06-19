SELECT credit = sum(lan.vlor_lan),
       debit = 0
  FROM bethadba.ctlancto AS lan,
       bethadba.ctcontas AS con
 WHERE lan.codi_emp = #
   AND con.codi_emp = #
   AND lan.ccre_lan = con.codi_cta
   AND substr(trim(con.clas_cta), 1, 1) = '#'
   AND lan.data_lan BETWEEN DATE('#') AND DATE('#')

UNION ALL

SELECT credit = 0,
       debit = sum(lan.vlor_lan)
  FROM bethadba.ctlancto AS lan,
       bethadba.ctcontas AS con
 WHERE lan.codi_emp = #
   AND con.codi_emp = #
   AND lan.cdeb_lan = con.codi_cta
   AND substr(trim(con.clas_cta), 1, 1) = '#'
   AND lan.data_lan BETWEEN DATE('#') AND DATE('#')