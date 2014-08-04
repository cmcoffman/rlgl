#this function converts something in the layout of a 96-well plate
#into a two column dataframe with the coordinate and the value in the cell
#note: this may have problems when the plate layout contains chracters and not just numbers

plate.to.table <- function(x){
  letters=rep(c("A","B","C","D","E","F","G","H"), 12)
  numbers=rep(c("01","02","03","04","05","06","07","08","09","10","11","12"), each=8)
  coord.list=paste0(letters, numbers)
  values=c(x[1:8,1],
           x[1:8,2],
           x[1:8,3],
           x[1:8,4],
           x[1:8,5],
           x[1:8,6],
           x[1:8,7],
           x[1:8,8],
           x[1:8,9],
           x[1:8,10],
           x[1:8,11],
           x[1:8,12])
  result=data.frame(coordinate=coord.list, values=values)
  return(result)
}