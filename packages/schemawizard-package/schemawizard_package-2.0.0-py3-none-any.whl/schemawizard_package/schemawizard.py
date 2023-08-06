"""
  Dave Skura, 2023
"""
import datetime 
import os
import sys
from postgresdave_package.postgresdave import db 


class dater:
	def __init__(self,date_to_check=''):
		self.local_db = db()
		self.connect_local_db()
		self.date_formats = ['YYYYMMDD','YYYY/MM/DD','YYYY-MM-DD','YYYY-DD-MM']
		self.date_to_check = date_to_check 
		if date_to_check != '':
			self.chk_date(date_to_check)

	def ask_for_database_details(self):
		DB_HOST = input('DB_HOST (localhost): ') or 'localhost'
		DB_PORT = input('DB_PORT (1532): ') or '1532'
		DB_NAME = input('DB_NAME (postgres): ') or 'postgres'
		DB_USERNAME = input('DB_USERNAME (postgres): ') or 'postgres'
		DB_SCHEMA = input('DB_SCHEMA (public): ') or 'public'
		DB_USERPWD = input('DB_USERPWD: ') or '4165605869'
		self.local_db.useConnectionDetails(DB_USERNAME,DB_USERPWD,DB_HOST,DB_PORT,DB_NAME,DB_SCHEMA)
		ans_save_connection_details = input('Save connection details (Y) ? ') or 'Y'
		if ans_save_connection_details == 'Y':
			f = open('.schemawiz_config','w')
			f.write(DB_USERNAME + ' - ' + DB_USERPWD + ' - ' + DB_HOST + ' - ' + DB_PORT + ' - ' + DB_NAME + ' - ' + DB_SCHEMA)
			f.close()

	def connect_local_db(self):
		try:
			f = open('.schemawiz_config','r')
			config_line = f.read() 
			f.close()
			dbsettings = config_line.split(' - ')
			DB_USERNAME = dbsettings[0]
			DB_USERPWD = dbsettings[1]
			DB_HOST = dbsettings[2]
			DB_PORT = dbsettings[3]
			DB_NAME = dbsettings[4]
			DB_SCHEMA = dbsettings[5]
			self.local_db.useConnectionDetails(DB_USERNAME,DB_USERPWD,DB_HOST,DB_PORT,DB_NAME,DB_SCHEMA)
		except:
			self.ask_for_database_details()


	def chk_date(self,possible_date_str):
		print (" Checking date " + possible_date_str) # 
		self.date_type = self.match_date_type(possible_date_str)

		if self.date_type == -1:
			print('Not a date. date_type = ' + str(self.date_type))
		else:
			print('Is a date, and matchs date_type ' + str(self.date_type) + ', ' + self.date_formats[self.date_type])

		return self.date_type

	def chk_date_format_old(self,date_string,date_format):
		try:
			dateObject = datetime.datetime.strptime(date_string, date_format)
			return True
		except ValueError:
			return False

	# -1 means no matching date format
	# > -1 means the date format matches self.date_formats[return_value]
	def match_date_type(self,date_string):	
		for i in range(0,len(self.date_formats)):
			if self.chk_sql_date_format(date_string,self.date_formats[i]):
				return i
		return -1

	def chk_sql_date_format(self,date_string,date_format):
		
		sql = """
			SELECT CASE 
				WHEN '""" + date_string + """' = to_char(to_date('""" + date_string + """','""" + date_format + """'),'""" + date_format + """') THEN '""" + date_format + """'
				else ''
				END as fmt
		"""

		try:
			return_fmt = self.local_db.queryone(sql)
			if return_fmt.strip() =='':
				return False
			else:
				return True
		except Exception as e:
			return False
		
