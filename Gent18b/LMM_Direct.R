library("SPOT")
library("GA")
library("parallel")
library("DEoptimR")

Remove_files<-function (){
  programs<-c("Griglia_part.sat","PBC_Adaptive.py","LMM_Direct.R", "Sfera_r_1.sat","M1-LL_LMM_LC.dat","LMM_Dir.py")
  for (i in 1:1) {
    wd<-file.path("C:",  "out_ABQ"  ,"LMM_Direct", "/")
    setwd(wd)
    lista<-list.files(path = wd) 
    file.remove(setdiff(lista, programs))
  }
  wd<-file.path("C:",  "out_ABQ","LMM_Direct", "/"  )
  setwd(wd)
}
nlcD <- function(x, r, delta,...) {
r=1.68389
delta=0.1
  ii <- 1
  n.part <- (length(x) / 3)
  pos <- matrix(ncol = 3, nrow = n.part)
  C <-
    numeric(factorial(n.part) / (factorial(2) * factorial(n.part - 2)))
  for (i in 1:n.part) {
    pos[i, 1:3] <- x[(1 + 3 * (i - 1)):(3 + 3 * (i - 1))]
  }
  for (i in 1:(n.part - 1)) {
    for (j in (i + 1):n.part) {
      dis.x <- (pos[j, 1] - pos[i, 1]) ^ 2
      dis.y <- (pos[j, 2] - pos[i, 2]) ^ 2
      dis.z <- (pos[j, 3] - pos[i, 3]) ^ 2
      C[ii] = -sqrt(dis.x + dis.y + dis.z) + 2 * r + delta
      ii = ii + 1
    }
  }
  print(sum(C[C > 0]))
  return(sum(C[C > 0]))
}
nlcD2 <- function(x, r, delta,...) {
  r=1.68389
  delta=0.1
  ii <- 1
  n.part <- (length(x) / 3)
  pos <- matrix(ncol = 3, nrow = n.part)
  C <-
    numeric(factorial(n.part) / (factorial(2) * factorial(n.part - 2)))
  for (i in 1:n.part) {
    pos[i, 1:3] <- x[(1 + 3 * (i - 1)):(3 + 3 * (i - 1))]
  }
  for (i in 1:(n.part - 1)) {
    for (j in (i + 1):n.part) {
      dis.x <- (pos[j, 1] - pos[i, 1]) ^ 2
      dis.y <- (pos[j, 2] - pos[i, 2]) ^ 2
      dis.z <- (pos[j, 3] - pos[i, 3]) ^ 2
      C[ii] = -sqrt(dis.x + dis.y + dis.z) + 2 * r + delta
      ii = ii + 1
    }
  }
  
  return(C)
}
Abaqus<- function(x,r,delta,n.part,LB,UB,...){

  LL <- NULL
  Feasible <- matrix(0,nrow(x),1)
  for(l in 1:nrow(x))
  {
    
    
  x.pos<- x[l,]
  REF <- 0
  WF <- get(x = "wf", envir = .GlobalEnv)
  X <- numeric(n.part)
  Y <- X
  Z <- X
  scala <- X
  scala[1:n.part] <- r

  for (k in 1:n.part) {
    X[k] <- x.pos[(k - 1) * 3 + 1]
    
    Y[k] <- x.pos[(k - 1) * 3 + 2]
    
    Z[k] <- x.pos[(k - 1) * 3 + 3]
    
  }

  C <- nlcD(x.pos, r, delta)
  print(C)
  if (max(C) <= 0.01 &
      min(x.pos) >= LB[1] &
      max(x.pos) <= UB[1]){
    print("Feasible******************")
    Feasible[l,1] <- 1
    FileName <-file.path("C:",  "out_ABQ" ,"LMM_Direct" ,"DATI.py" )
    write(n.part,FileName,append = TRUE,sep = "\n")
    write(X, FileName, append = TRUE, sep = "\n")
    write(Y, FileName, append = TRUE, sep = "\n")
    write(Z, FileName, append = TRUE, sep = "\n")
    write(scala,FileName,append = TRUE,sep = "\n")

    system("abaqus cae nogui=lmm_Dir.py")
    {
      a<-grep("UPPER BOUND SHAKEDOWN LIMIT MULTIPLIER:  ",readLines("M1-LL.dat"), value = TRUE)
      matches <- regmatches(a[length(a)], gregexpr("[[:digit:]]+", a[length(a)]))
      res<-as.numeric(unlist(matches))
      while (res[2]>1) {
        res[2]<-res[2]/10
      }
      if(length(res)==3)
        res[2]=res[2]*(10^(-res[3]))
      ll <- -( res[1]+res[2])
    } # Read results
    
    #ll <- runif(1,-2,-1)
    print(ll)

    WF <- max(c(WF,ll))
   Remove_files()
  }
  
  else{
    if (is.infinite(WF))
      
      ll = REF + C
    
    else
      ll = WF + C
    
  }
  LL <- c(LL,ll)
  }
  return(list(matrix(LL,nrow(x),1),x,Feasible))
}
{
   if (!exists("wf", envir = .GlobalEnv))
    wf <- -Inf
  vf <- 0.1
  delta <- 0.1
  n.part <- 5
  r <- (1000 * vf * 3 / (4 * pi * n.part)) ^ (1 / 3)
  lb = rep(r + delta, n.part*3)
  ub = rep(10 - r - delta, n.part*3)
  design <- designLHD(,lower = lb,upper = ub,control = list(inequalityConstraint=nlcD,size=20))
} # Initial configuration
#yDes <- Abaqus(design,r,delta,n.part,lb,ub)

{
  spotConfig <- list(
    
    types = rep("numeric",n.part*3),
    
    funEvals = 150,
    
    noise = TRUE,
    
    replicates = 1,
    
    seedSPOT = 1 ,
    
    model = buildKriging,
    # optimizer = optimDE,
    # optimizerControl=list(itermax=1e4),
    plots = TRUE,
    designControl=list(x=design),
    # optimizercontrol=list(lb=lb,ub=ub,eval_g_ineq=nlcD,eval_f=5e4,r=r,delta=delta,"algorithm"="NLOPT_GN_ISRES"),
    optimizer=optimJDE
    # optimizercontrol=list(lb=lb,ub=ub,eval_g_ineq=nlcD,eval_f=5e4,r=r,delta=delta,"algorithm"="NLOPT_GN_ISRES")
    
  )
} # spotConfig

{
  res <-
    spot(
      x = design,
      fun = Abaqus,
      lower = lb ,
      upper = ub ,
      control = spotConfig,
      delta = delta,
      n.part =n.part,
      LB=lb,
      UB=ub,
      r=r,
      Feasible=20
    )
}# spotRun

