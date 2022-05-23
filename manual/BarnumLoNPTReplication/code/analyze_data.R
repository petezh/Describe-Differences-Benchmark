######################################################################
## Produce all Main Text Figures and Tables and all Appendix Figures except fig. 8
## (for fig. 8, see "wordshoals.R")
## Miriam Barnum and James Lo
## September 16, 2019
######################################################################

#setwd("~/Dropbox/npt/data")
load("merged_final.Rdata")

dim(ts)			# N = 553 documents
length(unique(ts$year))	# T=13 conferences
length(unique(ts$country))  #I = 123 unique countries

table(ts$country, ts$year)

yearcount <- table(ts$year)
mean(yearcount[c(1,3,7,11)])
mean(yearcount[c(-1,-3,-7, -11)])

cor(ts$theta, ts$Idealpoint, use="pairwise")	#0.74 overall
cor(ts$theta[ts$nws==1], ts$Idealpoint[ts$nws==1], use="pairwise")	#0.53 overall
cor(ts$theta[ts$nws==0], ts$Idealpoint[ts$nws==0], use="pairwise")	#0.76 overall

years <- unique(ts$year)
for(i in 1:length(years)){
  cat(years[i], ":", cor( ts$theta[ts$year==years[i]], ts$Idealpoint[ts$year==years[i]], use="pairwise"), "\n")
}

#############
## Figure 1
#############

# df just for 2015
thetaplot <- ts[ts$year==2015,]

library(tools)
thetaplot$country <- toTitleCase(as.character(thetaplot$country))
thetaplot$country[thetaplot$country == "Uk"] <- "United Kingdom"
thetaplot$country[thetaplot$country == "Usa"] <- "United States"

# plot thetas
require(ggplot2)
pdf("../npt paper/pdf/thetas.pdf")
ggplot(thetaplot, aes(x=reorder(country, theta), y=theta, ymin=UB, ymax=LB)) + 
  geom_pointrange() + theme_bw(base_size = 14) + coord_flip() + 
  ylab('Estimated policy position') + xlab('') 
dev.off()


# screeplot
load("wfpool.Rdata")

x <- prcomp(wfpool@x)
pcs <- x$sdev^2

pdf("../npt paper/pdf/screeplot.pdf")
#screeplot(prcomp(wfpool@x), type = 'lines', main ='', ylim = c(0,600), cex.lab = 1.2, font.main = 1)
plot(1:10, pcs[1:10], type = "b", xlab = "Dimension", ylab = "Eigenvalue", cex.lab = 1.3, xaxt='n')
axis(1, at = 1:10)
dev.off()

#############
## Figure 2
#############

wfpool@beta <- -1 * wfpool@beta

pdf("../npt paper/pdf/new_gd_features.pdf")
textplot_scale1d(wfpool, margin = "features", highlighted = c('reprocess', 'enrich','shut','sensit', 'reactor', 
                                                              'uranium','black','loophol', 'noncompli', 'intermediate-rang',
                                                              'ballist', 'crise', 'provoc', 'unscr','fmct','ap','suppli',
                                                              'weapons-grad',
                                                              'icj', 'inhuman', 'non-discrimin', 'contravent', 'preferenti',
                                                              'reinterpret','court','horizont', 'vertic','advisori',
                                                              'justic','perpetu','court','discriminatori','select', 
                                                              'indefinit', 'imbal','systemat','surviv')) + 
  xlab(expression(paste("Estimated ", beta))) +
  ylab(expression(paste("Estimated ", psi)))
dev.off()

#############
## Figure 3
#############

pdf("../npt paper/pdf/convergent.pdf")
plot(ts$theta, ts$Idealpoint, main="",
     xlim=c(-2,2.5), ylim=c(-2,3),
     cex.lab=1.4,
     type="n",
     xlab="NPT policy positions",
     ylab="UNGA ideal points")
points(ts$theta[ts$nws==0], ts$Idealpoint[ts$nws==0], col="lightgrey", pch=20, cex=1.6)
points(ts$theta[ts$nws==1], ts$Idealpoint[ts$nws==1], col="black", pch=18, cex=1.9)
text(-1.5, 2.5, "r = 0.76", cex=1.6)
dev.off()

#############
## Table 1
#############

