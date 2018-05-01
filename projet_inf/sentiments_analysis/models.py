#from django.db import models

# Create your models here.
from django.db import models
from django_tables2 import SingleTableView, tables
#from django_filters.views import FilterView
from django.utils import timezone


class Tweets(models.Model):
	
	
	#id_tweets = models.BigIntegerField(null = True) 
	
	name = models.CharField(max_length=45)
	
	place = models.TextField(null = True)
	
	tweet = models.TextField(null = True)
	
	dateTime = models.DateTimeField(db_index=True)
	
	country = models.CharField(max_length=45,db_index=True)
	
	country_code = models.CharField(max_length=4,null = True)
	
	text_lem = models.TextField(null = True)
	
	sentiment_compound_polarity = models.FloatField(null = True)
	
	sentiment_type = models.CharField(max_length=45,null = True, db_index=True) 
	
	gender_predicted = models.CharField(max_length=45,null = True, db_index=True)
	
	

class TweetTable(tables.Table):
    class Meta:
        model = Tweets


class TweetList(SingleTableView):
    model = Tweets
    table_class = TweetTable 
	
#class FilteredTweetListView(SingleTableMixin, FilterView):
#    table_class = TweetTable
#    model = Tweets
#    template_name = 'accueil.html'
#
 #   filterset_class = TweetFilter

	

#	class Meta:
#	
#		verbose_name = "Tweets" 
#		ordering = ['dateTime']

#    class Meta:
#		verbose_name = "article"
#    	ordering = ['dateTime'] 

#    def __str__(self):
#
#        """ 
#
#        Cette méthode que nous définirons dans tous les modèles
#
#        nous permettra de reconnaître facilement les différents objets que 
#
#        nous traiterons plus tard dans l'administration
#
#        """

#        return self.titre