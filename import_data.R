#data.import
#read in just the nesisary rows from the original files
#fpath = file.path(getwd(), "raw_data", "20140718_171607_Schultzlab Phenolics_6602.csv");

#import abs data----
require(xlsx)
data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=3, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl4.abs.600=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=4, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl3.abs.600=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=5, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl2.abs.600=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=6, startRow=28, endRow=35, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl1.abs.600=data[,2:13]

#import flu data----
data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=3, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl4.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=4, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl3.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=5, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl2.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=6, startRow=59, endRow=66, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
chsl1.gfp=data[,2:13]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=1, startRow=29, endRow=30, header=FALSE,
                colClasses=c(NULL, rep("numeric", 12)))
blank.600=data[,2:10]

data=read.xlsx("140803_rgv2_and_dilutions.xlsx", sheetIndex=1, startRow=55, endRow=56, header=FALSE,
               colClasses=c(NULL, rep("numeric", 12)))
blank.gfp=data[,2:10]


#cleanup
rm(data)





