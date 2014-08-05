#plots!

require(ggplot2)

#repeat-sunday-plots----

sunday.repeat.plot.GFP <- ggplot(repeat.sunday, aes(green.intensity, GFP))
sunday.repeat.plot.GFP=sunday.repeat.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity ") +
  #xlab("Green Intensity") +
  #ylab("GFP") +
  geom_smooth(method = "loess")
sunday.repeat.plot.GFP
ggsave("repeat-sunday-GFP.png")

sunday.repeat.plot.OD <- ggplot(repeat.sunday, aes(green.intensity, OD.600))
sunday.repeat.plot.OD=sunday.repeat.plot.OD +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity") 
##xlab("Green Intensity") +
##ylab("OD.600")
sunday.repeat.plot.OD
ggsave("repeat-sunday-OD.png")

sunday.repeat.plot.GFP.row <- ggplot(repeat.sunday, aes(factor(row), GFP))
sunday.repeat.plot.GFP.row=sunday.repeat.plot.GFP.row +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP by row ") 
  #xlab("Row") +
  #ylab("GFP")
  sunday.repeat.plot.GFP.row
ggsave("repeat-sunday-GFP-row.png")

sunday.repeat.plot.OD.row <- ggplot(repeat.sunday, aes(factor(row), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD by row ") 
  #xlab("Row") +
  #ylab("OD.600")
  sunday.repeat.plot.OD.row
ggsave("repeat-sunday-OD-row.png")

sunday.repeat.plot.GFP.column <- ggplot(repeat.sunday, aes(factor(column), GFP)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity by column ") +
  #xlab("Column") +
  #ylab("GFP")
  sunday.repeat.plot.GFP.column
ggsave("repeat-sunday-GFP-column.png")

sunday.repeat.plot.OD.column <- ggplot(repeat.sunday, aes(factor(column), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity by column ") 
  #xlab("Column") +
  #ylab("OD.600")
  sunday.repeat.plot.OD.column
ggsave("repeat-sunday-OD-column.png")

sunday.repeat.plot.OD.vs.GFP <- ggplot(repeat.sunday, aes(GFP, OD.600)) +
  geom_point() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs GFP  ") 
  #xlab("Column") +
  #ylab("OD.600")
  sunday.repeat.plot.OD.vs.GFP
ggsave("repeat-sunday-ODvsGFP.png")

#step-up-plots----
step.up.plot.GFP <- ggplot(step.up, aes(time, GFP))
step.up.plot.GFP=step.up.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="GFP vs Time by Intensity") 
  #xlab("Time") +
  #ylab("GFP") +
  geom_smooth(method = "loess")
step.up.plot.GFP
ggsave("step-up-GFP.png")

step.up.plot.OD <- ggplot(step.up, aes(time, OD))
step.up.plot.OD=step.up.plot.OD +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="OD vs Time by Intensity") 
  #xlab("Time") +
  #ylab("GFP") +
  geom_smooth(method = "loess")
step.up.plot.GFP
ggsave("step-up-OD.png")

step.up.plot.GFP.row <- ggplot(step.up, aes(factor(row), GFP))
step.up.plot.GFP.row=step.up.plot.GFP.row +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP by row ") 
  #xlab("Row") +
  #ylab("GFP")
  step.up.plot.GFP.row
ggsave("step.up-GFP-row.png")

step.up.plot.OD.row <- ggplot(step.up, aes(factor(row), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD by row ") 
  #xlab("Row") +
  #ylab("OD.600")
  step.up.plot.OD.row
ggsave("step.up-OD-row.png")

step.up.plot.GFP.column <- ggplot(step.up, aes(factor(column), GFP)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity by column ") 
  #xlab("Column") +
  #ylab("GFP")
  step.up.plot.GFP.column
ggsave("step.up-GFP-column.png")

step.up.plot.OD.column <- ggplot(step.up, aes(factor(column), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity by column ") 
  #xlab("Column") +
  #ylab("OD.600")
  step.up.plot.OD.column
ggsave("step.up-OD-column.png")

step.up.plot.OD.vs.GFP <- ggplot(step.up, aes(GFP, OD.600)) +
  geom_point() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs GFP  ") 
  #xlab("Column") +
  #ylab("OD.600")
  step.up.plot.OD.vs.GFP
ggsave("step.up-ODvsGFP.png")

#step-down-plots----
step.down.plot.GFP <- ggplot(step.down, aes(time, GFP))
step.down.plot.GFP=step.down.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="GFP vs Time by Intensity") 
  #xlab("Time") +
  #ylab("GFP") +
  geom_smooth(method = "loess")
step.down.plot.GFP
ggsave("step-down-GFP.png")

step.down.plot.OD <- ggplot(step.down, aes(time, OD))
step.down.plot.OD=step.down.plot.OD +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="OD vs Time by Intensity") 
  #xlab("Time") +
  #ylab("GFP") +
  geom_smooth(method = "loess")
step.down.plot.GFP
ggsave("step-down-OD.png")

step.down.plot.GFP.row <- ggplot(step.down, aes(factor(row), GFP))
step.down.plot.GFP.row=step.down.plot.GFP.row +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP by row ") 
#xlab("Row") +
#ylab("GFP")
step.down.plot.GFP.row
ggsave("step.down-GFP-row.png")

step.down.plot.OD.row <- ggplot(step.down, aes(factor(row), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD by row ") 
#xlab("Row") +
#ylab("OD.600")
step.down.plot.OD.row
ggsave("step.down-OD-row.png")

step.down.plot.GFP.column <- ggplot(step.down, aes(factor(column), GFP)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity by column ") 
#xlab("Column") +
#ylab("GFP")
step.down.plot.GFP.column
ggsave("step.down-GFP-column.png")

step.down.plot.OD.column <- ggplot(step.down, aes(factor(column), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity by column ") 
#xlab("Column") +
#ylab("OD.600")
step.down.plot.OD.column
ggsave("step.down-OD-column.png")

step.down.plot.OD.vs.GFP <- ggplot(step.down, aes(GFP, OD.600)) +
  geom_point() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs GFP  ") 
#xlab("Column") +
#ylab("OD.600")
step.down.plot.OD.vs.GFP
ggsave("step.down-ODvsGFP.png")



