#plots!

require(ggplot2)
cshl.plot.OD <- ggplot(repeat.sunday, aes(green.intensity, OD.600))
cshl.plot.OD=cshl.plot.OD + 
  geom_point() + 
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity") +
  xlab("Green Intensity") +
  ylab("OD.600")
cshl.plot.OD
#ggsave("cshl-plot-OD.png")

cshl.plot.GFP <- ggplot(repeat.sunday, aes(green.intensity, GFP))
cshl.plot.GFP=cshl.plot.GFP + 
  geom_point() + 
  #scale_x_discrete(limits=c("mock","MeJA")) +
  #facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity") +
  xlab("Green Intensity") +
  ylab("GFP") +
  geom_smooth(method = "loess")
cshl.plot.GFP
#ggsave("cshl-plot-GFP.png")


cshl.plot.GFP.row <- ggplot(repeat.sunday, aes(factor(row), GFP))
cshl.plot.GFP.row=cshl.plot.GFP.row +
  geom_boxplot() + 
  facet_grid(.~plate) +
  ggtitle(label="GFP by row for each plate") +
  xlab("Row") +
  ylab("GFP")
cshl.plot.GFP.row
#ggsave("cshl-plot-GFP-row.png")

cshl.plot.OD.row <- ggplot(repeat.sunday, aes(factor(row), OD.600)) +
  geom_boxplot() + 
  facet_grid(.~plate) +
  ggtitle(label="OD by row for each plate") +
  xlab("Row") +
  ylab("OD.600")
cshl.plot.OD.row
#ggsave("cshl-plot-OD-row.png")

cshl.plot.GFP.column <- ggplot(repeat.sunday, aes(factor(column), GFP)) +
  geom_boxplot() + 
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity by column for each plate") +
  xlab("Column") +
  ylab("GFP")
cshl.plot.GFP.column
#ggsave("cshl-plot-GFP-column.png")


cshl.plot.OD.column <- ggplot(repeat.sunday, aes(factor(column), OD.600)) +
  geom_boxplot() + 
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity by column for each plate") +
  xlab("Column") +
  ylab("OD.600")
cshl.plot.OD.column
#ggsave("cshl-plot-OD-column.png")

cshl.plot.OD.vs.GFP <- ggplot(repeat.sunday, aes(GFP, OD.600)) +
  geom_point() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs GFP for each plate for each plate") +
  xlab("Column") +
  ylab("OD.600")
cshl.plot.OD.vs.GFP
#ggsave("cshl-plot-ODvsGFP.png")

  