# WAMMODELS

La libreria permite a los usuarios obtener combinaciones óptimas de variables y obtener resultados precisos de manera rápida y eficiente.

#### Actualmente soporta:
* Busqueda de combinaciones optimas
* Creacion de descomposición manual.

### Instalacion:
    pip install wammodels

## Importancion de Clases:
Las clases que posee la libreria wammodels son:
```python
from wammodels.global_func import *
from wammodels.combination import Combination
from wammodels.descomp import Descomp
```
**global_func** : Clase que posee funciones que nos ayudara a la creacion de combinaciones y la creacion de nuestra descomposicion:
```python
adstock(list,adstock_rate)
adbudg(list,rho=0,v=1,p=1,beta=1,alpha=0)
creation_seasonalities(data,start_range)
wmadstock_rate(*args):
wmv(*args):
wmrho(*args):
wmdiff(*args):
wmlag(*args):
wmcoef(*args):
wmcontrib(*args):
wmcomb(*args):
wmvar(*args):
test_comb(comb):
```

## Combination
En este ejemplo vamos a usar la clase  **Combination** para obtener un modelo basado en una busqueda de combinaciones las cuales nosotros le estamos proporcionando:

```python
#Importamos nuestras clases
from wammodels.global_func import *
from wammodels.combination import Combination

#Creamos nuestra formula
formula = [
    [y],
    [data.INVN, wmcomb(wmadstock_rate(0.05,0.50,0.06),wmcoef("+"))],
	[data.INVR, wmcomb(wmadstock_rate(0.05),wmv(1.0,4.5,0.05),wmrho(4000,30000000,2000),wmcontrib(0.10,0.20))],
    [data.ENE, wmcomb(wmlag(1,4,2))],
	[data.FEB, wmcomb(wmdiff(1,4,2))],
	[data.MAR],
]
#Enviamos nuestra formula a nuestra clase
get_combination = Combination(formula)
get_combination.search_combinations()
```

##### Explicacion:
Creamos un array donde vamos a ingresar nuestras variables, comenzando con la variable **Y**,
La variable **data.INVN** y la variable **data.INVR**  le agregamos la funcion **wmcomb** que es una funcion unica para la busqueda de combinaciones y dentro de esa funcion colocamos otras funciones como :

 * **wmadstock_rate** : Como podemos observer en la funcion le indicamos 3 numeros , **(0.05,0.50,0.06)** esto quiere decir que la variable **data.INVN** no va a tener un **wmadstock_rate** fijo como la variable **data.INVR** de lo contrario va a modificar los valores entre: **min : 0.05 - max: 0.50 con saltos de 0.06** 

* **wmv , wmrho** : Estas 2 funciones se usan para obtener el  **adbudg** siempre se tienen que poner las 2 funciones, de lo contrario dara error. Como se puede observar usa el mismo metodo de **min - max - salto** que la funcion **wmadstock_rate**

* **wmcoef** : Esta funcion se encarga en seleccionar la variable transformada cuando su coefciente sea positivo **wmcoef( "+")** asi mismo le podemos indicar que sea negativo **wmcoef("-")** 

* **wmcontrib** :  Esta funcion usa un rango de **min - max** indificando al algoritmo que cuando esa variable tenga una contribucion dentro de ese rango la dara como efectiva.

* **wmlag y wmdiff** : Estas 2 funciones usan el mismo metodo de la funcion **wmadstock_rate** , **min - max - salto** lo unico diferente es que sus valores son numeros enteros.

Teniendo nuestra formula lista procedemos a enviar la formula a la clase **Combination** - **Combination(formula)** luego de enviar nuestra formula ejecutamos la funcion **search_combinations()** la cual es la encargada de buscar las combinaciones y el modelo perfecto basado en la formula que hicimos.

##### Nota1: Las variables pueden tener valores fijos o con sus respectivos argumentos.
##### Nota2: Siempre que deseemos agregar una de estas funciones tenemos que colocar la funcion wmcomb y dentro de esa funcion agregar las funciones mencionadas.

