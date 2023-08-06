import wammodels.global_func as gf
import pandas as pd
import numpy as np
import statsmodels.api as sm
from patsy import dmatrices
from statsmodels.regression.linear_model import OLS
import plotly.express as px

class Descomp:
	def __init__(self,formula_new=None):
		self.formula = formula_new
		self.descomp_end = None
		self.x_cero =  None
		self.beta_cero = None
		self.eq1 = None

	def prepare_var(self,formula=None):
		list_var_edit = []

		formula_get = formula

		if self.formula != None:
			formula_get = self.formula
		
		for index,value in enumerate(formula_get):
			data_info =  formula_get[index][0]
			if len(formula_get[index]) > 1:
				keys_extra = formula_get[index][1]
			
				adstock_rate = 0
				v = 0
				rho = 0
				lag = 0
				coef = ""
				contrib_min = 0
				contrib_max = 0

				if "lag" in keys_extra:
					lag = keys_extra["lag"]

				if "coef" in keys_extra:
					coef = keys_extra["coef"]

				if "contrib_min" in keys_extra:
					contrib_min = keys_extra["contrib_min"]

				if "contrib_max" in keys_extra:
					contrib_max =  keys_extra["contrib_max"]

				if "adstock_rate" in keys_extra:
					adstock_rate = keys_extra["adstock_rate"]
					if "rho" in keys_extra:
						rho = keys_extra["rho"]
						if "v" in keys_extra:
							v = keys_extra["v"]
							list_var_edit.append([gf.stockbudg(data_info,adstock_rate = adstock_rate, rho=rho, v=v),{"adstock_rate":adstock_rate,"rho":rho,"v":v,"lag":lag,"coef":coef,"contrib_min":contrib_min,"contrib_max":contrib_max}])
						else:
							list_var_edit.append([gf.stockbudg(data_info,adstock_rate = adstock_rate, rho=rho),{"adstock_rate":adstock_rate,"rho":rho,"v":v,"lag":lag,"coef":coef,"contrib_min":contrib_min,"contrib_max":contrib_max}])
					else:
						list_var_edit.append([gf.adstock(data_info,adstock_rate = adstock_rate),{"adstock_rate":adstock_rate,"rho":rho,"v":v,"lag":lag,"coef":coef,"contrib_min":contrib_min,"contrib_max":contrib_max}])
							
				elif "diff" in keys_extra:
					diff_index = keys_extra["diff"]
					list_var_edit.append([data_info.diff(diff_index),{"diff":diff_index,"lag":lag,"coef":coef,"contrib_min":contrib_min,"contrib_max":contrib_max}])

				else:
					list_var_edit.append([data_info,{"lag":lag,"coef":coef,"contrib_min":contrib_min,"contrib_max":contrib_max}])

			else:
				list_var_edit.append([data_info])
		
		return list_var_edit

	def prepare_formula(self,list_var):
		get_var_prepare = self.prepare_var(list_var)
		get_var_prepare_only = [x[0] for x in get_var_prepare]
		return get_var_prepare_only

	def new_formula(self,formula_get,get_var_prepare):
		v_lag   =  [i[1]["lag"] if len(i) > 1 and "lag" in i[1] else 0 for i in get_var_prepare]
		formula_array =  formula_get.replace("+","").replace("~","").split()
		new_formula = ""
		for key,valor in enumerate(v_lag):
			if key == 1:
				new_formula += " ~ "
			if key > 1:
				new_formula += " + "
			if valor != 0:
				formula_array[key] = f"{formula_array[key]}.shift({valor})"
			new_formula += formula_array[key]
		return new_formula

	def create_df_formula(self,*args):
		args_v = [x[0] for x in args]
		dfs = [pd.DataFrame(arg) for arg in args_v]
		df = pd.concat(dfs, axis=1)
		df.columns = ['v' + str(i) for i in range(1, len(df.columns)+1)]
		df = df.sort_index()
		formula = df.columns[0] + " ~ " + " + ".join(df.columns[1:])
		formula_new = self.new_formula(formula,args)
		return df, formula_new

	def create_model(self,formula,df):
		y_model, x_model = dmatrices(formula, data=df, return_type='dataframe')
		result = sm.OLS(y_model, x_model).fit()
		return (result,x_model)


	def get_descomp_end(self):
		return self.descomp_end

	def get_x_cero(self):
		return self.x_cero

	def get_beta_cero(self):
		return self.beta_cero

	def get_eq1(self):
		return self.eq1

	def get_descomp(self,table="df"):
		prepare_var_get = self.prepare_var()
		(df,formula_get2) = self.create_df_formula(*prepare_var_get)
		(EQ1,X_Model) = self.create_model(formula_get2,df)

		#GET COEF // muestra los coefiecientes
		coef =  EQ1.params
		#GET RESID // muestra los residuales
		resid =  EQ1.resid
		#GET INFO // muestra 3 dataframe del modelo
		info  =  EQ1.summary()
		#GET PVALOR // muestra el valor.
		p_valor =  EQ1.pvalues # print(p_valor.to_string(float_format='{:,.7f}'.format))

		beta_gorro = np.array(coef)
		beta_cero = coef[0]+resid

		x_cero = [1]*len(resid)
		nmvar =  len(coef)
		x_modelo = X_Model.iloc[:,1:]

		x_modelo["x_cero"] = x_cero
		first_column = x_modelo.pop('x_cero')
		x_modelo.insert(0, 'x_cero', first_column)

		count = 0 
		for name_column  in x_modelo.columns:
			x_modelo[name_column] = x_modelo[name_column]*beta_gorro[count]
			count+=1

		descomp_end = np.array(x_modelo).T

		self.descomp_end =  descomp_end
		self.x_cero = x_cero
		self.beta_cero = beta_cero
		self.eq1 = EQ1

		if table == "df":
			df = pd.DataFrame(descomp_end).T
			#df.columns = ['v' + str(i) for i in range(1, len(df.columns)+1)]
			return df
		return descomp_end

	def get_descomp_anclas(self,anclas):
		descomp_normal =  self.get_descomp_end()
		#anclas = [0, 0, 0, 0, 0, min(DESCOMP_NORMAL[6]), 0, min(DESCOMP_NORMAL[8]), 0, 0, 0, 0, 0, 0, 0, 0, 0]
		ancla_base = sum(anclas) + self.get_beta_cero()
		base_new = ancla_base*self.get_x_cero()
		base_rest_ancla =  descomp_normal.T[:, 1:]
		data_anclas = pd.DataFrame(base_rest_ancla).T
		for a in range(0,data_anclas.shape[1]):
			data_anclas[a] = data_anclas[a]-anclas
		base_rest_anclas_new = data_anclas.T

		descomp_anclas = pd.concat([pd.DataFrame(base_new).reset_index(drop=True),pd.DataFrame(base_rest_anclas_new).reset_index(drop=True)],axis=1)
		descomp_anclas.columns = ['v' + str(i) for i in range(1, len(descomp_anclas.columns)+1)]
		return descomp_anclas

	def graphic_descomp(self,descomp):
		data_descomp_graphic = pd.melt(descomp, var_name=['Variable'], value_name='Values')
		data_group = data_descomp_graphic.groupby(["Variable"],dropna=False).agg(
			{
				"Values" : "sum",
			}
		).reset_index()

		fig = px.bar(data_group.sort_values("Values"), x="Values", y="Variable",orientation="h")
		fig.update_yaxes(title='', visible=True, showticklabels=True)
		fig.update_xaxes(title="")
		return fig