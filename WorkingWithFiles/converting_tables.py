import os
import xlrd
import sys




class convertTableToDictionary(object):
	"""docstring for convertTableToDictionary"""

	ROOT_PATH_OF_ACCESS = ""
	LISTOFACCESS_INTERNAL = {}
	ACCESS_FILE = ""
	ACCESS_FILE_PATH = ""

	def __init__(self, root_path: str, filename_of_access_file: str) -> None:
		super(convertTableToDictionary, self).__init__()
		self.ROOT_PATH_OF_ACCESS = root_path
		self.ACCESS_FILE = filename_of_access_file
		self.ACCESS_FILE_PATH = f"{self.ROOT_PATH_OF_ACCESS}/{self.ACCESS_FILE}"
		self.convert_table()



	def convert_table(self):
		try:
			workbook = xlrd.open_workbook(self.ACCESS_FILE_PATH)
			sheet = workbook.sheet_by_index(0)

		except Exception as e:
			print(f"Error message: {e}\n")
			print(f"Cannot find {self.ACCESS_FILE}\n")
			sys.exit()
			
		for row in range(1, sheet.nrows):
			intermidiate_data = [sheet.cell(row, col).value for col in range(sheet.ncols)]
			try:
				self.LISTOFACCESS_INTERNAL[intermidiate_data[-1]] = {'login_path':intermidiate_data[0], 'login_name':intermidiate_data[1], 'login_password':intermidiate_data[2]}
			except Exception as e:
				print(f"Error message: {e}\n")
				continue





	def get_list_of_accesses(self):
		return self.LISTOFACCESS_INTERNAL
