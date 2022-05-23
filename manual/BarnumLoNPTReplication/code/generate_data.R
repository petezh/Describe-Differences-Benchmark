######################################################################
## Generate Wordfish Estimates, Bootstrap CIs, Merge With Variables for Validation, Generate and Merge LDA estimates
## Miriam Barnum and James Lo
## September 16, 2019
######################################################################

#setwd("~/Dropbox/npt/code")

library(quanteda)

# geographic words to drop
countries <- read.csv("~/Dropbox/npt/data/to_merge/country-capitals.csv", stringsAsFactors = F)
dumpWords <- c("Nigeria", countries$CountryName, countries$CapitalName, 'UAE','Holy See','Republic of Korea', "Democratic People's Republic of Korea")
regions <- c("europe","european","asia","asian",'africa','african','eu','nam','non-aligned', 'arab', "uk", 'uae', 'holy','ipndv','npdi','islamic','french')
swords <- c("ladies","gentlemen","chairman", 'chairperson', 'january','february','march','april','may','june','july','august',
            'september','october','november','december', "medvedev","obama", 'side-event', 'summer','th', 'o','t')

# process docs, create corpus
corp <- function(dir){
  wd <- getwd()
  setwd(dir)
  # Read all documents
  fnames <- list.files()
  alldocs <- rep(NA, length(fnames))
  for(i in 1:length(fnames)){
    doc <- readLines(fnames[i])
    alldocs[i] <- paste(doc, collapse=" ")
  }
  
  # extract country names and dates from file names
  tmp <- gsub(".txt", "", fnames)
  docstate <- tolower(unlist(strsplit(tmp, "_"))[seq(1, 3*length(tmp), by=3)])
  docdate <- unlist(strsplit(tmp, "_"))[seq(2, 3*length(tmp), by=3)]
  docnames <- paste(docstate, docdate, sep = "_")
  
  # prepare corpus
  corpus <- corpus(alldocs)
  docnames(corpus) <- docnames
  docvars(corpus, "year") <- docdate
  docvars(corpus, "country") <- docstate
  
  #remove geo words
  for(n in dumpWords){ 
    corpus$documents$texts <- gsub(n, "", corpus$documents$texts)
  }
  
  setwd(wd)
  
  return(corpus)
}

# function to preprocess and run wordfish
fish <- function(corpus){
  # create dfm, preprocess
  dfm <- dfm(corpus, remove_punct=T, remove_numbers = T, stem = T, remove=c(stopwords("english"), regions, swords))
  dfm <- dfm_trim(dfm, min_docfreq = 10)
  
  # running wordfish
  wf <- textmodel(dfm, model="wordfish") # original code, old version of quanteda
  #wf <- textmodel_wordfish(dfm) # new version of quanteda. need to change @ to $ below if using this
  return(wf)
}

# get general debate docs, create corpus
path <- "../data/docs_by_committee/GD all years"
gdcorpus <- corp(path)

# save
#save(gdcorpus, file="../data/gd_corpus.RDATA")

set.seed(123)

# create dfm, run wf
wfpool <- fish(gdcorpus)


save(wfpool, file="../data/wfpool.RDATA")

# extract estimates
ts <- data.frame(doc = wfpool@docs, country = wfpool@x@docvars$country, year = wfpool@x@docvars$year, 
                 theta = wfpool@theta, se.theta = wfpool@se.theta)
ts$year <- as.numeric(as.character(ts$year))

#flip so NWS have positive ideal points
ts$theta <- -1*ts$theta

###########################
# Parametric Bootstrap 
###########################

sigma <- 3
dir <- wfpool@dir
tol <- c(1e-06, 1e-08)

nsim <- 100

source("bootstrap.R")

bootresult<-bootstrap(nsim, wfpool) 
ci.documents<-bootresult$conf.documents
ci.words<-bootresult$conf.words
boot.omega <- bootresult$output.se.omega
boot.beta <- bootresult$output.se.b
save(ci.documents,ci.words, boot.omega, boot.beta, file = "bootstrap.Rdata")

ci.documents <- ci.documents *(-1)
ci.documents <- as.data.frame(ci.documents)
ci.documents$doc <- rownames(ci.documents)
ts <- merge(ci.documents,ts, by = "doc", all = T)
save(ts, file = "merged_bootstrap.Rdata")

##################################
## ADDING DATA FROM OTHER SOURCES
## skip this and use the final
## merged data file provided
#################################

# add cowcodes
library(countrycode)
ts$ccode <- countrycode(as.character(ts$country), 'country.name','cown')
ts$ccode[ts$country=="serbia montenegro"] <- 345
ts$ccode[ts$country=="serbia"] <- 345
ts$ccode[ts$country=="lithuanina"] <- 368
ts$ccode[ts$country=="portugual"] <- 235

# nws
ts$nws <- ifelse(ts$ccode %in% c(2, 200,220,365,710), 1, 0)

# past violators
ts$prev_vi <- 0
ts$prev_vi[ts$country %in% c("syria", 'iran','iraq','libya','romania','yugoslavia','north korea')] <- 1

# nws allies
ally <- read.csv("../data/to_merge/alliances.csv")
ally <- ally[ally$ccode1 %in% c(2,365,710,200,220),]
ally <- ally[,c("ccode2","year","defense")]
ally <- aggregate(defense ~ ., data=ally, sum)

# impute for years w/out alliance data
a <- b <- c <- d <- e <- ally[ally$year == max(ally$year),]
a$year <- 2013
b$year <- 2014
c$year <- 2015
d$year <- 2017
e$year <- 2018
ally <- rbind(ally,a,b,c,d,e)

