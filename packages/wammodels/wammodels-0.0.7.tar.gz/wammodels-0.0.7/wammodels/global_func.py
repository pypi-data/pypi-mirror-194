import numpy as np
import pandas as pd

def adstock_new(sales, decay_rate):
	sales = np.array(sales, dtype=float)
	adstock_sales = np.zeros_like(sales)
	adstock_sales[0] = sales[0]
	for i in range(1, len(sales)):
		adstock_sales[i] = sales[i] + decay_rate * adstock_sales[i-1]            
	return adstock_sales

def adstock(list,adstock_rate):
	adstock_list = []
	for i in range(len(list)):
		if i == 0: 
			adstock_list.append(list[i])
		else:
			adstock_list.append(list[i] + adstock_rate * adstock_list[i-1])            
	return adstock_list

def adbudg(list,rho=0,v=1,p=1,beta=1,alpha=0):
	rho = rho*p
	tk=  alpha+((beta*(np.power(list,v)) )/( (np.power(list,v)) + (np.power(rho,v)) ))
	return tk

def stockbudg(var ,adstock_rate, rho=0, v=1, p=1 ,beta=1, alpha=0):
	return adbudg(adstock_new(var, adstock_rate), v = v, rho = rho, p = p, beta = beta, alpha = alpha)

def creation_seasonalities(data,start_range):
	matrix = np.zeros((len(data), 12))
	base = pd.DataFrame(matrix, columns=["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"])
	k = start_range
	base.loc[0, base.columns[k-1]] = 1
	for i in range(1, len(data)):
		k += 1
		if k > 12:
			k = 1
		base.loc[i, base.columns[k-1]] = 1
	
	return base

def create_dummy(start_range,end_range,add_dummy,freq="MS"):
	dates = pd.date_range(start=start_range, end=end_range, freq=freq)
	var_dummy = pd.Series(data=[0]*len(dates), index=dates)
	var_dummy[add_dummy] = 1
	var_dummy.reset_index(drop=True,inplace=True)
	return var_dummy

def get_contrib(data):
	decomp_total = data.sum()
	decomp_prcnt = decomp_total/sum(decomp_total)
	return decomp_prcnt

def wmadstock_rate(*args):
	return {"adstock_rate":list(args)}
def wmv(*args):
	return {"v":list(args)}
def wmrho(*args):
	return {"rho":list(args)}
def wmdiff(*args):
	return {"diff":list(args)}
def wmlag(*args):
	return {"lag":list(args)}
def wmcoef(*args):
	return {"coef":list(args)}
def wmcontrib(*args):
	return {"contrib":list(args)}
def wmmax(*args):
    return {"max_h":list(args)}
def wmtitle(*args):
    return {"title":list(args)}
#def wmcomb(*args):
#    if len(args) <= 0:
#        return {}
#    return reduce(lambda a, b: {**a, **b}, args)
def wmcomb(*args):
	if len(args) <= 0:
		return {}
	data =  args[0]
	for arg in args[1:]:
		data = {**data, **arg}
	#data = {k: v[0] for k, v in data.items()}
	return data
def wmvar(*args):
	if len(args) <= 0:
		return {}
	data =  args[0]
	for arg in args[1:]:
		data = {**data, **arg}
	data = {k: v[0] for k, v in data.items()}
	return data

def test_comb(comb):
	for b in comb:
		print(f"Variable : {b.upper()}")
		print("----------------------")
		print("Values Combinations:")
		var =  comb[b]
		other_var = ["lag","diff"]
		if b in other_var:
			min = int(var[0])
			if len(var) > 1:
				max = int(var[1])+1
				freq = int(var[2])
			else:
				max = min+1
				freq = min

			for range_var in range(min,max,freq):
				print(f"-> {range_var}")
		else:
			min = int(var[0]*100)
			if len(var) > 1:
				max = int(var[1]*100)+1
				freq = int(var[2]*100)
			else:
				max = min+1
				freq = min

			for range_var in range(min,max,freq):
				print(f"-> {range_var/100.0}")
		