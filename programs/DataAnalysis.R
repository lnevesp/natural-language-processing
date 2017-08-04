library(ggplot2)

setwd("~/Dropbox/Data Science/Projects/Natural Language Process/StupidBackoff_Python/programs/log")

LogData = read.csv("./Log.csv")
LogData$Test<- with(LogData, paste0(Method, " - 0", NumJobs, " Core"))
LogData = LogData[LogData$PC=="ASUS" & LogData$Version=="Git 0.3",]

Plot01 = ggplot(LogData, aes(x=SampleTrainRate, y=Time_Total/60, colour=Test)) +
  ggtitle("Total Running Time") +
  xlab("Train Sample Rate") + 
  ylab("Time (min)") +
  labs(colour = "Method") +
  geom_line() + geom_point() + geom_smooth()

Plot02 = ggplot(LogData, aes(x=SampleTrainRate, y=Time_CreateNGram/60, colour=Test)) +
  ggtitle("Running Time - Create N-Grams") +
  xlab("Train Sample Rate") + 
  ylab("Time (min)") +
  labs(colour = "Method") +
  geom_line() + geom_point() + geom_smooth()

Plot01 + scale_color_manual(values=c("#A0522D", "#9999CC", "#FF00FF", "#483D8B",
                                     "#1E90FF", "#F4A460", "#7FFFD4", "#000000", "#FF4500"))
Plot02 + scale_color_manual(values=c("#A0522D", "#9999CC", "#FF00FF", "#483D8B",
                                     "#1E90FF", "#F4A460", "#7FFFD4", "#000000", "#FF4500"))