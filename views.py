from django.shortcuts import render
from datetime import datetime, date
from django.db.models import Sum
import json

# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render
from sentiments_analysis.models import  Tweets,TweetTable,TweetTable
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import TweetFilter
from . import filters



def home(request):

    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """

    return HttpResponse(request,'sentiments_analysis/index.html')
	
	
def carte(request):

	tweets_list= Tweets.objects.filter(dateTime__month='04').values('country_code').annotate(Sum('sentiment_compound_polarity'))
	print(json.dumps(tweets_list))
	
	return render(request, 'sentiments_analysis/index.html',{'liste': tweets_list})
	
def test(request):
	
	"""tweets_list= Tweets.objects.order_by('-dateTime')
	tweets_filter = TweetFilter(request.GET, queryset=tweets_list)
	return render(request, 'sentiments_analysis/test.html',{'response': tweets_filter})"""
	
	"""tweets_list= Tweets.objects.order_by('-dateTime')
	page = request.GET.get('page', 1)
	paginator = Paginator(tweets_list, 10)
	try:
		tweets = paginator.page(page)
	except PageNotAnInteger:
		tweets = paginator.page(1)
	except EmptyPage:
		tweets = paginator.page(paginator.num_pages)
	tweets_filter = TweetFilter(request.GET, queryset=tweets)"""
	
	tweets_filter = TweetFilter(request.GET, queryset=Tweets.objects.order_by('-dateTime'))
	filtered_qs = filters.TweetFilter(request.GET, queryset=Tweets.objects.order_by('-dateTime')).qs	
	paginator = Paginator(filtered_qs, 10)
	page = request.GET.get('page')
	try:
		response = paginator.page(page)
	except PageNotAnInteger:
		response = paginator.page(1)
	except EmptyPage:
		response = paginator.page(paginator.num_pages)
	
	return render(request, 'sentiments_analysis/test.html',{'response': response,'tweets_filter': tweets_filter })

def test2(request):
	
	tweets_list= Tweets.objects.order_by('-dateTime')
	page = request.GET.get('page', 1)
	paginator = Paginator(tweets_list, 10)
	try:
		tweets = paginator.page(page)
	except PageNotAnInteger:
		tweets = paginator.page(1)
	except EmptyPage:
		tweets = paginator.page(paginator.num_pages)
	
	return render(request, 'sentiments_analysis/map.html', {'tweets': tweets})
	
def accueil(request):
	
	tweets= Tweets.objects.all()
	
	return render(request, 'sentiments_analysis/accueil.html',{'table': tweets})
	
#def accueil(request):

#	tweets =  Tweets.objects.all() # Nous sélectionnons tous nos articles
	#filter = FilteredTweetListView(request.GET, queryset=Tweets.objects.all())
	#return render(request, 'sentiments_analysis/template.html', {'filter': filter})
#	return render(request,'sentiments_analysis/accueil.html', {'table': tweets})
	#return render(request, 'sentiments_analysis/accueil.html', {'derniers_tweets': tweets})


def lire(request, id):

    """ Afficher un  Tweets complet """

    pass # Le code de cette fonction est donné un peu plus loin.

def view_article(request, id_article):

    # Si l'ID est supérieur à 100, nous considérons que l' Tweets n'existe pas

    if int(id_article) > 100:

        raise Http404
	

    return HttpResponse('<h1>Mon  Tweets ici</h1>')

def date_actuelle(request):

    return render(request, 'sentiments_analysis/date.html', {'date': datetime.now()})



def addition(request, nombre1, nombre2):    

    total = nombre1 + nombre2


    # Retourne nombre1, nombre2 et la somme des deux au tpl

    return render(request, 'sentiments_analysis/addition.html', locals())