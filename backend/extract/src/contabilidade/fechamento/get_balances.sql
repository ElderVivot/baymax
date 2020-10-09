SELECT credit = sum(lan.vlor_lan),
       debit = 0,
       has_zeramento = 0
  FROM bethadba.ctlancto AS lan 
       INNER JOIN bethadba.ctparmto AS par 
            ON    par.codi_emp = lan.codi_emp,
       bethadba.ctcontas AS con
 WHERE lan.codi_emp = #
   AND CASE WHEN par.codi_pad IS NULL THEN par.codi_emp ELSE par.codi_pad END = con.codi_emp
   AND lan.ccre_lan = con.codi_cta
   AND substr(trim(con.clas_cta), 1, 1) = '#'
   AND lan.data_lan <= DATE('#')

UNION ALL

SELECT credit = 0,
       debit = sum(lan.vlor_lan),
       has_zeramento = 0
  FROM bethadba.ctlancto AS lan 
       INNER JOIN bethadba.ctparmto AS par 
            ON    par.codi_emp = lan.codi_emp,
       bethadba.ctcontas AS con
 WHERE lan.codi_emp = #
   AND CASE WHEN par.codi_pad IS NULL THEN par.codi_emp ELSE par.codi_pad END = con.codi_emp
   AND lan.cdeb_lan = con.codi_cta
   AND substr(trim(con.clas_cta), 1, 1) = '#'
   AND lan.data_lan <= DATE('#')