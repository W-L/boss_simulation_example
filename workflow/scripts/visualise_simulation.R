library(ggplot2)
library(argparse)
library(dplyr)
library(patchwork)

theme_set(theme_minimal())


ptol_10 <- c(
  "#332288",
  "#88CCEE",
  "#44AA99",
  "#117733",
  "#999933",
  "#DDCC77",
  "#661100",
  "#CC6677",
  "#882255",
  "#AA4499"
)

nrow <- 2


get_arguments <- function() {
  parser <- argparse::ArgumentParser()
  parser$add_argument('--input_cov', required = TRUE)
  parser$add_argument('--input_unb', required = TRUE)
  parser$add_argument('--output', required = TRUE)
  args<- parser$parse_args()
  return(args)
}


# get the arguments for input and output files
args <- get_arguments()
input_cov <- args$input_cov
input_unb <- args$input_unb
output <- args$output



# load the coverage data
cov <- read.csv(input_cov)
# cond, time, otu, mean_coverage, low_coverage_prop
# get the ordering of the OTUs
otu_order <- cov %>%
  filter(cond == 'control', time == max(time)) %>%
  arrange(desc(mean_coverage)) %>%
  pull(otu)
# reorder factor levels
cov$otu <- factor(cov$otu, levels=otu_order)


# load the unblocking data and reorder the factor levels
unb <- read.csv(input_unb)
unb$otu <- factor(unb$otu, levels=otu_order)
unb_cond <- unb %>% filter(cond == "boss")




# create plots

unb_plot <- ggplot(
    data=unb_cond,
    mapping=aes(x=time, y=unb_ratio, color=otu, group=otu)) +
  geom_line(linewidth=1) +
  geom_point() +
  scale_color_manual(values=ptol_10) +
  ylab("prop. rejected reads") +
  theme(legend.position = "none")
# unb_plot

nreads <- ggplot(
    data=unb,
    mapping=aes(x=time, y=total, linetype=cond, colour=otu)) +
  geom_line(linewidth=1) +
  facet_wrap(~otu, scales="free_y", nrow = nrow) +
  scale_color_manual(values=ptol_10, guide = "none") +
  ylab("# reads")
# nreads

meanc <- ggplot(
    data=cov,
    mapping=aes(x=time, y=mean_coverage, linetype=cond, colour=otu)) +
  geom_line(linewidth=1) +
  facet_wrap(~otu, scales="free_y", nrow = nrow) +
  scale_color_manual(values=ptol_10, guide = "none") +
  ylab("mean coverage")
# meanc

lowc <- ggplot(
    data=cov,
    mapping=aes(x=time, y=low_coverage_prop, linetype=cond, colour=otu)) +
  geom_line(linewidth=1) +
  facet_wrap(~otu, scales="free_y", nrow = nrow) +
  scale_color_manual(values=ptol_10, guide = "none") +
  ylab("prop. sites at <5x")
# lowc



layout <- ((unb_plot | nreads) / (meanc | lowc) / guide_area()) +
  plot_annotation(tag_levels = "A") +
  plot_layout(guides="collect", heights=c(1, 1, 0.3)) &
  xlab("seq. time (intervals)") &
  theme(
    legend.position = "bottom",
    legend.title = element_blank(),
    strip.text.x = element_blank()
  )


ggsave(output, layout, w=15, h=8)