library(stargazer)
latent <- ts[,c("theta","nws","stoll","n_cap7","fuhrmann.lab")]
cor(latent, use="pairwise")
stargazer(cor(latent, use="pairwise"))

#############
## Table 2
#############

## nuclear status
summary(nws.model <- lm(nws ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))

## Jo and Gartzke latent
summary(ncap7.model <- lm(n_cap7 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
summary(glm(n_cap7 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts, family=poisson(link="log")))
summary(glm(n_cap7 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts, family=quasipoisson(link="log")))

## Robust to collapsing of data
ncap <- by(ts$n_cap7t, ts$ccode, mean, na.rm=TRUE)
gdmean <- by(ts$gdtheta, ts$ccode, mean, na.rm=TRUE)
summary(glm(ncap ~ gdmean, data=ts))

# stoll capacity
summary(stoll.model <- lm(stoll ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
summary(glm(stoll ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts, family=poisson(link="log")))
summary(glm(stoll ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts, family=quasipoisson(link="log")))

# imputed stoll
summary(lm(stoll.imputed ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))

# fuhrmann lab
summary(fmann.lmodel <- lm(fuhrmann.lab ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
summary(glm(fuhrmann.lab ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts, family=binomial(link="probit")))

# fuhrmann pilot
summary(fmann.pmodel <- lm(fuhrmann.pilot ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
summary(glm(fuhrmann.pilot ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts, family=binomial(link="probit")))

# output table
stargazer(nws.model, stoll.model, ncap7.model, fmann.lmodel)

#############
## Figure 4
#############

# Estimates for 7 topic LDA
r1 <- summary(lm(topic1 ~ theta, data=ts))	
r2 <- summary(lm(topic2 ~ theta, data=ts))	
r3 <- summary(lm(topic3 ~ theta, data=ts))	
r4 <- summary(lm(topic4 ~ theta, data=ts))	
r5 <- summary(lm(topic5 ~ theta, data=ts))	
r6 <- summary(lm(topic6 ~ theta, data=ts))	
r7 <- summary(lm(topic7 ~ theta, data=ts))	

t1 <- summary(lm(topic1 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	
t2 <- summary(lm(topic2 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	
t3 <- summary(lm(topic3 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	
t4 <- summary(lm(topic4 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	
t5 <- summary(lm(topic5 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	
t6 <- summary(lm(topic6 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	
t7 <- summary(lm(topic7 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))	

modelcoef <- c(t1$coefficients[2,1], t2$coefficients[2,1], t3$coefficients[2,1],
               t4$coefficients[2,1], t5$coefficients[2,1], t6$coefficients[2,1],
               t7$coefficients[2,1])

modelse <- c(t1$coefficients[2,2], t2$coefficients[2,2], t3$coefficients[2,2],
             t4$coefficients[2,2], t5$coefficients[2,2], t6$coefficients[2,2],
             t7$coefficients[2,2])

ylo <- modelcoef - 1.96*(modelse)
yhi <- modelcoef + 1.96*(modelse)

names <- c("Conference process", "Strengthening the regime", "Non-proliferation", "NWFZ",
           "Cooperation", "Disarmament", "Progress")

dfplot1 <- data.frame(names, modelcoef, modelse, ylo, yhi, model = "with controls")

modelcoef <- c(r1$coefficients[2,1], r2$coefficients[2,1], r3$coefficients[2,1],
               r4$coefficients[2,1], r5$coefficients[2,1], r6$coefficients[2,1],
               r7$coefficients[2,1])

modelse <- c(r1$coefficients[2,2], r2$coefficients[2,2], r3$coefficients[2,2],
             r4$coefficients[2,2], r5$coefficients[2,2], r6$coefficients[2,2],
             r7$coefficients[2,2])

ylo <- modelcoef - 1.96*(modelse)
yhi <- modelcoef + 1.96*(modelse)

dfplot2 <- data.frame(names, modelcoef, modelse, ylo, yhi, model = "no controls")

dfplot <- rbind(dfplot1, dfplot2)

require(ggplot2)
pdf("../npt paper/pdf/topics7.pdf")
ggplot(dfplot, aes(colour = model)) + 
  geom_hline(yintercept = 0, lty = 2) + 
  geom_pointrange(aes(x = reorder(names, seq(length(names),1,-1)), 
                      y = modelcoef, ymin = ylo, ymax = yhi), position = position_dodge(width = 1/4)) + 
  scale_color_manual(values = c('black', 'darkgrey'), guide = F) +
  ylab('Estimated OLS coefficient') + xlab('') +
  coord_flip() + theme_bw(base_size = 14)
dev.off()

# Estimates for 11 topic LDA
r1 <- summary(lm(XItopic1 ~ theta, data=ts))
r2 <- summary(lm(XItopic2 ~ theta, data=ts))	
r3 <- summary(lm(XItopic3 ~ theta, data=ts))
r4 <- summary(lm(XItopic4 ~ theta, data=ts))
r5 <- summary(lm(XItopic5 ~ theta, data=ts))
r6 <- summary(lm(XItopic6 ~ theta, data=ts))
r7 <- summary(lm(XItopic7 ~ theta, data=ts))
r8 <- summary(lm(XItopic8 ~ theta, data=ts))	
r9 <- summary(lm(XItopic9 ~ theta, data=ts))
r10 <- summary(lm(XItopic10 ~ theta, data=ts))	
r11 <- summary(lm(XItopic11 ~ theta, data=ts))

t1 <- summary(lm(XItopic1 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t2 <- summary(lm(XItopic2 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t3 <- summary(lm(XItopic3 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t4 <- summary(lm(XItopic4 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t5 <- summary(lm(XItopic5 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t6 <- summary(lm(XItopic6 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t7 <- summary(lm(XItopic7 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t8 <- summary(lm(XItopic8 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t9 <- summary(lm(XItopic9 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t10 <- summary(lm(XItopic10 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))
t11 <- summary(lm(XItopic11 ~ theta + Idealpoint + polity2 + gdppc_WDI_PW + unsc_region, data=ts))

modelcoef <- c(t1$coefficients[2,1], t2$coefficients[2,1], t3$coefficients[2,1],
               t4$coefficients[2,1], t5$coefficients[2,1], t6$coefficients[2,1],
               t7$coefficients[2,1], t8$coefficients[2,1], t9$coefficients[2,1], 
               t10$coefficients[2,1], t11$coefficients[2,1])

modelse <- c(t1$coefficients[2,2], t2$coefficients[2,2], t3$coefficients[2,2],
             t4$coefficients[2,2], t5$coefficients[2,2], t6$coefficients[2,2],
             t7$coefficients[2,2], t8$coefficients[2,2], t9$coefficients[2,2], 
             t10$coefficients[2,2], t11$coefficients[2,2])

ylo <- modelcoef - 1.96*(modelse)
yhi <- modelcoef + 1.96*(modelse)

names <- c("Progress", "NWFZ", "Disarmament", "Strengthening the regime", "NNWS concerns", "Conference process","Cooperation", 
           "Non-proliferation", "Middle East NWFZ", "Safeguards", "Humanitarian impacts")

dfplot1 <- data.frame(names, modelcoef, modelse, ylo, yhi, model = "with controls")

modelcoef <- c(r1$coefficients[2,1], r2$coefficients[2,1], r3$coefficients[2,1],
               r4$coefficients[2,1], r5$coefficients[2,1], r6$coefficients[2,1],
               r7$coefficients[2,1], r8$coefficients[2,1], r9$coefficients[2,1],
               r10$coefficients[2,1], r11$coefficients[2,1])

modelse <- c(r1$coefficients[2,2], r2$coefficients[2,2], r3$coefficients[2,2],
             r4$coefficients[2,2], r5$coefficients[2,2], r6$coefficients[2,2],
             r7$coefficients[2,2], r8$coefficients[2,2], r9$coefficients[2,2], 
             r10$coefficients[2,2], r11$coefficients[2,2])

ylo <- modelcoef - 1.96*(modelse)
yhi <- modelcoef + 1.96*(modelse)

dfplot2 <- data.frame(names, modelcoef, modelse, ylo, yhi, model = "no controls")

dfplot <- rbind(dfplot1, dfplot2)

require(ggplot2)
pdf("../npt paper/pdf/topics11.pdf")
ggplot(dfplot, aes(colour = model)) + 
  geom_hline(yintercept = 0, lty = 2) + 
  geom_pointrange(aes(x = reorder(names, seq(length(names),1,-1)), 
                      y = modelcoef, ymin = ylo, ymax = yhi), position = position_dodge(width = 1/2)) + 
  scale_color_manual(values = c('black', 'darkgrey'), guide = F) +
  ylab('Estimated OLS coefficient') + xlab('') +
  coord_flip() + theme_bw(base_size = 14)
dev.off()

#############
## Figure 5
#############

# setup for confidence interval on all time-series plots, including those in the appendix
load("bootstrap.Rdata")
rm(boot.beta)

boot.omega <- as.data.frame(boot.omega * (-1))
boot.omega$year <- ts$year

ci.nws <- aggregate(. ~ year, boot.omega[ts$nws==1,], mean)
ci.nnws <- aggregate(. ~ year, boot.omega[ts$nws==0,], mean)
ci.allies <- aggregate(. ~ year, boot.omega[ts$nws==0 & ts$defense == 1,], mean)
ci.nonallies <- aggregate(. ~ year, boot.omega[ts$nws==0 & ts$defense == 0,], mean)

lb.nws <- rep(NA,13)
ub.nws <- rep(NA,13)
lb.nnws <- rep(NA,13)
ub.nnws <- rep(NA,13)
lb.allies <- rep(NA,13)
ub.allies <- rep(NA,13)
lb.nonallies <- rep(NA,13)
ub.nonallies <- rep(NA,13)

for(i in 1:13){
  lb.nws[i] <- quantile(ci.nws[i,2:101],0.025)
  ub.nws[i] <- quantile(ci.nws[i,2:101],0.975)
  lb.nnws[i] <- quantile(ci.nnws[i,2:101],0.025)
  ub.nnws[i] <- quantile(ci.nnws[i,2:101],0.975)
  lb.allies[i] <- quantile(ci.allies[i,2:101],0.025)
  ub.allies[i] <- quantile(ci.allies[i,2:101],0.975)
  lb.nonallies[i] <- quantile(ci.nonallies[i,2:101],0.025)
  ub.nonallies[i] <- quantile(ci.nonallies[i,2:101],0.975)
}

years <- unique(ts$year)
poly_yr <- c(years[order(years)], years[order(-years)]) #years forward and backward for plotting CI polygon


# figure 5, left panel
pdf("../npt paper/pdf/ts_plots.pdf")
plot(ts$year, ts$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT policy positions", main = "", xlim=c(2000,2020), cex.lab=1.4)
polygon(poly_yr,c(unlist(lb.nws), unlist(ub.nws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "black", lty=2)
polygon(poly_yr,c(unlist(lb.nnws), unlist(ub.nnws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
points(ts$year[ts$nws==0], ts$theta[ts$nws==0], col="darkgrey", pch=20, cex=1.6)
lines(aggregate(theta ~ year, ts[ts$nws==0,], mean), col="darkgrey", lwd = 3, lty=2)
points(ts$year[ts$nws==1], ts$theta[ts$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(theta ~ year, ts[ts$nws==1,], mean), col="black", lwd = 3)
#axis(side=1,at=seq(2000,2018,1))
dev.off()

# figure 7 (online appendix), left panel
pdf("../reviewer memo/pdf/allies.pdf")
plot(ts$year, ts$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT policy positions", main = "", xlim=c(2000,2020), cex.lab=1.4)
polygon(poly_yr,c(unlist(lb.nonallies), unlist(ub.nonallies[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
polygon(poly_yr,c(unlist(lb.allies), unlist(ub.allies[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
polygon(poly_yr,c(unlist(lb.nws), unlist(ub.nws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "black", lty=2)
points(ts$year[ts$nws==0 & ts$defense == 0], ts$theta[ts$nws==0 & ts$defense == 0], col="darkgrey", pch=20, cex=1.6)
points(ts$year[ts$nws==0 & ts$defense == 1], ts$theta[ts$nws==0 & ts$defense == 1], col="black", pch=1, cex=1.2)
lines(aggregate(theta ~ year, ts[ts$nws==0 & ts$defense == 1,], mean), col="black", lwd = 2, lty =2)
points(ts$year[ts$nws==1], ts$theta[ts$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(theta ~ year, ts[ts$nws==1,], mean), col="black", lwd = 3)
lines(aggregate(theta ~ year, ts[ts$nws==0 & ts$defense == 0,], mean), col="gray35", lwd = 3, lty=2)
legend("topleft", legend = c("NWS", "Allies", "Other NNWS"), bty = "n",
       lwd = c(3,2,3), cex = 1.25, col = c("black", "black", "gray35"), lty = c(1,2,2), pch = c(18, 1, 20), pt.cex = c(1.6,1.2,1.6))
dev.off()

# figure 6 (online appendix), left panel
yr <- years[order(years)]

diff <- ci.nws - ci.nnws
lb.diff <- rep(NA,13)
ub.diff <- rep(NA,13)
for(i in 1:13){
  lb.diff[i] <- quantile(diff[i,2:101],0.025)
  ub.diff[i] <- quantile(diff[i,2:101],0.975)
}

# difference plot
pdf("../reviewer memo/pdf/diff.pdf")
plot(ts$year, ts$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NWS mean - NNWS mean", main = "", xlim=c(2000,2020), cex.lab=1.4)
lines(years[order(years)], (aggregate(theta ~ year, ts[ts$nws==1,], mean)$theta - aggregate(theta ~ year, ts[ts$nws==0,], mean)$theta), col="black", lwd = 3)
polygon(poly_yr,c(unlist(lb.diff), unlist(ub.diff[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
#axis(side=1,at=seq(2000,2018,1))
dev.off()

#################
# restrict to to countries present in every year
tab <- data.frame(table(ts$ccode))
ts_comp <- merge(ts,tab, by.x="ccode",by.y="Var1")
ts_comp <- ts_comp[ts_comp$Freq==13,]
ts_comp <- ts_comp[order(ts_comp$year),]

boot.omega$ccode <- ts$ccode
boot.comp <- merge(boot.omega,tab, by.x="ccode",by.y="Var1")
boot.comp <- boot.comp[boot.comp$Freq==13,]
boot.comp <- boot.comp[order(boot.comp$year),]

ci.nws <- aggregate(. ~ year, boot.comp[ts_comp$nws==1,], mean)
ci.nnws <- aggregate(. ~ year, boot.comp[ts_comp$nws==0,], mean)
ci.allies <- aggregate(. ~ year, boot.comp[ts_comp$nws==0 & ts_comp$defense == 1,], mean)

for(i in 1:13){
  lb.nws[i] <- quantile(ci.nws[i,3:102],0.025)
  ub.nws[i] <- quantile(ci.nws[i,3:102],0.975)
  lb.nnws[i] <- quantile(ci.nnws[i,3:102],0.025)
  ub.nnws[i] <- quantile(ci.nnws[i,3:102],0.975)
  lb.allies[i] <- quantile(ci.allies[i,3:102],0.025)
  ub.allies[i] <- quantile(ci.allies[i,3:102],0.975)
}
#################

# figure 5, right panel
pdf("../npt paper/pdf/ts_complete.pdf")
plot(ts_comp$year, ts_comp$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT policy positions", main = "", xlim=c(2000,2020), cex.lab=1.4)
polygon(poly_yr,c(unlist(lb.nws), unlist(ub.nws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "black", lty=2)
polygon(poly_yr,c(unlist(lb.nnws), unlist(ub.nnws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
points(ts_comp$year[ts_comp$nws==0], ts_comp$theta[ts_comp$nws==0], col="darkgrey", pch=20, cex=1.6)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==0,], mean), col="darkgrey", lwd = 3, lty=2)
points(ts_comp$year[ts_comp$nws==1], ts_comp$theta[ts_comp$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==1,], mean), col="black", lwd = 3)
dev.off()

# figure 7 (online appendix), right panel
pdf("../reviewer memo/pdf/allies_complete.pdf") # 2 nws, 3 nws allies
plot(ts_comp$year, ts_comp$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT policy positions", main = "", xlim=c(2000,2020), cex.lab=1.4)
polygon(poly_yr, c(unlist(lb.nnws), unlist(ub.nnws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
polygon(poly_yr, c(unlist(lb.nws), unlist(ub.nws[13:1])), col = rgb(0,0,0,alpha=0.1), border = "black", lty=2)
points(ts_comp$year[ts_comp$nws==0 & ts_comp$defense == 0], ts_comp$theta[ts_comp$nws==0 & ts_comp$defense == 0], col="darkgrey", pch=20, cex=1.6)
points(ts_comp$year[ts_comp$nws==0 & ts_comp$defense == 1], ts_comp$theta[ts_comp$nws==0 & ts_comp$defense == 1], col="black", pch=1, cex=1.2)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==0 & ts_comp$defense == 1,], mean), col="black", lwd = 2, lty =2)
points(ts_comp$year[ts_comp$nws==1], ts_comp$theta[ts_comp$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==1,], mean), col="black", lwd = 3)
#legend("topleft", legend = c("NWS", "Allies", "Other NNWS"), bty = "n",
#       lwd = c(3,2,3), cex = 1, col = c("black", "black", "gray35"), lty = c(1,2,2), pch = c(18, 1, 20), pt.cex = c(1.6,1.2,1.6))
#lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==0 & ts_comp$defense == 0,], mean), col="gray35", lwd = 3, lty=2)
#axis(side=1,at=seq(2000,2018,1))
dev.off()

# figure 6 (online appendix), right panel
# difference plot
diff <- ci.nws - ci.nnws
lb.diff <- rep(NA,13)
ub.diff <- rep(NA,13)
for(i in 1:13){
  lb.diff[i] <- quantile(diff[i,3:102],0.025)
  ub.diff[i] <- quantile(diff[i,3:101],0.975)
}

pdf("../reviewer memo/pdf/diff_complete.pdf")
plot(ts$year, ts$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NWS mean - NNWS mean", main = "", xlim=c(2000,2020), cex.lab=1.4)
lines(years[order(years)], (aggregate(theta ~ year, ts_comp[ts_comp$nws==1,], mean)$theta - aggregate(theta ~ year, ts_comp[ts_comp$nws==0,], mean)$theta), col="black", lwd = 3)
polygon(poly_yr,c(unlist(lb.diff), unlist(ub.diff[13:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
#axis(side=1,at=seq(2000,2018,1))
dev.off()

#################
# restrict to to countries present in every  RevCon year
tmp <- ts[ts$year %in% c(2000,2005,2010,2015),]
tab <- data.frame(table(tmp$ccode))
ts_comp <- merge(tmp,tab, by.x="ccode",by.y="Var1")
ts_comp <- ts_comp[ts_comp$Freq==4,]

tmp <- boot.omega[boot.omega$year %in% c(2000,2005,2010,2015),]
boot.comp <- merge(tmp,tab, by.x="ccode",by.y="Var1")
boot.comp <- boot.comp[boot.comp$Freq==4,]

ci.nws <- aggregate(. ~ year, boot.comp[ts_comp$nws==1,], mean)
ci.nnws <- aggregate(. ~ year, boot.comp[ts_comp$nws==0,], mean)
ci.allies <- aggregate(. ~ year, boot.comp[ts_comp$nws==0 & ts_comp$defense == 1,], mean)
ci.nonallies <- aggregate(. ~ year, boot.comp[ts_comp$nws==0 & ts_comp$defense == 0,], mean)

lb.nws <- rep(NA,4)
ub.nws <- rep(NA,4)
lb.nnws <- rep(NA,4)
ub.nnws <- rep(NA,4)
lb.allies <- rep(NA,4)
ub.allies <- rep(NA,4)
lb.nonallies <- rep(NA,4)
ub.nonallies <- rep(NA,4)

for(i in 1:4){
  lb.nws[i] <- quantile(ci.nws[i,3:102],0.025)
  ub.nws[i] <- quantile(ci.nws[i,3:102],0.975)
  lb.nnws[i] <- quantile(ci.nnws[i,3:102],0.025)
  ub.nnws[i] <- quantile(ci.nnws[i,3:102],0.975)
  lb.allies[i] <- quantile(ci.allies[i,3:102],0.025)
  ub.allies[i] <- quantile(ci.allies[i,3:102],0.975)
  lb.nonallies[i] <- quantile(ci.nonallies[i,3:102],0.025)
  ub.nonallies[i] <- quantile(ci.nonallies[i,3:102],0.975)
}
#################

# figure 5, center panel
pdf("../npt paper/pdf/ts_complete_revcons.pdf")
plot(ts_comp$year, ts_comp$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT policy positions", main = "", xlim=c(2000,2020), cex.lab=1.4)
polygon(c(2000,2005,2010,2015,2015,2010,2005,2000),c(unlist(lb.nnws), unlist(ub.nnws[4:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
polygon(c(2000,2005,2010,2015,2015,2010,2005,2000),c(unlist(lb.nws), unlist(ub.nws[4:1])), col = rgb(0,0,0,alpha=0.1), border = "black", lty=2)
points(ts_comp$year[ts_comp$nws==0], ts_comp$theta[ts_comp$nws==0], col="darkgrey", pch=20, cex=1.6)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==0,], mean), col="darkgrey", lwd = 3, lty=2)
points(ts_comp$year[ts_comp$nws==1], ts_comp$theta[ts_comp$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==1,], mean), col="black", lwd = 3)
dev.off()

# figure 7 (online appendix), center panel
pdf("../reviewer memo/pdf/allies_revcons.pdf") # 3 nws, 7 nws allies, 6 nnws (non-allies)
plot(ts_comp$year, ts_comp$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT policy positions", main = "", xlim=c(2000,2020), cex.lab=1.4)
polygon(c(2000,2005,2010,2015,2015,2010,2005,2000),c(unlist(lb.nonallies), unlist(ub.nonallies[4:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
polygon(c(2000,2005,2010,2015,2015,2010,2005,2000),c(unlist(lb.allies), unlist(ub.allies[4:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
polygon(c(2000,2005,2010,2015,2015,2010,2005,2000),c(unlist(lb.nws), unlist(ub.nws[4:1])), col = rgb(0,0,0,alpha=0.1), border = "black", lty=2)
points(ts_comp$year[ts_comp$nws==0 & ts_comp$defense == 0], ts_comp$theta[ts_comp$nws==0 & ts_comp$defense == 0], col="darkgrey", pch=20, cex=1.6)
points(ts_comp$year[ts_comp$nws==0 & ts_comp$defense == 1], ts_comp$theta[ts_comp$nws==0 & ts_comp$defense == 1], col="black", pch=1, cex=1.2)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==0 & ts_comp$defense == 1,], mean), col="black", lwd = 2, lty =2)
points(ts_comp$year[ts_comp$nws==1], ts_comp$theta[ts_comp$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==1,], mean), col="black", lwd = 3)
lines(aggregate(theta ~ year, ts_comp[ts_comp$nws==0 & ts_comp$defense == 0,], mean), col="gray35", lwd = 3, lty=2)
#legend("topleft", legend = c("NWS", "Allies", "Other NNWS"), bty = "n",
#       lwd = c(3,2,3), cex = 1, col = c("black", "black", "gray35"), lty = c(1,2,2), pch = c(18, 1, 20), pt.cex = c(1.6,1.2,1.6))
#axis(side=1,at=seq(2000,2018,1))
dev.off()

# figure 6 (online appendix), center panel
yr <- c(2000,2005,2010,2015)

diff <- ci.nws - ci.nnws
lb.diff <- rep(NA,4)
ub.diff <- rep(NA,4)
for(i in 1:4){
  lb.diff[i] <- quantile(diff[i,3:102],0.025)
  ub.diff[i] <- quantile(diff[i,3:102],0.975)
}

# difference plot
pdf("../reviewer memo/pdf/diff_revcons.pdf")
plot(ts_comp$year, ts_comp$theta, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NWS mean - NNWS mean", main = "", xlim=c(2000,2020), cex.lab=1.4)
lines(yr, (aggregate(theta ~ year, ts_comp[ts_comp$nws==1,], mean)$theta - aggregate(theta ~ year, ts_comp[ts_comp$nws==0,], mean)$theta), col="black", lwd = 3)
polygon(c(2000,2005,2010,2015,2015,2010,2005,2000),c(unlist(lb.diff), unlist(ub.diff[4:1])), col = rgb(0,0,0,alpha=0.1), border = "darkgrey", lty=2)
#axis(side=1,at=seq(2000,2018,1))
dev.off()