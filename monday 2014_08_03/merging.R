well.index=subset(metadata, select=c(Well.Number, coordinate))

cshl1=merge(cshl1, well.index, by=c("coordinate"))
cshl2=merge(cshl2, well.index, by=c("coordinate"))
cshl3=merge(cshl3, well.index, by=c("coordinate"))
cshl4=merge(cshl4, well.index, by=c("coordinate"))

#merge with randomization matrix
well.index=subset(metadata, select=c(Well.Number, green.intensity))

rand.1=data.frame(position=random1$Randomized.Index, Well.Number=random1$Well.Number)
rand.1=merge(rand.1, well.index, by="Well.Number")
rand.1=rand.1[,2:3]
rand.1=data.frame(Well.Number=rand.1$position, green.intensity=rand.1$green.intensity)

rand.2=data.frame(position=random2$Randomized.Index, Well.Number=random2$Well.Number)
rand.2=merge(rand.2, well.index, by="Well.Number")
rand.2=rand.2[,2:3]
rand.2=data.frame(Well.Number=rand.2$position, green.intensity=rand.2$green.intensity)

rand.3=data.frame(position=random3$Randomized.Index, Well.Number=random3$Well.Number)
rand.3=merge(rand.3, well.index, by="Well.Number")
rand.3=rand.3[,2:3]
rand.3=data.frame(Well.Number=rand.3$position, green.intensity=rand.3$green.intensity)

rand.4=data.frame(position=random4$Randomized.Index, Well.Number=random4$Well.Number)
rand.4=merge(rand.4, well.index, by="Well.Number")
rand.4=rand.4[,2:3]
rand.4=data.frame(Well.Number=rand.4$position, green.intensity=rand.4$green.intensity)



cshl2=merge(cshl2, rand.2, by=c("Well.Number"))
cshl3.gfp=merge(cshl3.gfp, rand.3, by=c("Well.Number"))
cshl4.gfp=merge(cshl4.gfp, rand.4, by=c("Well.Number"))

plot(cshl1.gfp$green.intensity, cshl1.gfp$values)

