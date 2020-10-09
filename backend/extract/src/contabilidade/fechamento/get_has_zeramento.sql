SELECT has_zeramento = 1
  FROM bethadba.ctlancto AS lan
 WHERE lan.codi_emp = #
   AND lan.data_lan = DATE('#')
   AND lan.orig_lan = 2
GROUP BY has_zeramento