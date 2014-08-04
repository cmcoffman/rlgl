#spatial autocorrelation with Moran's I
#this is a big matrix, don't be alarmed
cshl.dists <- as.matrix(dist(cbind(cshl.all$column, cshl.all$row)))
inv.cshl.dists <- 1/cshl.dists
diag(inv.cshl.dists) <- 0

#get rid of infinities
inv.cshl.dists[is.infinite(inv.cshl.dists)] <- 0

require("ape")
Moran.I(cshl.all$GFP, inv.cshl.dists)

#pair plots of variables
attach(subset(cshl.all, cshl.all$plate==1))

plot(data.frame(OD.600, GFP, row, column))
detach(cshl.all)
