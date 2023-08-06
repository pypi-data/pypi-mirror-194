rm(list=ls())
{
  suppressMessages(library(nloptr))
}
{
  inversion <- 0
  TOTAL_VAR_SEND <- 4 # NOT TOUCH
}

func_run_optimizacion <- function(data,title_m){
  list_var <- lapply(list(data), as.numeric)
  size_list <- length(list_var[[1]])
  title_medios <- title_m
  
  get_convert_object <- function(x){
    var_return <- 0
    index_x <- 1
    for (i in seq(1,size_list,by=TOTAL_VAR_SEND)) {
      coef = list_var[[1]][i]
      rho = list_var[[1]][i+1]
      p_v = list_var[[1]][i+2]
      formula <- coef*(((x[index_x]/rho)^p_v)/(((x[index_x]/rho)^p_v)+1))
      var_return = var_return+formula
      index_x = index_x+1
    }
    return (var_return)
  }
  
  get_convert_gradient <- function(x){
    var_return = list()
    index_x <- 1
    for (i in seq(1,size_list,by=TOTAL_VAR_SEND)) {
      coef = list_var[[1]][i]
      rho = list_var[[1]][i+1]
      p_v = list_var[[1]][i+2]
      var_return[index_x] = -(coef * ((x[index_x]/rho)^(p_v - 1) * (p_v * (1/rho))/(((x[index_x]/rho)^p_v) + 1) - ((x[index_x]/rho)^p_v) * ((x[index_x]/rho)^(p_v - 1) * (p_v * (1/rho)))/(((x[index_x]/rho)^p_v) + 1)^2))
      index_x = index_x +1
    }
    return (c(var_return,recursive = TRUE))
  }
  
  eval_f<- function( x ) {
    objetive = -(get_convert_object(x))
    gradient = get_convert_gradient(x)
    return( list("objective" = objetive,
                 "gradient" = gradient))
  }

  eval_g_eq_3<- function( x ) {
    formula <- 0
    for (i in seq(1,size_list/TOTAL_VAR_SEND)) {
      formula = formula + x[i]
    }
    formula = formula - inversion
    constr_3<- c(formula)
    grad_3<- c(list(rep(1,size_list/TOTAL_VAR_SEND)),recursive = TRUE)
    return( list( "constraints"=constr_3, "jacobian"=grad_3 ))
  }

  get_ub <- function(){
    max_list = list()
    index_max <- 1
    for (i in seq(1,size_list,by=TOTAL_VAR_SEND)) {
      max_list[index_max] <- list_var[[1]][i+3]
      index_max = index_max+1
    }
    return (max_list)
  } 
  get_contribuccion <- function(resultados)
  {
    var_return = list()
    for (a in seq(1,size_list/TOTAL_VAR_SEND)) {
      if(a <= 1) 
      {
        coef = list_var[[1]][(a*(TOTAL_VAR_SEND))-3]
        rho = list_var[[1]][(a*(TOTAL_VAR_SEND)+1)-3]
        p_v = list_var[[1]][(a*(TOTAL_VAR_SEND)+2)-3]
        var_return[a] <-  coef * (((resultados[a,1]/rho)^p_v)/((((resultados[a,1]/rho)^p_v)+1)))

      }else{
        coef = list_var[[1]][((a-1)*(TOTAL_VAR_SEND))+1]
        rho = list_var[[1]][((a-1)*(TOTAL_VAR_SEND)+1)+1]
        p_v = list_var[[1]][((a-1)*(TOTAL_VAR_SEND)+2)+1]
        var_return[a] <-  coef * (((resultados[a,1]/rho)^p_v)/((((resultados[a,1]/rho)^p_v)+1)))
      }
    }

    return (var_return)
  }

  # initial values#
  x0 <- c(list(rep(1,size_list/TOTAL_VAR_SEND)),recursive=TRUE)
  # lower and upper bounds of control
  lb <- c(list(rep(0,size_list/TOTAL_VAR_SEND)),recursive=TRUE)
  
  ub <- c(get_ub(), recursive=TRUE)
  
  local_opts <- list("algorithm" = "NLOPT_LD_MMA",
                     "xtol_rel" = 1.0e-7 )
  opts <- list("algorithm" = "NLOPT_LD_AUGLAG",
               "xtol_rel" = 1.0e-7,
               "maxeval" = 1000,
               "local_opts" = local_opts )
  
  res <- nloptr( x0=x0,eval_f=eval_f,lb=lb,ub=ub,eval_g_eq=eval_g_eq_3,opts=opts)
  resultados=data.frame(res$solution)
  colnames(resultados)[1] <- "investment"
  resultados$medio = c(title_medios,recursive=TRUE)
  resultados$contrib = c(get_contribuccion(resultados),recursive=TRUE)
  return(resultados)
}

func_edit_inversion <- function(inv){
  inversion <<- inv
}