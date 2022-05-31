######################################################################
## Wordshoals Estimates, Figure 8 (online appendix)
## Miriam Barnum and James Lo
## September 16, 2019
######################################################################

#setwd("~/Dropbox/npt/code")
set.seed(123)

library(wordshoal)
library(quanteda)
load("../data/deprecated/gd_corpus.RDATA")

regions <- c("europe","european","asia","asian",'africa','african','eu','nam','non-aligned', 'arab', "uk", 'uae', 'holy','ipndv','npdi','islamic','french')
swords <- c("ladies","gentlemen","chairman", 'chairperson', 'january','february','march','april','may','june','july','august',
            'september','october','november','december', "medvedev","obama", 'side-event', 'summer','th', 'o','t')

# add cowcodes
library(countrycode)
docvars(gdcorpus, "ccode") <- countrycode(docvars(gdcorpus, "country"), 'country.name','cown')

# create dfm, preprocess, same as steps taken for wordfish
dfm <- dfm(gdcorpus, remove_punct=T, remove_numbers = T, stem = T, remove=c(stopwords("english"), regions, swords))
dfm <- dfm_trim(dfm, min_docfreq = 10)

dfm@docvars$ccode[dfm@docvars$country=="serbia montenegro"] <- 345
dfm@docvars$ccode[dfm@docvars$country=="serbia"] <- 345
dfm@docvars$ccode[dfm@docvars$country=="lithuanina"] <- 368
dfm@docvars$ccode[dfm@docvars$country=="portugual"] <- 235
  
# running wordshoals
ws <- textmodel_wordshoal(dfm, groups = dfm@docvars$year, authors = dfm@docvars$ccode)
save(ws, file="../data/wordshoal.RDATA")

df <- data.frame(ccode = ws$authors, year = ws$groups, psi = ws$psi)

years <- c(2000,2004,2005,2007,2008,2009,2010,2012,2013,2014,2015,2017,2018)
betas <- data.frame(year = years, beta = ws$beta)

df <- merge(df, betas, all.x = T)
df$position <- -df$psi * df$beta

# merge with other covariates
load("../data/merged.Rdata")
df$ccode <- as.numeric(as.character(df$ccode))
df$year <- as.numeric(as.character(df$year))
df <- merge(df, ts, by = c("ccode","year"), all.x = T)

#df$country <- countrycode(df$ccode, 'cown', 'country.name')
save(df, file="../data/wordshoal_merged.RDATA")


#############
## Figure 8 (Appendix)
#############

pdf("../figures/wordshoal_fig5_1.pdf")
plot(df$year, df$position, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT Ideal Points", main = "", xlim=c(2000,2020), cex.lab=1.4)
points(df$year[df$nws==0], df$position[df$nws==0], col="darkgrey", pch=20, cex=1.6)
lines(aggregate(position ~ year, df[df$nws==0,], mean), col="darkgrey", lwd = 3, lty=2)
points(df$year[df$nws==1], df$position[df$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(position ~ year, df[df$nws==1,], mean), col="black", lwd = 3)
#axis(side=1,at=seq(2000,2018,1))
dev.off()

# restrict to to countries present in every year
tab <- data.frame(table(df$ccode))
df_comp <- merge(df,tab, by.x="ccode",by.y="Var1")
df_comp <- df_comp[df_comp$Freq==13,]
df_comp <- df_comp[order(df_comp$year),]

pdf("../figures/wordshoal_fig5_3.pdf")
plot(df_comp$year, df_comp$position, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT Ideal Points", main = "", xlim=c(2000,2020), cex.lab=1.4)
points(df_comp$year[df_comp$nws==0], df_comp$position[df_comp$nws==0], col="darkgrey", pch=20, cex=1.6)
lines(aggregate(position ~ year, df_comp[df_comp$nws==0,], mean), col="darkgrey", lwd = 3, lty=2)
points(df_comp$year[df_comp$nws==1], df_comp$position[df_comp$nws==1], col="black", pch=18, cex=1.6)
lines(aggregate(position ~ year, df_comp[df_comp$nws==1,], mean), col="black", lwd = 3)
dev.off()

# restrict to to countries present in every  RevCon year
tmp <- df[df$year %in% c(2000,2005,2010,2015),]
tab <- data.frame(table(tmp$ccode))
df_comp <- merge(tmp,tab, by.x="ccode",by.y="Var1")
df_comp <- df_comp[df_comp$Freq==4,]

pdf("../figures/wordshoal_fig5_2.pdf")
plot(df_comp$year, df_comp$position, ylim = c(-3,3), type="n", xlab = "Year", ylab = "NPT Ideal Points", main = "", xlim=c(2000,2020), cex.lab=1.4)
points(df_comp$year[df_comp$nws==0], df_comp$position[df_comp$nws==0], col="darkgrey", pch=20, cex=1.6)
lines(aggregate(position ~ year, df_comp[df_comp$nws==0,], mean), col="darkgrey", lwd = 3, lty=2)
points(df_comp$year[df_comp$nws==1], df_comp$position[df_comp$nws==1], col="black", pch=1, cex=1.6)
lines(aggregate(position ~ year, df_comp[df_comp$nws==1,], mean), col="black", lwd = 3)
dev.off()

#############
## Wordshoals Version of Figure 3
#############

cor(df$position,df$Idealpoint, use = "complete.obs")

pdf("../npt paper/pdf/wordshoals_convergent.pdf")
plot(df$position, df$Idealpoint, main="",
     xlim=c(-2.5,3), ylim=c(-2,3),
     cex.lab=1.4,
     type="n",
     xlab="NPT Ideal Points",
     ylab="UNGA Ideal Points")
points(df$position[df$nws==0], df$Idealpoint[df$nws==0], col="lightgrey", pch=20, cex=1.6)
points(df$position[df$nws==1], df$Idealpoint[df$nws==1], col="black", pch=18, cex=1.9)
text(1.5, 2.5, "r = 0.50", cex=1.6)
dev.off()

##############
#wordfish vs wordshoals

cor(df$position, df$theta, use = "complete.obs")

plot(df$theta, df$position)

plot(df$position, df$theta, main="",
     xlim=c(-2.5,2.5), ylim=c(-2.5,2.5),
     cex.lab=1.4,
     type="n",
     xlab="Wordshoals Ideal Points",
     ylab="Wordfish Ideal Points")
points(df$position[df$nws==0], df$theta[df$nws==0], col="lightgrey", pch=20, cex=1.6)
points(df$position[df$nws==1], df$theta[df$nws==1], col="black", pch=18, cex=1.9)

plot(df$position[df$nws==1], df$theta[df$nws==1], col=df$ccode[df$nws==1], pch=20, cex=1.6)
text(df$position[df$nws==1], df$theta[df$nws==1], labels=df$year[df$nws==1], cex=0.9, font=2)
