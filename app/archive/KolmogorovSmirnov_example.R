require(graphics)
require(ggplot2)

x <- rnorm(50)
x+2
plot(x)
y <- runif(30)
plot(y)
# Do x and y come from the same distribution?
ks.test(x, y)
# Does x come from a shifted gamma distribution with shape 3 and rate 2?
ks.test(x+2, "pgamma", 3, 2) # two-sided, exact
ks.test(x+2, "pgamma", 3, 2, exact = FALSE)
ks.test(x+2, "pgamma", 3, 2, alternative = "gr")

# test if x is stochastically larger than x2
x2 <- rnorm(50, -1)
plot(ecdf(x), xlim = range(c(x, x2)))
plot(ecdf(x2), add = TRUE, lty = "dashed")
t.test(x, x2, alternative = "g")
wilcox.test(x, x2, alternative = "g")
ks.test(x, x2, alternative = "l")

x = c(2.7, 2.8, 2.9, 3, 3, 3, 3.1, 3.2, 3.3, 4)
y = c(1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.7, 2.8, 2.9, 3, 3, 3, 3.1, 3.2, 3.3, 4)
ks.test(x, y)
# Python scipy.stats.ks_2samp(x, y)
# Ks_2sampResult(statistic=0.6666666666666666, pvalue=0.0011406975408981323) 
# D = 0.66667, p-value = 0.002545
df <- data.frame(x=x, y=y)
ggplot(df) + stat_ecdf(aes(x, size=2), geom = "step", colour="red") + 
  stat_ecdf(aes(y, size=2), geom = "step", colour="blue")


x = c(1.1, 2.7, 2.8, 2.9, 3, 3, 3, 3.1, 3.2, 3.3, 4, 4.0, 4.0, 4.0, 4.0)
y = c(1.1, 2.7, 2.8, 2.9, 3, 3, 3, 3.1, 3.2, 3.3, 4, 4.1, 4.1, 4.3, 4.4)
ks.test(x, y)
df <- data.frame(x=x, y=y)
ggplot(df) + stat_ecdf(aes(x, size=3), geom = "step", colour="red") + stat_ecdf(aes(y, size=1), geom = "step", colour="blue")
