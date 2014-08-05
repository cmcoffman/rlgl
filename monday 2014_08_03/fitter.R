
rlgl.model.fit <- function(plate, b=b, a=a, n=n, k=k){
  
#this will setup the fit parameters
plate$GFP.OD=plate$GFP/plate$OD
plate$g=plate$green.intensity

#input parameters
b = b                          #background ~"y int"
a = a                         # highest value minus low (minus b)
n = n                             #cooperativity - how sigmoidal it is
k = k                          #half maximum light intensity


plot(plate$g, plate$GFP.OD)

#non-linear least squares fit
fit = nls(GFP.OD ~ b+a*(((g^n)/((g^n)+(k^n)))), data=repeat.sunday, start=list(b=b, a=a, n=n, k=k))

return(fit)
}