library(ggplot2)
library(tidyr)
library(dplyr)
library(gridExtra)

kbo <- read.csv('/home/shlee/Desktop/Programming/scrapping/kbotown_5_6-12.csv')

kbo$reply <- as.numeric (as.character(kbo$reply))

kbo_team_and_subject <- filter(kbo, word != 'NULL') %>%
                        group_by(word) %>%
                        summarise(n = n(),
                                  viewcount = sum(viewV),
                                  replycount = sum(reply)) %>%
                        mutate(view_by_n = viewcount/n, reply_by_n = replycount/n) %>%
                        arrange(desc(n)) %>%
                        filter(n > 1000) %>%
                        ungroup()

kbo_team_and_subject

head(kbo_team_and_subject)

viewdata <- ggplot(data = kbo_team_and_subject,
                  mapping = aes(x = word, y = viewcount)) +
             geom_bar(stat = 'identity')

ndata <-ggplot(data = kbo_team_and_subject,
               mapping = aes(x = word, y = n)) +
          geom_bar(stat = 'identity')

replydata <- ggplot(data = kbo_team_and_subject,
                    mapping = aes(x = word, y = replycount)) +
              geom_bar(stat = 'identity')

grid.arrange(viewdata, ndata, replydata)

vbn <- ggplot(data = kbo_team_and_subject,
             mapping = aes(x = word, y = view_by_n)) +
        geom_bar(stat = 'identity') + 
        coord_cartesian(ylim = c(300,600))
        
rbn <- ggplot(data = kbo_team_and_subject,
             mapping = aes(x = word, y = reply_by_n)) +
               geom_bar(stat = 'identity')   


