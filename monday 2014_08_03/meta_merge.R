
meta.merge <- function(plate, metadata, randomization){
  merge1=merge(randomization, metadata, by.x="Well.Number", by.y="metadata.well.number")
  merge2=merge(merge1, plate, by.x="Randomized.Index", by.y="plate.well.index")
  return(merge2)
}

