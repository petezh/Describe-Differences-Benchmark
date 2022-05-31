######################################################################
## Main Committee Wordfish Estimates
######################################################################

# get  docs, create corpus
c1corpus <- corp("../data/docs_by_committee/C1 all years")
c2corpus <- corp("../data/docs_by_committee/C2 all years")
c3corpus <- corp("../data/docs_by_committee/C3 all years")

set.seed(123)

c1 <- fish(c1corpus)
c2 <- fish(c2corpus)
c3 <- fish(c3corpus)

library(countrycode)

df1 <- data.frame(country = c1@x@docvars$country, year = c1@x@docvars$year,
                  c1theta = c1@theta, c1se.theta = c1@se.theta)
df1$year <- as.numeric(as.character(df1$year))
df1$ccode <- countrycode(df1$country, 'country.name', 'cown')
df1$ccode[df1$name == 'malysia'] <- 820
df1$ccode[df1$name == 'nz'] <- 920
df1$ccode[df1$name == 'republicofkorea'] <- 732
df1$ccode[df1$name == 'rok'] <- 732
df1$ccode[df1$name == 'southafrica'] <- 560


df2 <- data.frame(country = c2@x@docvars$country, year = c2@x@docvars$year, 
                  c2theta = c2@theta, c2se.theta = c2@se.theta)
df2$year <- as.numeric(as.character(df2$year))
df2$ccode <- countrycode(df2$country, 'country.name', 'cown')
df2$ccode[df2$name == 'philippine'] <- 840
df2$ccode[df2$name == 'nz'] <- 920
df2$ccode[df2$name == 'republicofkorea'] <- 732
df2$ccode[df2$name == 'rok'] <- 732
df2$ccode[df2$name == 'southafrica'] <- 560

df3 <- data.frame(country = c3@x@docvars$country, year = c3@x@docvars$year, 
                  c3theta = c3@theta, c3se.theta = c3@se.theta)
df3$year <- as.numeric(as.character(df3$year))
df3$ccode <- countrycode(df3$country, 'country.name', 'cown')
df3$ccode[df3$name == 'nz'] <- 920
df3$ccode[df3$name == 'republicofkorea'] <- 732
df3$ccode[df3$name == 'rok'] <- 732
df3$ccode[df3$name == 'southafrica'] <- 560

mc <- merge(df1,df2, by=c('ccode','year'), all = T)
mc <- merge(mc,df3, by=c('ccode','year'), all = T)

load("~/Dropbox/npt/data/merged.Rdata")

df <- merge(mc, ts, by=c('ccode','year'))
df$c1se.theta <- -1 * df$c1se.theta
df$c1theta <- -1 * df$c1theta
df$c3se.theta <- -1 * df$c3se.theta
df$c3theta <- -1 * df$c3theta

cor(df$theta, df$c1theta, use="pairwise") # 0.2153139
cor(df$theta, df$c2theta, use="pairwise") # 0.6120301
cor(df$theta, df$c3theta, use="pairwise") # 0.5557533

save(df, file = "../data/merged_with_committee.Rdata")

# discriminant words
sw <- data.frame(beta=c2@beta, word=c2@features)
sw <- sw[order(sw$beta),]
print(head(sw$word, n=20))
print(tail(sw$word, n=40))
