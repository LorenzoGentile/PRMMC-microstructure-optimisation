library("SPOT")
library("GA")
library("parallel")
create_folder <- function(i) {
  programs<-c("Griglia_part.sat","PBCx_lorenzo.py","Read_DISP.py", "Sfera_r_1.sat","Ex.py")
  
  for (i in 1:i){
    wd <-
      file.path(
        "C:",  "out_ABQ"  , "Gaussian",  
        as.character(i),
        "/"
      )
    dir.create(wd)
    file.copy(programs,wd)
  }
}
Remove_files<-function (j){
  programs<-c("Griglia_part.sat","PBCx_lorenzo.py","Read_DISP.py", "Sfera_r_1.sat","Ex.py")
  for (i in 1:j) {
    wd<-file.path("C:",  "out_ABQ"  , "Gaussian",as.character(i),"/")
    setwd(wd)
    lista<-list.files(path = wd) 
    file.remove(setdiff(lista, programs))
  }
  wd<-file.path("C:",  "out_ABQ"  , "Gaussian")
  setwd(wd)
}
nlc2 <- function(x, r, delta, ref,...) {
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
  return(sum(C[C > 0]))
}
obj2E <- function(x, r, delta, ref,...) {
  end = length(x)
  
  C <- nlc2(x, r, delta, ref)
  s.x = sd(x[seq(1, end, 3)])
  s.y = sd(x[seq(2, end, 3)])
  s.z = sd(x[seq(3, end, 3)])
  m.x = mean(x[seq(1, end, 3)])
  m.y = mean(x[seq(2, end, 3)])
  m.z = mean(x[seq(3, end, 3)])
  S = ((s.x - ref[1]) ^ 2 + (s.y - ref[2]) ^ 2 + (s.z - ref[3]) ^ 2 +
   (m.x - 5) ^ 2 + (m.y - 5) ^ 2 + (m.z - 5) ^ 2) ^ 0.5
 # S = ((s.x - ref[1]) ^ 2 + (s.y - ref[2]) ^ 2 + (s.z - ref[3]) ^ 2) ^ 0.5
  if (C > 0.0001) {
    S = S + C * 1000
  }
  return(-S)
}
lowerLevel <- function(i,n.part,r,LB,UB,ref,...){
  i=1 # To change if parallel
  wd <- file.path( "C:",  "out_ABQ" , "Gaussian", as.character(i))
  setwd(wd)
    
  GA <- ga( maxFitness = -1e-1,      popSize = 30,      pcrossover = 0.75,      pmutation = 0.15,      elitism = 3,
      type = "real-valued",  fitness=    obj2E,      min = LB,      max = UB,      maxiter = 2e3,      run = 2e3,
      r = r,      delta = delta,ref=ref)
    x.pos<-GA@population[which.max(GA@fitness),]
    E<- Abaqus(x.pos,r,delta,n.part,LB,UB,i=i,wd)
    Remove_files(i)
    end=n.part*3
    s.x = sd(x.pos[seq(1, end, 3)])
    s.y = sd(x.pos[seq(2, end, 3)])
    s.z = sd(x.pos[seq(3, end, 3)])
    return(list(E,c(s.x,s.y,s.z,n.part)))
    
}
Abaqus<- function(x.pos,r,delta,n.part,LB,UB,i,wd,...){
  REF <- -6.89
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

C <- nlc2(x.pos, r, delta, ref = x[l, ])
if (max(C) <= 0.01 &
    min(x.pos) >= LB[1, 1] &
    max(x.pos) <= UB[1, 1]){
      FileName <-file.path(    "C:",  "out_ABQ"  , "Gaussian",          as.character(i),          "DATI.py"        )
      write(n.part,FileName,append = TRUE,sep = "\n")
      write(X, FileName, append = TRUE, sep = "\n")
      write(Y, FileName, append = TRUE, sep = "\n")
      write(Z, FileName, append = TRUE, sep = "\n")
      write(scala,FileName,append = TRUE,sep = "\n")
      write(wd, FileName, append = TRUE, sep = "\n")
      system("abaqus cae script=Ex.py")
      FileName <-        file.path(          "C:",  "out_ABQ",  "Gaussian",           as.character(i),          "YM_calc.txt"        )
      E <- as.numeric(read.table(FileName))
      E <- E / 10000
      WF <- max(c(WF, E))
      assign("wf", WF, envir = .GlobalEnv)
    }

else{
  if (is.infinite(WF))
    
    E = REF + C
  
  else
    E = WF + C
  
}
return(E)
}
Young_Mod<-function(x, vf, n.part, delta){
  y=NULL
  xUpdated=NULL
  for(k in 1:nrow(x))
{
  folder=1
  n.part<- x[k,4]
  r <- (1000 * vf * 3 / (4 * pi * n.part)) ^ (1 / 3)
  LB <- matrix(r + delta, ncol = 1, nrow = n.part * 3)
  UB <- matrix(10 - r - delta, ncol = 1, nrow = n.part * 3)

  lowerResults<-mclapply(X=c(1:folder),FUN="lowerLevel",n.part,r,LB,UB,ref=x[k,1:3],mc.cores = 1,mc.set.seed = TRUE)
  # cl <- makeCluster(mc <- getOption("cl.cores", 1))
  #clusterExport(cl=cl, varlist=ls())
# lowerResults<-parLapply(cl,1:folder,FUN=lowerLevel,n.part,r,LB,UB,ref=x[k,1:3],mc.cores = 1,mc.set.seed = TRUE)
   for (i in 1:folder) {
     y=rbind(y,unlist(lowerResults[[i]][1]))
     xUpdated=rbind(xUpdated,unlist(lowerResults[[i]][2]))
   }
  
}
  return(list(y,xUpdated))
}
{
  if (!exists("wf", envir = .GlobalEnv))
  wf <- -Inf
  vf <- 0.1
  lb <- c(0.7, 0.7, 0.7,2)
  ub <- c(2.5, 2.5, 2.5,50)
  delta <- 0.1
} # Initial configuration
{
  spotConfig <- list(
    
    types = c("numeric", "numeric", "numeric","integer"),
    
    funEvals = 150,

    noise = TRUE,

    replicates = 1,

    seedSPOT = 1 ,

    design = designLHD,

    designControl=list(size=20,replicates=1),
    model = buildKriging,
    optimizer = optimDE,
    optimizerControl=list(itermax=1e4),
    plots = TRUE
  )
} # spotConfig

{
  resRf.YOUNG <-
    spot(
      x = NULL,
      fun = Young_Mod,
      lower = lb ,
      upper = ub ,
      control = spotConfig,
      delta = delta,
      vf = vf
    )
}# spotRun

