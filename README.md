# sentimentAnalyses

## Twitter Sentiment Analyses in python



As part of a python project, we decided to create a web application about people feelings (english only) on Twitter. So this project is divided in tree parts: Twitter scraping, machine learning and web application. Indeed, we first scrapped english tweets using Twitter API around the world. Then after cleaned it, we predicted the sentiments using from package named nltk. It uses VADER, a parsimonious rule-based model for Sentiment Analysis of Social Media text written by Hutto, C.J. & Gilbert, E.E. (2014).

We used more precisely *SentimentIntensityAnalyzer* class which gives a sentiment intensity score to sentences. Indeed, positive values are positive valence, negative value are negative valence and null value are neutral. Finaly, we decided to present our analysis in an web application. So We chose a well known Python Web framework: Django.

