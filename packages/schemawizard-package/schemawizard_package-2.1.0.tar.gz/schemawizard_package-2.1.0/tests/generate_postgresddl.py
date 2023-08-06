"""
  Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

obj = schemawiz()

# add any specific known date formats
obj.dt_chker.date_formats.append('%Y/%m/%d')

obj.loadcsvfile('tesla.csv')

postgres_ddl = obj.guess_postgres_ddl()

print('Tablename used in CREATE TABLE statement: ' + obj.lastcall_tablename + '\n')


print(postgres_ddl)

