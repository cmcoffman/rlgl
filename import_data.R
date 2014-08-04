#data.import
#read in just the nesisary rows from the original files
#fpath = file.path(getwd(), "raw_data", "20140718_171607_Schultzlab Phenolics_6602.csv");

#import abs data----
require(xlsx)
data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=3, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl4.abs.600=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=4, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl3.abs.600=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=5, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl2.abs.600=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=6, startRow=25, endRow=32, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl1.abs.600=data[,2:13]

#import flu data----
data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=3, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl4.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=4, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl3.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=5, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl2.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=6, startRow=56, endRow=63, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
cshl1.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=1, startRow=29, endRow=30, header=FALSE,
                colClasses=c(NULL, rep("numeric", 12)))
blank.600=data[,2:10]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=1, startRow=55, endRow=56, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
blank.gfp=data[,2:10]


#cleanup
rm(data)

#convert plates to table----
source("plate_to_table.R")

cshl1.abs.600=plate.to.table(cshl1.abs.600)
cshl2.abs.600=plate.to.table(cshl2.abs.600)
cshl3.abs.600=plate.to.table(cshl3.abs.600)
cshl4.abs.600=plate.to.table(cshl4.abs.600)

cshl1.gfp=plate.to.table(cshl1.gfp)
cshl2.gfp=plate.to.table(cshl2.gfp)
cshl3.gfp=plate.to.table(cshl3.gfp)
cshl4.gfp=plate.to.table(cshl4.gfp)

#this is a dumb hack to import the blanks because they are partial plates

letters=rep(c("B","C"), 9)
numbers=rep(c("03","04","05","06","07","08","09","10","11"), each=2)
coord.list=paste0(letters, numbers)
values=c(blank.600[1:2,1],
         blank.600[1:2,2],
         blank.600[1:2,3],
         blank.600[1:2,4],
         blank.600[1:2,5],
         blank.600[1:2,6],
         blank.600[1:2,7],
         blank.600[1:2,8],
         blank.600[1:2,9])
blank.600=data.frame(coordinate=coord.list, values=values)

letters=rep(c("B","C"), 9)
numbers=rep(c("03","04","05","06","07","08","09","10","11"), each=2)
coord.list=paste0(letters, numbers)
values=c(blank.gfp[1:2,1],
         blank.gfp[1:2,2],
         blank.gfp[1:2,3],
         blank.gfp[1:2,4],
         blank.gfp[1:2,5],
         blank.gfp[1:2,6],
         blank.gfp[1:2,7],
         blank.gfp[1:2,8],
         blank.gfp[1:2,9])
blank.gfp=data.frame(coordinate=coord.list, values=values)

#import metadata----
metadata=read.csv("metadata.csv")

random1=read.csv("randomizationMatrix (1).csv")
random2=read.csv("randomizationMatrix (2).csv")
random3=read.csv("randomizationMatrix (3).csv")
random4=read.csv("randomizationMatrix (4).csv")

#merge data and metadata----

well.index=subset(metadata, select=c(Well.Number, coordinate))

#put Well.Number on each plate
cshl1.gfp=merge(cshl1.gfp, well.index, by=c("coordinate"))
cshl2.gfp=merge(cshl2.gfp, well.index, by=c("coordinate"))
cshl3.gfp=merge(cshl3.gfp, well.index, by=c("coordinate"))
cshl4.gfp=merge(cshl4.gfp, well.index, by=c("coordinate"))

cshl1.abs.600=merge(cshl1.abs.600, well.index, by=c("coordinate"))
cshl2.abs.600=merge(cshl2.abs.600, well.index, by=c("coordinate"))
cshl3.abs.600=merge(cshl3.abs.600, well.index, by=c("coordinate"))
cshl4.abs.600=merge(cshl4.abs.600, well.index, by=c("coordinate"))

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


cshl1.abs.600=merge(cshl1.abs.600, rand.1, by=c("Well.Number"))
cshl2.abs.600=merge(cshl2.abs.600, rand.2, by=c("Well.Number"))
cshl3.abs.600=merge(cshl3.abs.600, rand.3, by=c("Well.Number"))
cshl4.abs.600=merge(cshl4.abs.600, rand.4, by=c("Well.Number"))

cshl1.gfp=merge(cshl1.gfp, rand.1, by=c("Well.Number"))
cshl2.gfp=merge(cshl2.gfp, rand.2, by=c("Well.Number"))
cshl3.gfp=merge(cshl3.gfp, rand.3, by=c("Well.Number"))
cshl4.gfp=merge(cshl4.gfp, rand.4, by=c("Well.Number"))

plot(cshl1.gfp$values, cshl1.gfp$green.intensity)

#get intensities
well.index=subset(metadata, select=c(Well.Number, green.intensity))
well.index=data.frame(Randomized.Index=well.index$Well.Number, Green.Intensity=well.index$green.intensity)

#merge with intensitieis
cshl1.abs.600=merge(cshl1.abs.600, well.index, by=c("Randomized.Index"))
cshl2.abs.600=merge(cshl2.abs.600, well.index, by=c("Randomized.Index"))
cshl3.abs.600=merge(cshl3.abs.600, well.index, by=c("Randomized.Index"))
cshl4.abs.600=merge(cshl4.abs.600, well.index, by=c("Randomized.Index"))

cshl1.gfp=merge(cshl1.gfp, well.index, by=c("Randomized.Index"))
cshl2.gfp=merge(cshl2.gfp, well.index, by=c("Randomized.Index"))
cshl3.gfp=merge(cshl3.gfp, well.index, by=c("Randomized.Index"))
cshl4.gfp=merge(cshl4.gfp, well.index, by=c("Randomized.Index"))




phen.plate1.meta=merge(phen.plate1, subset(metadata, plate==1, select = c(Well, good.sample)), by=c("Well"))


rm(values)
rm(coord.list)
rm(letters)
rm(numbers)
