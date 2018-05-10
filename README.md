# Twitter Sentiments Analyses Web Application



As part of a python project, we decided to create a web application about people feelings (english only) on Twitter. So this project is divided in tree parts: Twitter scraping, machine learning and web application. Indeed, we first scrapped english tweets using Twitter API around the world. Then after cleaned it, we predicted the sentiments using from package named __nltk__. It uses __VADER__, a parsimonious rule-based model for Sentiment Analysis of Social Media text written by Hutto, C.J. & Gilbert, E.E. (2014).

We used more precisely __SentimentIntensityAnalyzer__ class which gives a sentiment intensity score to sentences. Indeed, positive values are positive valence, negative value are negative valence and null value are neutral. Finaly, we decided to present our analysis in an web application. So We chose a well known Python Web framework: __Django__.

## How to install it ?

-	Install the requirements

yourpath\projet_inf pip install -r /path/to/requirements.txt

-	Launch the server

yourpath\projet_inf python manage.py runserver



