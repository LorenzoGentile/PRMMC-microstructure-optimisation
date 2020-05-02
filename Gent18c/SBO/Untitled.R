nlc2t <- function(x, r, delta, ref) {
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
      C[ii] = sqrt(dis.x + dis.y + dis.z) - 2 * r - delta
      ii = ii + 1
    }
  }
  return(C)
}
obj2t <- function(x, r, delta, ref) {
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
  return(S)
}
n.part<- 20
delta=0.1
vf <- 0.1
r <- (1000 * vf * 3 / (4 * pi * n.part)) ^ (1 / 3)
ref=c(2,2,2)
LB <- matrix(r + delta, ncol = 1, nrow = n.part * 3)
x0<-LB
UB <- matrix(10 - r - delta, ncol = 1, nrow = n.part * 3)
j<-nloptr(x0=rep(0,n.part*3), eval_f=obj2t, lb=LB, ub=UB,eval_g_ineq = nlc2t,
      xtol_rel = 1e-6, nl.info = FALSE, r=r, delta=delta, ref=ref,opts=list("algorithm" ="NLOPT_GN_ISRES",maxeval=1e3,      pop.size = 20*(length(x0)+1)))
