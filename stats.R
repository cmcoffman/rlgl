#stats
lm0=lm(GFP~green.intensity*OD.600+plate+factor(row)*factor(column), data=cshl.all )
summary(lm0)
