"""
  Dave Skura
  
"""
import datetime

class dater:
	def __init__(self,date_to_check=''):
		
		self.date_formats = ['%Y-%d-%m','%Y-%m-%d']
		self.date_to_check = date_to_check 
		if date_to_check != '':
			self.chk_date(date_to_check)


	def chk_date(self,possible_date_str):
		print (" Checking date " + possible_date_str) # 
		self.date_type = self.match_date_type(possible_date_str)

		if self.date_type == -1:
			print('Not a date. date_type = ' + str(self.date_type))
		else:
			print('Is a date, and matchs date_type ' + str(self.date_type) + ', ' + self.date_formats[self.date_type])

		return self.date_type

	def chk_date_format(self,date_string,date_format):
		try:
			dateObject = datetime.datetime.strptime(date_string, date_format)
			return True
		except ValueError:
			return False

	# -1 means no matching date format
	# > -1 means the date format matches self.date_formats[return_value]
	def match_date_type(self,date_string):	
		for i in range(0,len(self.date_formats)):
			if self.chk_date_format(date_string,self.date_formats[i]):
				return i
		return -1

if __name__ == '__main__':
	datetime.datetime.strptime('Jan 31/23','Mon DD/YY')

	obj = dater()

	# add any specific known date formats
	#obj.date_formats.append('%Y-%m-%d')
	dt = obj.match_date_type('2023-2-28')
	print(str(dt))
	print(obj.date_formats[dt])

	

