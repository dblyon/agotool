df = read.csv("/Users/dblyon/modules/cpr/agotool/app/python/df_etype_2_pval_LOG.txt", sep="\t")
p <- ggplot(data=df, aes(x=pval, color=random)) + geom_density(alpha=0.4) + facet_grid(etype ~ .)
p  
ggsave("/Users/dblyon/SynologyDrive/UZH/Presentations/BIG_group_meeting/KS_pvals_density.png", last_plot())
#####
df = read.csv("/Users/dblyon/modules/cpr/agotool/data/exampledata/Example_1_Yeast_acetylation_abundance_correction.txt", sep="\t")
ggplot(data=df, aes(x=Intensity)) + geom_histogram(bins=12, color="black", fill="#F8766D") + 
  theme(panel.background = element_blank()) + 
  labs(x="Protein abundance", y="Count") +
  theme(axis.text=element_text(size=12), axis.title=element_text(size=46)) +
  theme(axis.ticks.x=element_blank(), axis.ticks.y=element_blank()) +
  theme(axis.line=element_blank(),axis.text.x=element_blank(),
        axis.text.y=element_blank(),axis.ticks=element_blank(),
        legend.position="none",
        panel.background=element_blank(),panel.border=element_blank(),panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),plot.background=element_blank())
ggsave("/Users/dblyon/SynologyDrive/UZH/Presentations/BIG_group_meeting/AbundanceCorrection_Hist_1.png", last_plot())

df = read.csv("/Users/dblyon/SynologyDrive/UZH/Presentations/BIG_group_meeting/DF_2_plot_abundance_correction.txt", sep="\t")
ggplot(data=df, aes(x=Intensity, fill=FG_BG)) + geom_histogram(bins=12, color="black") #+ 
  theme(panel.background = element_blank()) + 
  labs(x="Protein abundance", y="Count") +
  theme(axis.text=element_text(size=12), axis.title=element_text(size=46)) +
  theme(axis.ticks.x=element_blank(), axis.ticks.y=element_blank()) +
  theme(axis.line=element_blank(),axis.text.x=element_blank(),
        axis.text.y=element_blank(),axis.ticks=element_blank(),
        panel.background=element_blank(),panel.border=element_blank(),panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),plot.background=element_blank()) +
  theme(legend.text=element_text(size=22))
ggsave("/Users/dblyon/SynologyDrive/UZH/Presentations/BIG_group_meeting/AbundanceCorrection_Hist_2_wrong.png", last_plot())



