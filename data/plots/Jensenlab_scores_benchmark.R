library(ggplot2)
library(wesanderson)
library(reshape2)
library(reshape)
library(plyr)
library(scales)
library(RColorBrewer)
library(gridExtra)
library(extrafont)
library(grid)
library(dendsort)
### R color brewer
# http://colorbrewer2.org/?type=qualitative&scheme=Dark2&n=3
# df$function_type = factor(df$etype, levels=c(-25, -26, -20), labels=c("BTO tissues", "DOID diseases", "GO-CC"))
### 
#fn2plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_overview_1.txt"
#df <- read.csv(fn2plot, sep="\t", header=TRUE)
#df$function_type = factor(df$etype, levels=c(-25, -26, -20), labels=c("BTO tissues", "DOID diseases", "GO-CC"))
#plt <- ggplot(aes(x=score_cutoff, y=counts), data=df) + geom_col() + facet_grid(. ~ function_type)
#plt + labs(title="Number of terms @ varying score_cutoffs") + ylab("number of significant terms") + theme(plot.title = element_text(hjust = 0.5))
#fn_plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_scoreCutoff_vs_counts_facetEtype.png"
#ggsave(fn_plot, plot=last_plot()) #, width=12, height=9)
###
#fn2plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_overview_significant.txt"
#df <- read.csv(fn2plot, sep="\t", header=TRUE)
#df$function_type = factor(df$etype, levels=c(-25, -26, -20), labels=c("BTO tissues", "DOID diseases", "GO-CC"))
#plt <- ggplot(aes(x=score_cutoff, y=counts, fill=significant), data=df) + geom_col() + facet_grid(. ~ function_type)
#plt + labs(title="Number of terms @ varying score_cutoffs") + ylab("number of significant terms") + theme(plot.title = element_text(hjust = 0.5))
#fn_plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_scoreCutoff_vs_counts_facetEtype_fillSignificant.png"
#ggsave(fn_plot, plot=last_plot()) #, width=12, height=9)
###
fn2plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_overview_significant.txt"
df <- read.csv(fn2plot, sep="\t", header=TRUE)
df <- subset(df, df$significant == "True")
df$function_type = factor(df$etype, levels=c(-25, -26, -20), labels=c("BTO tissues", "DOID diseases", "GO-CC"))
plt <- ggplot(df, aes(fill=function_type, y=counts, x=score_cutoff)) + geom_bar(position="dodge2", stat="identity", width=0.8) + 
  scale_fill_manual(values=c('#1b9e77','#d95f02','#7570b3')) + theme(legend.position="bottom") + 
  labs(title="Number of terms depending on score_cutoffs", subtitle = "FDR <= 5%") + ylab("number of terms") + xlab("score cutoff") + 
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5), text = element_text(size=22))
plt
fn_plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_scoreCutoff_vs_counts_FDR.png"
ggsave(fn_plot, plot=last_plot()) #, width=12, height=9)

fn2plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_overview_significant.txt"
df <- read.csv(fn2plot, sep="\t", header=TRUE)
df <- subset(df, df$significant == "False")
df$function_type = factor(df$etype, levels=c(-25, -26, -20), labels=c("BTO tissues", "DOID diseases", "GO-CC"))
plt <- ggplot(df, aes(fill=function_type, y=counts, x=score_cutoff)) + geom_bar(position="dodge2", stat="identity", width=0.8) + 
  scale_fill_manual(values=c('#1b9e77','#d95f02','#7570b3')) + theme(legend.position="bottom") + 
  labs(title="Number of terms depending on score_cutoffs", subtitle = "no FDR cutoff") + ylab("number of terms") + xlab("score cutoff") + 
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5), text = element_text(size=22))
plt
fn_plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_scoreCutoff_vs_counts_noFDR.png"
ggsave(fn_plot, plot=last_plot()) #, width=12, height=9)


fn2plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Significant_count_per_file.txt"
df <- read.csv(fn2plot, sep='\t', header=TRUE)
#df <- subset(df, df$etype == "-20")
df$function_type = factor(df$etype, levels=c(-25, -26, -20), labels=c("BTO tissues", "DOID diseases", "GO-CC"))
ggplot(df, aes(x=score_cutoff, y=count, fill=function_type)) + geom_bar(stat="identity", position="dodge2")
ggplot(df, aes(x=score_cutoff, y=count, fill=function_type)) + geom_boxplot(stat="identity", position="dodge2")
ggplot(df, aes(x=score_cutoff, y=count, fill=function_type)) + geom_boxplot(position="dodge2", stat="identity", width=0.8)


ggplot(df, aes(x=score_cutoff, y=count, fill=function_type)) + geom_violin()

plt <- ggplot(df, aes(x=score_cutoff, y=count, fill=function_type)) + geom_boxplot() + 
  scale_fill_manual(values=c('#1b9e77','#d95f02','#7570b3')) + theme(legend.position="bottom") + 
  labs(title="Number of terms depending on score_cutoffs", subtitle = "no FDR cutoff") + ylab("number of terms") + xlab("score cutoff") + 
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5), text = element_text(size=22))
plt
#fn_plot <- "/Users/dblyon/modules/cpr/agotool/data/plots/Barplot_scoreCutoff_vs_counts_noFDR.png"
#ggsave(fn_plot, plot=last_plot()) #, width=12, height=9)


