###########################
# Parametric Bootstrap Code 
# from wordfish implementation in tm package
###########################
setwd("~/Dropbox/npt/data")
set.seed(123)

sigma <- 3
dir <- wfpool@dir
tol <- c(1e-06, 1e-08)

# Log-Likelihood Functions (Poisson model)
# ========================================

llik_psi_b <- function(p,y,omega,alpha,sigma) { # beta and psi will be estimated 
  b   <- p[1]   
  psi <- p[2]
  lambda<-exp(psi+alpha+b*omega)                  # Lambda parameter for Poisson distribution
  -(sum(-lambda+log(lambda)*y)-0.5*(b^2/sigma^2)) # Log-likelihood including normal prior on Beta
}


llik_alpha_1 <- function(p,y,b,psi) { # omega[1] is estimated
  omega <- p[1]
  lambda<-exp(psi+b*omega)        # Lambda parameter; alpha is excluded b/c it is set to be zero
  -sum(-lambda+log(lambda)*y)     # Log-likelihood
}

llik_alpha_omega <- function(p,y,b,psi) { # all other omegas and alphas are estimated
  omega <- p[1]
  alpha <- p[2]
  lambda<-exp(psi+alpha+b*omega)      # Lambda parameter
  -sum(-lambda+log(lambda)*y)     # Log-likelihood
}


llik_justalpha <- function(p,y,b,psi,omega) { # alpha is estimated
  alpha <- p[1]
  lambda<-exp(psi+alpha+b*omega)      # Lambda parameter
  -sum(-lambda+log(lambda)*y)     # Log-likelihood
}


# Expectation-Maximization Algorithm FOR MEAN 0, SD 1 IDENTIFICATION
# ==================================================================

rockingpoisson <- function(dta, tol, sigma, params=NULL, dir=dir, printsum=TRUE) {
  
  P <- nrow(dta)
  W <- ncol(dta)
  
  if (is.null(params)) {
    params <- rockingstarts(dta) # Call up starting value calculation
  }
  
  iter<-2
  maxllik<-cbind(-1e70,rep(0,1400))
  ll.words<-matrix(-1e70,W,1400)
  diffllik<-500
  
  # Set the convergence criterion 
  conv<-tol
  params$conv<-conv   
  
  while (diffllik>conv) { # Run algorithm if difference in LL > convergence criterion
    omegaprev<-params$omega
    bprev<-params$b   
    alphaprev<-params$alpha       
    psiprev<-params$psi 
    
    # ESTIMATE OMEGA AND ALPHA
    
    if(printsum==TRUE){
      cat("Iteration",iter-1,"\n")
      cat("\tUpdating alpha and omega..\n")
    }
    
    
    
    # Estimate first omega (alpha is set to 0)
    resa <- optim(p=c(params$omega[1]),
                  fn=llik_alpha_1,                        
                  y=as.numeric(dta[1,]),
                  b=params$b,
                  psi=params$psi,
                  method=c("BFGS")
    )
    params$omega[1] <- resa$par[1]
    params$min1[1] <- -1.00*resa$value
    params$alpha[1] <- 0
    ifelse(resa$convergence!=0,print("Warning: Optim Failed to Converge!"),NA)
    
    
    # Estimate all other omegas and alphas    
    for (i in 2:P) {
      
      resa <- optim(par=c(params$omega[i],params$alpha[i]),
                    fn=llik_alpha_omega,
                    y=as.numeric(dta[i,]),
                    b=params$b,
                    psi=params$psi)
      params$omega[i] <- resa$par[1]
      params$alpha[i] <- resa$par[2]
      params$min1[i] <- -1.00*resa$value
      ifelse(resa$convergence!=0,print("Warning: Optim Failed to Converge!"),NA)
      
    }    
    
    flush.console()
    
    
    # Z-score transformation of estimates for omega (to identify model)
    omegabar     <- mean(params$omega)
    b1       <- params$b
    params$b <- params$b * sd(params$omega)
    params$omega <- (params$omega - omegabar)/ sd(params$omega)
    params$psi <- params$psi + b1*omegabar  
    
    # Global identification
    if (params$omega[dir[1]]>params$omega[dir[2]]){params$omega<-params$omega*(-1)}
    
    
    
    # ESTIMATE PSI AND BETA
    if(printsum==TRUE){
      cat("\tUpdating psi and beta..\n")}
    
    for (j in 1:W) {                        
      resb <- optim(par=c(params$b[j],params$psi[j]),
                    fn=llik_psi_b,
                    y=dta[,j], 
                    omega=params$omega,
                    alpha=params$alpha,
                    sigma=sigma
      )
      params$b[j] <- resb$par[1]
      params$psi[j] <- resb$par[2]
      params$min2[j] <- -1.00*resb$value
      ifelse(resa$convergence!=0,print("Warning: Optim Failed to Converge!"),NA)
    }    
    
    flush.console()
    
    # Calculate Log-Likelihood
    maxllik[iter]<-sum(params$min2)
    diffparam<-mean(abs(params$omega-omegaprev)) # difference btw current & previous estimate for omega
    
    ll.words[,iter]<-params$min2
    diff.ll.words<-(ll.words[,iter]-ll.words[,iter-1])
    diffllik<-sum(diff.ll.words)/abs(maxllik[iter])
    
    
    if(printsum==TRUE){
      #print(sum(diff.ll.words))
      #print(abs(maxllik[iter]))
      cat("\tConvergence of LL: ",diffllik,"\n")
    }
    
    params$diffllik[iter-1]<-diffllik
    params$diffparam[iter-1]<-diffparam
    params$diffparam.last<-diffparam
    params$maxllik[iter-1]<-maxllik[iter]
    params$iter<-iter-1
    iter<-iter+1
  }    
  params$diffllik[1]<-NA 
  return(params)
}

