import pandas
import openpyxl
import sys
import os
import json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from drop import *


_EXCELR_ = lambda f,r,c=None: pandas.read_excel(f, sheet_name=r, usecols=c)

class queryPY(object):
	errorMSG = []
	error = False
	try:
		def __init__(self,method,con,query="",req=[]):
			self.conn = self.connect(con)
			self.sheets = self.conn.sheetnames
			self.res = self.functinon_list(method)(con,query,req)
			# self.conn.close()

		def result(self):
			return self.res

		def functinon_list(self,m):
			MET_FUNC = {
				"SELECT":self.selection_f,
				"INSERT":self.insert_f,
				"UPDATE":self.update_f,
				"DELETE":self.delete_f,
				"SHOW_TABEL":self.show_tabel_f,
				"SHOW_COLUMNS":self.show_coll_f,
				"FIELDS":self.show_field_f,
				"CREATE":self.create_f,
				"ALERT":self.alter_f
			}
			return MET_FUNC[m]
		def connect(self,a):
			self.DB_NAME = "_".join(a["excelFile"].split("/")[-2:]).split(".")[0]
			return openpyxl.load_workbook(a["excelFile"])

		def selection_f(self,a,q,r):
			q = list(filter(None,q.split(';')))
			if q:
				for i in q:
					i = list(filter(None,i.split('|')))
					sheet = i[0]
					columns = list(filter(None,i[1].split(','))) if i[1]!="*" else None
					if sheet in self.sheets:
						return _EXCELR_(a["excelFile"],sheet,columns).to_dict(orient='split')["data"]
			return []
		def insert_f(self,a,q,r):
			q = list(filter(None,q.split(';')))
			if q:
				try:
					for sheets in q:
						sheets = sheets.split('|')
						sheet = sheets[0]
						columns = [i for i in list(filter(None,sheets[1].split('=>')))[0].split('&') if i!=None]
						obj = json.loads(list(filter(None,sheets[1].split('=>')))[1].replace("NULL",'null'))
						if obj:
							data = _EXCELR_(a["excelFile"],sheet,columns)
							index = data.to_dict(orient='split')['index'][-1]+1 if len(data.to_dict(orient='split')['index'])>0 else 0
							df = pandas.concat([data, pandas.DataFrame([obj],columns=columns)], ignore_index=True)
							with pandas.ExcelWriter(a["excelFile"]) as writer:
								df.to_excel(writer, index=False,sheet_name=sheet)
					return True
				except BaseException as e:
					self.error = True
					self.errorMSG.append(e)
					return False
			return False

		def update_f(self,a,q,r):
			def dropCond(a,b,c):
				for i in 
			q = list(filter(None,q.split(';')))
			if q:
				try:
					for sheets in q:
						sheets = sheets.split('|')
						sheet = sheets[0]
						column = list(filter(None,sheets[1].split('->')))[0]
						value = list(filter(None,sheets[1].split('->')))[1]
						if value and column:
							data = _EXCELR_(a["excelFile"],sheet)
							columns = data.to_dict('split')['columns']
							obj = dropCond(r,data.to_dict('split')['data'],columns)
							# index = data.to_dict(orient='split')['index'][-1]+1 if len(data.to_dict(orient='split')['index'])>0 else 0
							df = pandas.concat([data, pandas.DataFrame([obj],columns=columns)], ignore_index=True)
					return True
				except BaseException as e:
					self.error = True
					self.errorMSG.append(e)
					return False
			return False

		def delete_f(self,a,q,r):
			
			return True
		def show_tabel_f(self,a,q,r):
			return [self.sheets]

		def show_field_f(self,a,q,r):
			def get_type_convert(np_type):
				convert_type = type(np.zeros(1,np_type).tolist()[0])
				return type(np_type), convert_type
			q = list(filter(None,q.split(';')))
			if q:
				for sheet in q:
					return [get_type_convert(i) for i in list(_EXCELR_(a["excelFile"],sheet).dtypes)]

		def show_coll_f(self,a,q,r):
			data = {}
			q = list(filter(None,q.split(';')))
			if q:
				for i in q:
					return _EXCELR_(a["excelFile"],i).to_dict(orient='split')['columns']
			return data
		def create_f(self,a,q,r):
			
			return False

		def alter_f(self,a,q,r):
			pass



	except BaseException as e:
		self.error = True
		self.errorMSG.append(e)
