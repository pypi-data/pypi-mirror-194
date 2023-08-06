"""
  Dave Skura, 2023
"""
from datetime import *
import os
import sys

class schemawiz:	
	def __init__(self,csvfilename=''):
		self.version=1.0
		self.force_delimiter = ''
		self.lastcall_tablename = ''
		self.delimiter = ''
		self.logging_on = False
		self.SomeFileContents = []
		self.column_names = []
		self.column_datatypes = []
		self.BigQuery_datatypes = []
		self.column_sample = []
		self.analyzed	 = False
		self.IsaDateField = False
		self.DateField = ''
		self.clusterField1 = ''
		self.clusterField2 = ''
		self.clusterField3 = ''

		self.csvfilename = ''
		if csvfilename != '':
			self.loadcsvfile(csvfilename)

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
			self.SomeFileContents.append('0000/00/00,textB,textC,textD,textE')
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

		now = (datetime.now())
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
		# check for simple date with / delimiter
		if '/' in chardict and ':' not in chardict and '.' not in chardict and '-' not in chardict and '\\' not in chardict:
			if chardict['/'] == 2 and alphacount == 0:
				# 2018/10/15
				lookslike = 'date'
			else:
				self.logger('too many /')
				lookslike = 'unknown'

		elif alphacount == 0 and deccount == 1:
			# 123.123232222
			lookslike = 'numeric'

		elif alphacount == 0 and deccount == 0:
			# 123
			lookslike = 'integer'

		else:
			lookslike = 'text'

		return lookslike

	def get_column_types(self):
		found_datatypes = {}
		found_datavalues = {}
		for i in range(1,len(self.SomeFileContents)):
			dataline = self.SomeFileContents[i].strip().split(self.delimiter)
			#print(dataline)
			for j in range(0,len(dataline)):

				thisdatatype = self.get_datatype(dataline[j])
				if self.column_names[j] not in found_datatypes:
					found_datatypes[self.column_names[j]] = thisdatatype
					found_datavalues[self.column_names[j]] = dataline[j]
				else:
					if found_datatypes[self.column_names[j]] != thisdatatype:
						if found_datatypes[self.column_names[j]] == 'text' or thisdatatype == 'text':
							found_datatypes[self.column_names[j]] == 'text'
						elif found_datatypes[self.column_names[j]] == 'numeric' or thisdatatype == 'numeric':
							found_datatypes[self.column_names[j]] == 'numeric'
						elif found_datatypes[self.column_names[j]] == 'date' or thisdatatype == 'date':
							found_datatypes[self.column_names[j]] == 'text'


		for k in range(0,len(self.column_names)):
			self.column_datatypes.append(found_datatypes[self.column_names[k]])
			self.column_sample.append(found_datavalues[self.column_names[k]].replace('"',''))
			self.BigQuery_datatypes.append(self.translate_dt('BigQuery',found_datatypes[self.column_names[k]]))
			if not self.IsaDateField and self.translate_dt('BigQuery',found_datatypes[self.column_names[k]]) == 'DATE': 		
				self.IsaDateField = True
				self.DateField = self.column_names[k]
			else:
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
			return 'FLOAT'
		else:
			return 'UNKNOWN'
 
	def clean_column_name(self,col_name):

		new_column_name = col_name
		chardict = self.count_chars(col_name)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		if ((len(col_name)-2) == (alphacount + nbrcount)) and '1234567890'.find(col_name[:1]) == -1:
			new_column_name = col_name.replace('"','').strip()


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
			sql += '\t' + self.column_names[i] + ' ' + self.BigQuery_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'
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
			sql += '\t' + self.column_names[i] + ' ' + self.BigQuery_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'
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

		sql = 'CREATE TABLE IF NOT EXISTS ' + tablename + '(\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.column_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'
		sql = sql[:-2] + '\n);\n\n'
		sql += 'COMMENT ON TABLE ' + tablename + " IS 'This Postgres table was defined by schemawiz for loading the csv file " + self.csvfilename + ", delimiter= " + self.delimiter + "';\n"

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
			sql += '\t' + self.column_names[i] + ' ' + self.column_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'
		sql = sql[:-2] + '\n) \n'
		
		sql += 'COMMENT="This MySQL table was defined by schemawiz for loading the csv file ' + self.csvfilename + ', delimiter= ' + self.delimiter + '"; \n'

		return sql


if __name__ == '__main__':

	csvfilename = input('csvfile to read? ')
	
	obj = schemawiz(csvfilename)
	
	#obj.loadcsvfile(csvfilename)

	print('/* Postgres DDL - BEGIN ----- schemawiz(csvfilename).guess_postgres_ddl() ----- */ \n')
	ddl = obj.guess_postgres_ddl()
	print('Tablename used : ' + obj.lastcall_tablename + '\n')
	print(ddl)
	print('/* Postgres DDL - END   ----- ----- ----- ----- */ \n')

	print('/* MySQL DDL - BEGIN ----- schemawiz(csvfilename).guess_mysql_ddl() ----- */ \n')
	print(obj.guess_mysql_ddl())
	print('/* MySQL DDL - END   ----- ----- ----- ----- */ \n')

	print('/* BigQuery External DDL - BEGIN ----- schemawiz(csvfilename).guess_BigQueryExternal_ddl() ----- */ \n')
	print(obj.guess_BigQueryExternal_ddl())
	print('\n/* BigQuery External DDL - END   ----- ----- ----- ----- */ \n')

	print('/* BigQuery DDL - BEGIN ----- schemawiz(csvfilename).guess_BigQuery_ddl() ----- */ \n')
	print(obj.guess_BigQuery_ddl())
	print('\n/* BigQuery DDL - END   ----- ----- ----- ----- */ \n')
	

