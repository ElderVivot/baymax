SELECT tab.table_name,
       ( SELECT MAX(1)
           FROM sys.syscolumn AS col 
          WHERE col.table_id = tab.table_id
            AND col.column_name = 'codi_emp' ) AS exist_codi_emp
  FROM sys.SYSTABLE AS tab
 WHERE tab.table_name LIKE 'FO%'
   AND tab.table_type = 'BASE'
ORDER BY tab.table_name