ts <- merge(ts, ally, by.x = c("ccode", "year"),by.y = c("ccode2", "year"), all.x = T)
ts$defense <- ifelse(is.na(ts$defense), 0, ifelse(ts$defense > 0, 1, 0))
ts$defense[ts$ccode == 365 | ts$ccode == 710] <- 1

# polity
library(readxl)
polity <- read_excel("../data/to_merge/p4v2017.xls")
polity <- polity[,c("ccode","year","polity2")]
ts <- merge(ts, polity, all.x = T)

# gdp/capita
load("../data/to_merge/PREPPED_WDI_PW.RDATA")
wdi_pwt <- wdi_pwt[,c("ccode","year","gdppc_WDI_PW")]
ts <- merge(ts, wdi_pwt, all.x = T)

# UN idealpoints
library(readstata13)
un <- read.dta13("../data/to_merge/IdealpointsPublished.dta", nonint.factors = TRUE)
un <- un[,c("year","ccode","Idealpoint","unsc_region")]
ts <- merge(ts, un, all.x = T)

## Jo and Gartzke latent
library(foreign)
jo <- read.dta("../data/to_merge/jo_gartzke_0207_nuccap_0906.dta")
jo <- jo[jo$year==2001,]
jo <- jo[, -2]
ts <- merge(ts, jo, by="ccode", all.x=TRUE)

### Stoll data
## http://es.rice.edu/projects/Poli378/Nuclear/Proliferation/Countries/Algeria.html

stoll <- read.csv("../data/to_merge/stoll_capacity.csv")
ts$stoll <- stoll$latent_cap[match(ts$ccode, stoll$CCode)]

## Simple imputation (if desired)
## Only Belgium, Czech Republic, Singapore, Iceland, Kuwait, UAE are highly developed
unique(ts$country[which(is.na(ts$stoll))])
ts$stoll.imputed <- ts$stoll
table(ts$stoll)	# 6 is lowest value
ts$stoll.imputed[is.na(ts$stoll.imputed)]  <- 6


## Fuhrmann data. Coded as 1 once they have ever gotten it and 0 otherwise
fmann <- read.csv("../data/to_merge/Fuhrmann_country-year_dataset.csv", as.is=TRUE)

## Did the state *ever* have latent capability?
fstuff.lab <- by(fmann$latency_lab, fmann$ccode, max) 
ts$fuhrmann.lab <- fstuff.lab[match(ts$ccode, as.numeric(names(fstuff.lab)) )]

## Did the state *ever* have latent capability?
fstuff.pilot <- by(fmann$latency_pilot, fmann$ccode, max) 
ts$fuhrmann.pilot <- fstuff.lab[match(ts$ccode, as.numeric(names(fstuff.pilot)) )]

save(ts, file = "../data/merged_backup.RDATA")

#######################
## ADDING TOPIC MODELS
#######################
 
library(tidyr)
library(tidytext)
library(topicmodels)
library(gridExtra)

set.seed(654)
mytheme <- ttheme_default(base_size = 4)

# create dfm, preprocess
dfm <- dfm(gdcorpus, remove_punct=T, remove_numbers = T, stem = T, 
           remove=c(stopwords("english"), regions, swords, 
                    "nuclear","weapon","weapons","mr","president","treaty","npt","conference","conferences"))
dfm <- dfm_trim(dfm, min_docfreq = 10)

# run LDA for 7 and 11 topics
lda7 <- LDA(dfm, k = 7, method = "Gibbs", 
             control = list(verbose=25L, seed = 1234, burnin = 500, iter = 4000))
#save(lda7, file = '../data/lda7.Rdata')
lda11 <- LDA(dfm, k = 11, method = "Gibbs", 
            control = list(verbose=25L, seed = 1234, burnin = 500, iter = 4000))
#save(lda11, file = '../data/lda11.Rdata', sep =)

# merge in data for 7 topics
gamma <- tidy(lda7, matrix = "gamma")
gamma <- gamma %>% separate(document, c("country", "year"), sep = "_", convert = TRUE)
gamma$topic <- paste("topic", gamma$topic, sep = '')
gamma <- spread(gamma, topic, gamma)
ts <- merge(ts, gamma, all.x = T)

# merge in data for 11 topics
gamma <- tidy(lda11, matrix = "gamma")
gamma <- gamma %>% separate(document, c("country", "year"), sep = "_", convert = TRUE)
gamma$topic <- paste("XItopic", gamma$topic, sep = '')
gamma <- spread(gamma, topic, gamma)
ts <- merge(ts, gamma, all.x = T)

save(ts, file = "../data/merged_final.Rdata")

####################################
## Run wordfish for each of the three main committees
####################################

# get  docs, create corpus
c1corpus <- corp("../data/docs_by_committee/C1 all years")
c2corpus <- corp("../data/docs_by_committee/C2 all years")
c3corpus <- corp("../data/docs_by_committee/C3 all years")

set.seed(123)

c1 <- fish(c1corpus)
c2 <- fish(c2corpus)
c3 <- fish(c3corpus)

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

df <- merge(mc, ts, by=c('ccode','year'))
df$c1se.theta <- -1 * df$c1se.theta
df$c1theta <- -1 * df$c1theta
df$c3se.theta <- -1 * df$c3se.theta
df$c3theta <- -1 * df$c3theta

cor(df$theta, df$c1theta, use="pairwise") # 0.2153139
cor(df$theta, df$c2theta, use="pairwise") # 0.6120301
cor(df$theta, df$c3theta, use="pairwise") # 0.5557533

save(df, file = "../data/merged_with_committee.Rdata")
