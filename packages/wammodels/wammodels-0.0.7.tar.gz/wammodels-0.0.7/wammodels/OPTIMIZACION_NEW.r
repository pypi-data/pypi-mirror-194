rm(list=ls())
{
  suppressMessages(library(nloptr))
}
{
  inversion <- 0
  TOTAL_VAR_SEND <- 4 # NOT TOUCH
}

func_run_optimizacion <- function(...){
  list_var <- lapply(list(...), as.numeric)
  size_list <- length(list_var)
  
  get_convert_object <- function(x){
    var_return <- 0
    index_x <- 1
    for (i in seq(1,size_list,by=TOTAL_VAR_SEND)) {
      coef = list_var[[i]]
      rho = list_var[[i+1]]
      p_v = list_var[[i+2]]
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
      coef = list_var[[i]]
      rho = list_var[[i+1]]
      p_v = list_var[[i+2]]
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
      max_list[index_max] <- list_var[[i+3]]
      index_max = index_max+1
    }
    return (max_list)
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
  return(resultados)
}

func_edit_inversion <- function(inv){
  inversion <<- inv
}