# Funcion search_combinations()

Esta funcion permite ajustar nuestra busqueda con ciertos argumentos como son:

* **max_comb / default = 1 :**  El algoritmo se detiene cuando tenga x cantidad de modelos perfectos basados en nuestra formula realizada.

* **pvalor /default = 0.11:** Nos ayuda a obtener los modelos que sus variables no superen el pvalor ingresado

* **time_stop default = None :** Nos permite agregar un tiempo maximo de busqueda , cuando el tiempo llegue a su limite el algoritmo se detiene y dejara de buscar.

* **method = "default":**  Esta variable es muy importante ya que nuestro algoritmo cuenta con 2 algoritmos de busqueda **("default")** y **("cross")** el default es recomendable cuando tenemos pocas variables no quiere decir que no funcione con una formula con muchas variables y combinaciones, Puede funcionar perfectamente. El metodo cross es un algoritmo de ** "Busqueda Random Combinacion Cruzada"** , este metodo es entrenado para que busque por sectores eso implica que el algoritmo sea mas ordenado a la hora de buscar combinaciones , el algoritmo cross cuenta con 6 subprocesos dado que tiene 6 subprocesos es recomendable darle como tiempo de busqueda un minimo de 30 minutos para formulas con muchas combinaciones y variables.

#### Ejemplos:

* ##### Ejemplo 1 :
	* Usa el metodo **"cross"**
	* Cuando encuentre **3 combinaciones** o llegue a **30 minutos** de busqueda se detenga, lo primero que suceda.
```python
get_combination = Combination(formula)
get_combination.search_combinations(max_comb=3,method="cross",time_stop=60*30)
```

* ##### Ejemplo 2:
	* Usa el metodo **"default"**
	* Cuando encuentre **3 combinaciones** y todas las variables tengan un **pvalor <= 0.08** se detenga.
```python
get_combination = Combination(formula)
get_combination.search_combinations(max_comb=3,pvalor=0.08)
```

* ##### Ejemplo 3:
	* Usa el metodo **"cross"**
	* Le estamos diciendo que todas las variables deben de tener un **pvalor <= 0.20** y que se detenga a cumplir los **30 minutos**
```python
get_combination = Combination(formula)
get_combination.search_combinations(method="cross",time_stop=60*30,pvalor=0.20)
```

##### Basado en esos ejemplos podemos jugar con las diferentes variables como son el method , time_stop, pvalor y max_comb dependiendo nuestra necesidad.

# Funcion get_var_all()

Esta funcion se usara una ves terminada la busqueda y permite obtener las combinaciones que nuestro algoritmo encontro

```python
get_combination = Combination(formula_comb)
get_combination.search_combinations(max_comb=3,method="cross")
get_combination.get_var_all(0)
```

![](https://metin2.download/picture/OzWGLbc05JSmxoMV6VL0Am9mu9tkhpD2/.png)

Cuando ejecutamos esta funcion nos mostrara como resultado 2 dataframe, el valor 0 dentro de la funcion get_var_all(0) es la combinacion que queremos obtener. Si colocamos 1 nos traera la siguiente combinacion.
* El primer dataframe mostrara el R2 ajustado y el Durbin
* El segundo nos mostrara un dataframe indicando que combinaciones encontro y agregando los valores de **contribucion** , **coef** y **pvalor** (La imagen muestra una combinacion de una formula que tenia 18 variables.)

Si a nuestra funcion **get_var_all()** le agregamos la variable **table="df"** nos mostrara un dataframe diferente

```python
get_combination = Combination(formula_comb)
get_combination.search_combinations(max_comb=3)
get_combination.get_var_all(0,table="df")
```

![](https://metin2.download/picture/lD0g8P11gilG5x9RkN4QYvOgaz5I6oJ5/.png)










