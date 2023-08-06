import rpy2
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2.robjects.numpy2ri as numpy2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter

def f(x):
	return ""

rpy2.rinterface_lib.callbacks._CCHAR_ENCODING = "cp1252"

utils = importr('utils')
rpy2.rinterface_lib.callbacks.consolewrite_warnerror = f
r = robjects.r
suppmsg = robjects.r["suppressMessages"]

class Optimization:
	def __init__(self):
		self.formula =  None
		self.investment = 0
		#self.optimization = self.load_optimization()
		self.load_archive()
  
	def load_archive(self):
		suppmsg(utils.capture_output(r.source("OPTIMIZACION_NEW.r")))

	def prepare_formula(self,formula):
		data = pd.DataFrame.from_records([x[0] for x in formula])
		data_end = sum(data.values.tolist(),[])
		data_end_filtre = [end for end in data_end if not isinstance(end,str)]
		data_end_text = [end for end in data_end if isinstance(end,str)]
		with localconverter(robjects.default_converter + pandas2ri.converter + numpy2ri.converter):
			data_r_end =  robjects.conversion.py2rpy(data_end_filtre)
			data_r_text_end =  robjects.conversion.py2rpy(data_end_text)
		return (data_r_end,data_r_text_end)
     
	def load_optimization(self,formula,investment=0):
		(formula,text) = self.prepare_formula(formula)
		r.func_edit_inversion(investment)
		func_optimizacion = r.func_run_optimizacion(formula,text)
		data_final_optimizacion = pandas2ri.rpy2py(func_optimizacion).reset_index(drop=True)
		data_final_optimizacion["investment"] = data_final_optimizacion["investment"].astype(int)
		return data_final_optimizacion

	
	