class schemawiz:	
	def __init__(self,csvfilename=''):
		self.version=2.0
		self.dt_chker = dater()
		self.force_delimiter = ''
		self.lastcall_tablename = ''
		self.delimiter = ''
		self.logging_on = False
		self.SomeFileContents = []
		self.column_names = []
		self.column_datatypes = []
		self.BigQuery_datatypes = []
		self.column_sample = []
		self.column_dateformats = []
		self.analyzed	 = False
		self.IsaDateField = False
		self.DateField = ''
		self.clusterField1 = ''
		self.clusterField2 = ''
		self.clusterField3 = ''

		self.csvfilename = ''
		if csvfilename != '':
			self.loadcsvfile(csvfilename)

	def lastcall_delimiter(self):
		return self.delimiter

	def utf8len(self,s):
			return len(s.encode('utf-8'))

	def logger(self,logline):
		if self.logging_on:
			print(logline)

	def loadcsvfile(self,csvfilename):
		if csvfilename != '':
			try:
				f = open(csvfilename,'r')
				f.close()
				self.csvfilename = csvfilename
				self.analyze_csvfile()
			except Exception as e:
				print('Cannot read file: ' + csvfilename)
				sys.exit(0)

		else:
				print('schemawiz.loadcsvfile(csvfilename) requires a valid csv file.')
				sys.exit(0)

	def analyze_csvfile(self):
		self.analyzed = False
		if self.csvfilename == '':
			print('/* No csvfilename was provided to schemawiz.loadcsvfile().  Will use empty template */\n')
			self.SomeFileContents.append('field1,field2,field3,field4,field5')
			self.SomeFileContents.append('1999/02/18,0,0.001,textD,textE')
			self.get_column_names()
			self.get_column_types()
			self.analyzed = True


		else:

			try:
				self.logger('Checking file size for ' + self.csvfilename + '\n')
				file_stats = os.stat(self.csvfilename)

				linecount = 0
				total_linesize = 0
				with open(self.csvfilename) as f:
					for line in f:
						linecount += 1
						if linecount != 1:
							total_linesize += self.utf8len(line)
						if linecount == 11:
							self.datalinesize = total_linesize/10

						self.SomeFileContents.append(line)
				
				#self.logger('file has ' + str(len(self.SomeFileContents)) + ' lines')
				#self.logger('line size is ' + str(self.datalinesize) + ' ytes')
				#self.logger('file size is ' + str(file_stats.st_size) + ' bytes')

				self.get_column_names()
				self.get_column_types()
				self.analyzed = True
			except Exception as e:
			
				print(str(e))
				sys.exit(0)

	def get_just_filename(self):
		justfilename=''
		if self.csvfilename.find('\\') > -1: # have a path and dirs
			fileparts = self.csvfilename.split('\\')
			justfilename = fileparts[len(fileparts)-1]
		else:
			if self.csvfilename != '':
				justfilename = self.csvfilename

		return justfilename

	def gettablename(self):

		now = (datetime.datetime.now())
		rando_tablename= 'tblcsv_' + str(now.year) + ('0' + str(now.month))[-2:] + str(now.day) + str(now.hour) + str(now.minute) 

		return rando_tablename

	def count_chars(self,data,exceptchars=''):
		chars_in_hdr = {}
		for i in range(0,len(data)):
			if data[i] != '\n' and exceptchars.find(data[i]) == -1:
				if data[i] in chars_in_hdr:
					chars_in_hdr[data[i]] += 1
				else:
					chars_in_hdr[data[i]] = 1
		return chars_in_hdr

	def count_alpha(self,alphadict):
		count = 0
		for ch in alphadict:
			if 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def count_nbr(self,alphadict):
		count = 0
		for ch in alphadict:
			if '0123456789'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def count_decimals(self,alphadict):
		count = 0
		for ch in alphadict:
			if '.'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def get_datatype(self,datavalue):
		chardict = {}
		data = ''
		if datavalue[0:1] == '"' and datavalue[-1:] == '"':
			#self.logger('enclosed in quotes ""')
			data = datavalue[1:-1]
			#self.logger('data: ' + data)
		else:
			data = datavalue.strip()

		chardict = self.count_chars(data)
		#self.logger(chardict)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		deccount = self.count_decimals(chardict)

		#self.logger('alpha count : ' + str(alphacount))
		#self.logger('numeric count : ' + str(nbrcount))
		#self.logger('decimal count : ' + str(deccount))

		lookslike = ''
		date_format_nbr = self.dt_chker.match_date_type(data)
		dtformat = ''

		if date_format_nbr != -1:
			lookslike = 'date' 
			dtformat = self.dt_chker.date_formats[date_format_nbr] 

		elif alphacount == 0 and deccount == 1:
			# 123.123232222
			lookslike = 'numeric'

		elif alphacount == 0 and deccount == 0:
			# 123
			lookslike = 'integer'

		else:
			lookslike = 'text'

		return lookslike,dtformat

	def get_column_types(self):
		found_datatypes = {}
		found_datavalues = {}
		found_datefomat = {}
		for i in range(1,len(self.SomeFileContents)):
			dataline = self.SomeFileContents[i].strip().split(self.delimiter)
			#print(dataline)
			for j in range(0,len(dataline)):

				thisdatatype,dtformat = self.get_datatype(dataline[j])
				if self.column_names[j] not in found_datatypes:
					found_datatypes[self.column_names[j]] = thisdatatype
					found_datavalues[self.column_names[j]] = dataline[j]
					found_datefomat[self.column_names[j]]	= dtformat
				else:
					if found_datatypes[self.column_names[j]] == 'date' and thisdatatype =='date' and found_datefomat[self.column_names[j]] != dtformat:
						found_datatypes[self.column_names[j]] == 'text'
					elif found_datatypes[self.column_names[j]] != thisdatatype:
						if found_datatypes[self.column_names[j]] == 'text' or thisdatatype == 'text':
							found_datatypes[self.column_names[j]] == 'text'
						elif found_datatypes[self.column_names[j]] == 'numeric' or thisdatatype == 'numeric':
							found_datatypes[self.column_names[j]] == 'numeric'
						elif found_datatypes[self.column_names[j]] == 'date' or thisdatatype == 'date':
							found_datatypes[self.column_names[j]] == 'text'


		for k in range(0,len(self.column_names)):
			self.column_datatypes.append(found_datatypes[self.column_names[k]])
			self.column_sample.append(found_datavalues[self.column_names[k]].replace('"',''))
			self.column_dateformats.append(found_datefomat[self.column_names[k]])
			self.BigQuery_datatypes.append(self.translate_dt('BigQuery',found_datatypes[self.column_names[k]]))
			if not self.IsaDateField and self.translate_dt('BigQuery',found_datatypes[self.column_names[k]]) == 'DATE': 		
				self.IsaDateField = True
				self.DateField = self.column_names[k]
			elif self.translate_dt('BigQuery',found_datatypes[self.column_names[k]]) != 'FLOAT64':
				if self.clusterField1 == '':
					self.clusterField1 = self.column_names[k]
				elif self.clusterField2 == '':
					self.clusterField2 = self.column_names[k]
				elif self.clusterField3 == '':
					self.clusterField3 = self.column_names[k]

		for m in range(0,len(self.column_datatypes)):
			self.logger('column ' + self.column_names[m] + ' has data type ' + self.column_datatypes[m])

	def translate_dt(self,targettype,postgres_datatype):
		if postgres_datatype.lower().strip() == 'text':
			return 'STRING'
		elif postgres_datatype.lower().strip() == 'date':
			return 'DATE'
		elif postgres_datatype.lower().strip() == 'integer':
			return 'INT64'
		elif postgres_datatype.lower().strip() == 'numeric':
			return 'FLOAT64'
		else:
			return 'UNKNOWN'

	def clean_text(self,ptext): # remove optional double quotes
		text = ptext.strip()
		if (text[:1] == '"' and text[-1:] == '"'):
			return text[1:-1]
		else:
			return text

	def clean_column_name(self,col_name):

		new_column_name = col_name
		chardict = self.count_chars(col_name)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		if ((len(col_name)-2) == (alphacount + nbrcount)) and '1234567890'.find(col_name[:1]) == -1:
			new_column_name = self.clean_text(col_name) # .replace('"','').strip()


		return new_column_name

	def get_column_names(self):
		self.delimiter = self.GuessDelimiter()
		self.logger('file delimiter is ' + self.delimiter)
		self.column_names = self.SomeFileContents[0].strip().split(self.delimiter)
		self.logger('Column Names are ' + str(self.column_names))

		for i in range(0,len(self.column_names)):
			self.column_names[i] = self.clean_column_name(self.column_names[i])

	def GuessDelimiter(self):
		if self.force_delimiter != '':
			delimiter_guess = self.force_delimiter
		else:
			hdrs = self.SomeFileContents[0]
			chars_in_hdr = {}
			chars_in_hdr = self.count_chars(hdrs,"'"+ 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"')

			currentchar = 'no idea'
			currentvalue = 0
			for ch in chars_in_hdr:
				if chars_in_hdr[ch] > currentvalue:
					currentchar = ch
					currentvalue = chars_in_hdr[ch]

			delimiter_guess = currentchar

		return delimiter_guess

	def guess_BigQueryExternal_ddl(self,useproject='',usedataset='',usetablename=''):

		if useproject == '':
			project = 'schemawiz-123'
		else:
			project = useproject

		if usedataset == '':
			dataset = 'sampledataset'
		else:
			dataset = usedataset

		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		project = project.replace(' ','').lower()
		dataset = dataset.replace(' ','').lower()
		tablename = tablename.replace(' ','').lower()
		
		if not self.analyzed:
			self.analyze_csvfile()

		sql = 'CREATE EXTERNAL TABLE IF NOT EXISTS `' + project + '.' + dataset + '.' + tablename + '` (\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.BigQuery_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ' 
			
			if self.column_datatypes[i].strip().lower() == 'date':
				sql += "OPTIONS (description='dateformat in csv [" + self.column_dateformats[i] + "]')"

			sql += ',\n'

		sql = sql[:-2] + '\n)'
		
		sql += " OPTIONS (\n    format = 'CSV',\n    Field_delimiter = '" + self.delimiter  + "',\n    uris = ['gs://bucket/" 
		sql += self.get_just_filename() + "*'],\n    skip_leading_rows = 1,\n    "
		sql += "description='" + "This externally stored, BigQuery table was defined by schemawiz for creating a BQ table to use csv files as source.'\n);"


		return sql

	def guess_BigQuery_ddl(self,useproject='',usedataset='',usetablename=''):

		if useproject == '':
			project = 'schemawiz-123'
		else:
			project = useproject

		if usedataset == '':
			dataset = 'sampledataset'
		else:
			dataset = usedataset

		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		project = project.replace(' ','').lower()
		dataset = dataset.replace(' ','').lower()
		tablename = tablename.replace(' ','').lower()
		
		if not self.analyzed:
			self.analyze_csvfile()

		sql = 'CREATE TABLE IF NOT EXISTS `' + project + '.' + dataset + '.' + tablename + '` (\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.BigQuery_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ' 
			
			if self.column_datatypes[i].strip().lower() == 'date':
				sql += "OPTIONS (description='dateformat in csv [" + self.column_dateformats[i] + "]')"

			sql += ',\n'


		sql = sql[:-2] + '\n)\n'
		
		if self.IsaDateField:
			sql += 'PARTITION BY ' + self.DateField + '\n'
		
		if self.clusterField1 != '':
			sql += 'CLUSTER BY \n    ' + self.clusterField1 + ',\n'

		if self.clusterField2 != '':
			sql += '    ' + self.clusterField2 + ',\n'

		if self.clusterField3 != '':
			sql += '    ' + self.clusterField3 + ',\n'

		sql = sql[:-2]

		sql += "\nOPTIONS (\n    require_partition_filter = False,\n    "
		sql += "description = 'This BigQuery table was defined by schemawiz for loading the csv file " + self.get_just_filename() + ", delimiter= " + self.delimiter + "' \n);"
    
		return sql

	def guess_postgres_ddl(self,usetablename=''):

		if not self.analyzed:
			self.analyze_csvfile()
		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		fldcommentsql = '' 

		sql = 'CREATE TABLE IF NOT EXISTS ' + tablename + '(\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.column_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'
			if self.column_datatypes[i].strip().lower() == 'date':
				fldcommentsql += 'COMMENT ON COLUMN ' + tablename + '.' + self.column_names[i] + " IS 'dateformat in csv [" + self.column_dateformats[i] + "]';\n"
		sql = sql[:-2] + '\n);\n\n'
		sql += 'COMMENT ON TABLE ' + tablename + " IS 'This Postgres table was defined by schemawiz for loading the csv file " + self.csvfilename + ", delimiter= " + self.delimiter + "';\n"
		sql += fldcommentsql

		return sql

	def guess_mysql_ddl(self,usetablename=''):
		if not self.analyzed:
			self.analyze_csvfile()
		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename
		self.lastcall_tablename = tablename

		sql = 'CREATE TABLE IF NOT EXISTS ' + tablename + '(\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.column_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ '
			if self.column_datatypes[i].strip().lower() == 'date':
				sql += 'COMMENT "dateformat in csv [' + self.column_dateformats[i] + ']" '
			sql += ' ,\n'

		sql = sql[:-2] + '\n) \n'
		
		sql += 'COMMENT="This MySQL table was defined by schemawiz for loading the csv file ' + self.csvfilename + ', delimiter= ' + self.delimiter + '"; \n'

		return sql


if __name__ == '__main__':
	csvfilename = 'tesla.csv' #input('csvfile to read? ')

	obj = schemawiz()

	# add any specific known date formats
	obj.dt_chker.date_formats.append('Mon DD,YY')
	if csvfilename != '':
		obj.loadcsvfile(csvfilename)

	print('/* BigQuery External DDL - BEGIN ----- schemawiz().guess_BigQueryExternal_ddl() ----- */ \n')
	print(obj.guess_BigQueryExternal_ddl('watchful-lotus-364517','dave'))
	print('\n/* BigQuery External DDL - END   ----- ----- ----- ----- */ \n')

	print('/* BigQuery DDL - BEGIN ----- schemawiz().guess_BigQuery_ddl() ----- */ \n')
	print(obj.guess_BigQuery_ddl('watchful-lotus-364517','dave'))
	print('\n/* BigQuery DDL - END   ----- ----- ----- ----- */ \n')

	print('/* MySQL DDL - BEGIN ----- schemawiz().guess_mysql_ddl() ----- */ \n')
	print(obj.guess_mysql_ddl())
	print('/* MySQL DDL - END   ----- ----- ----- ----- */ \n')

	print('/* Postgres DDL - BEGIN ----- schemawiz().guess_postgres_ddl() ----- */ \n')
	ddl = obj.guess_postgres_ddl('tesla_csv')
	print('/* Tablename used : ' + obj.lastcall_tablename + ' */ \n')
	print(ddl)
	print('/* Postgres DDL - END   ----- ----- ----- ----- */ \n')


