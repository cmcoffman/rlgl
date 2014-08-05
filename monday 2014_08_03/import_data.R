#data.import
#read in just the nesisary rows from the original files
#fpath = file.path(getwd(), "raw_data", "20140718_171607_Schultzlab Phenolics_6602.csv");

#import abs data----
require(xlsx)

abs=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=1, startRow=28, endRow=123, header=FALSE)
gfp=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=1, startRow=147, endRow=242, header=FALSE)
cshl4=data.frame(coordinate=abs[,1], Abs.600=abs[,2], GFP.flu=gfp[,2])
cshl4$plate=4

abs=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=2, startRow=28, endRow=123, header=FALSE)
gfp=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=2, startRow=147, endRow=242, header=FALSE)
cshl3=data.frame(coordinate=abs[,1], Abs.600=abs[,2], GFP.flu=gfp[,2])
cshl3$plate=3

abs=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=3, startRow=28, endRow=123, header=FALSE)
gfp=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=3, startRow=147, endRow=242, header=FALSE)
cshl2=data.frame(coordinate=abs[,1], Abs.600=abs[,2], GFP.flu=gfp[,2])
cshl2$plate=2

abs=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=4, startRow=28, endRow=123, header=FALSE)
gfp=read.xlsx("Tabor_step_function_plates.xlsx", sheetIndex=4, startRow=147, endRow=242, header=FALSE)
cshl1=data.frame(coordinate=abs[,1], Abs.600=abs[,2], GFP.flu=gfp[,2])
cshl1$plate=1




#read in randomization matricies

random4=read.csv("randomizationMatrix_stepOff.csv")
random3=read.csv("randomizationMatrix_steOn2.csv")
random2=read.csv("randomizationMatrix_(2).csv")
random1=read.csv("randomizationMatrix_stepOn1.csv")

#set metadata-----
cshl1$experiment=c("red precondition step up")
cshl2$experiment=c("repeat sunday")
cshl3$experiment=c("red precondition step up")
cshl4$experiment=c("step down")

metadata1=read.csv("metadata1.csv")
metadata2=read.csv("metadata2.csv")
metadata3=read.csv("metadata3.csv")
metadata4=read.csv("metadata4.csv")


#set well indicies
cshl1$plate.well.index=c(0:95)
cshl2$plate.well.index=c(0:95)
cshl3$plate.well.index=c(0:95)
cshl4$plate.well.index=c(0:95)

#merge with randomization matrix----
source("meta_merge.R")
cshl1=meta.merge(cshl1, metadata1, random1)
cshl2=meta.merge(cshl2, metadata2, random2)
cshl3=meta.merge(cshl3, metadata3, random3)
cshl4=meta.merge(cshl4, metadata4, random4)

cshl.all=rbind(cshl1, cshl2, cshl3, cshl4)


#these blanks values are hardcoded from Sunday
JT2.blank=0.131
media.blank=0.0482

#absorbance blank subtraction
cshl.all$OD.600=cshl.all$Abs.600-media.blank

#flu blank subtraction
cshl.all$GFP=cshl.all$GFP.flu-(JT2.blank-media.blank)*(cshl.all$OD.600/JT2.blank)

#group experiments
step.up=subset(cshl.all, cshl.all$plate==1 | cshl.all$plate==3)
repeat.sunday=subset(cshl.all, cshl.all$plate==2)
step.down=subset(cshl.all, cshl.all$plate==4)
