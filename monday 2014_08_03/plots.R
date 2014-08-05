#plots!

require(ggplot2)

#repeat-sunday-plots----
cshl.plot.OD <- ggplot(repeat.sunday, aes(green.intensity, OD.600))
cshl.plot.OD=cshl.plot.OD +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity ") +
  xlab("Green Intensity") +
  ylab("OD.600")
cshl.plot.OD
ggsave("repeat-sunday-OD.png")

cshl.plot.GFP <- ggplot(repeat.sunday, aes(green.intensity, GFP))
cshl.plot.GFP=cshl.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity ") +
  xlab("Green Intensity") +
  ylab("GFP") +
  geom_smooth(method = "loess")
cshl.plot.GFP
ggsave("repeat-sunday-GFP.png")


cshl.plot.GFP.row <- ggplot(repeat.sunday, aes(factor(row), GFP))
cshl.plot.GFP.row=cshl.plot.GFP.row +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP by row ") +
  xlab("Row") +
  ylab("GFP")
cshl.plot.GFP.row
ggsave("repeat-sunday-GFP-row.png")

cshl.plot.OD.row <- ggplot(repeat.sunday, aes(factor(row), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD by row ") +
  xlab("Row") +
  ylab("OD.600")
cshl.plot.OD.row
ggsave("repeat-sunday-OD-row.png")

cshl.plot.GFP.column <- ggplot(repeat.sunday, aes(factor(column), GFP)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="GFP vs Intensity by column ") +
  xlab("Column") +
  ylab("GFP")
cshl.plot.GFP.column
ggsave("repeat-sunday-GFP-column.png")


cshl.plot.OD.column <- ggplot(repeat.sunday, aes(factor(column), OD.600)) +
  geom_boxplot() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs Intensity by column ") +
  xlab("Column") +
  ylab("OD.600")
cshl.plot.OD.column
ggsave("repeat-sunday-OD-column.png")

cshl.plot.OD.vs.GFP <- ggplot(repeat.sunday, aes(GFP, OD.600)) +
  geom_point() +
  facet_grid(.~plate) +
  ggtitle(label="OD vs GFP  ") +
  xlab("Column") +
  ylab("OD.600")
cshl.plot.OD.vs.GFP
ggsave("repeat-sunday-ODvsGFP.png")

#step-up-plots----
cshl.plot.GFP <- ggplot(step.up, aes(time, GFP))
cshl.plot.GFP=cshl.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="GFP vs Time by Intensity") +
  xlab("Time") +
  ylab("GFP") +
  geom_smooth(method = "loess")
cshl.plot.GFP
ggsave("step-up-GFP.png")

cshl.plot.GFP <- ggplot(step.up, aes(time, OD))
cshl.plot.GFP=cshl.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="OD vs Time by Intensity") +
  xlab("Time") +
  ylab("GFP") +
  geom_smooth(method = "loess")
cshl.plot.GFP
ggsave("step-up-OD.png")

#step-off-plots----
cshl.plot.GFP <- ggplot(step.down, aes(time, GFP))
cshl.plot.GFP=cshl.plot.GFP +
  geom_point() +
  #scale_x_discrete(limits=c("mock","MeJA")) +
  facet_grid(.~green.intensity) +
  ggtitle(label="GFP vs Time by Intensity - step off") +
  xlab("Time") +
  ylab("GFP") +
  geom_smooth(method = "loess")
cshl.plot.GFP
ggsave("step-off-GFP.png")