SELECT has_zeramento = 1, date_end = DATE('#')
  FROM bethadba.ctlancto AS lan
 WHERE lan.codi_emp = #
   AND YMD(YEAR(lan.data_lan), MONTH(lan.data_lan), 1) = YMD(YEAR(date_end), MONTH(date_end), 1)
   AND lan.orig_lan = 2
GROUP BY has_zeramento, date_end