bootstrap<-function(nsim, model) {
  
  cat("STARTING PARAMETRIC BOOTSTRAP\n")
  
  nparty <- length(model@theta)
  nword <- length(model@beta)
  
  # Create matrix of results.
  output.se.omega <- matrix(0,nparty,nsim)
  output.se.b <- matrix(0,nword,nsim)
  
  alpha <- model@alpha
  omega <- model@theta
  psi <- model@psi
  b <- model@beta
  
  # create data matrix
  dtasim<-matrix(1,nrow=nparty,ncol=nword)
  
  cat("======================================\n")
  cat("Now running", nsim,"bootstrap trials.\n")
  cat("======================================\n")
  cat("Simulation ")
  
  for (k in 1:nsim){
    
    cat(k,"...")
    
    # Generate new data using lambda 
    for (i in 1:nparty) {
      dtasim[i,] <- rpois(nword, exp(psi+alpha[i]+b*omega[i]))  
    }
    
    alphastart <- alpha + rnorm(nparty, mean=0, sd=(sd(model@alpha)/2))
    omegastart <- omega + rnorm(nparty, mean=0, sd=(sd(model@theta)/2))
    psistart <- psi + rnorm(nword, mean=0,sd=(sd(model@psi)/2))
    bstart <- b + rnorm(nword, mean=0,sd=(sd(model@beta)/2))
    params <- list(alpha=alphastart,omega=omegastart,psi=psistart,b=bstart)      
    
    
    
    est <- rockingpoisson(dtasim,tol,sigma,params=params,dir=dir,printsum=FALSE)
    
    # Store omegas 
    output.se.omega[,k] <- est$omega
    # Store Bs
    output.se.b[,k] <- est$b
  }
  
  
  conf.documents<-matrix(0,nparty,4)
  colnames(conf.documents)<-c("LB","UB","Omega: ML","Omega: Sim Mean")
  rownames(conf.documents) <- model@docs
  for (i in 1:nparty) {
    conf.documents[i,1]<-quantile(output.se.omega[i,],0.025)
    conf.documents[i,2]<-quantile(output.se.omega[i,],0.975)
    conf.documents[i,3]<-omega[i]
    conf.documents[i,4]<-mean(output.se.omega[i,])
  }
  
  
  
  #CI for word weights
  conf.words<-matrix(0,nword,4)
  colnames(conf.words)<-c("LB","UB","B: ML","B: Sim Mean")
  rownames(conf.words) <- model@features
  
  
  for (i in 1:nword) {
    conf.words[i,1]<-quantile(output.se.b[i,],0.025)
    conf.words[i,2]<-quantile(output.se.b[i,],0.975)
    conf.words[i,3]<-b[i]
    conf.words[i,4]<-mean(output.se.b[i,])
  }
  
  return(list(conf.documents=conf.documents,conf.words=conf.words, output.se.omega = output.se.omega, output.se.b = output.se.b))
}