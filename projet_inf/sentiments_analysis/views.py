from django.shortcuts import render
from datetime import datetime, date
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from sentiments_analysis.models import  Tweets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import TweetFilter, CarteFilter
from . import filters
from django.db.models import Count
import datetime
from datetime import timedelta

def accueil(request):

	tweets= Tweets.objects.all()
	
	return render(request, 'sentiments_analysis/accueil.html',{'table': tweets})
	
	
def home(request):

    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """

    return HttpResponse(request,'sentiments_analysis/index.html')
	
	
def carte(request):
	
	tweets_filter = filters.CarteFilter(request.GET, queryset=Tweets.objects.order_by('-dateTime'))
	#tweets_list= list(Tweets.objects.values('country_code').annotate(Sum('sentiment_compound_polarity')))
	tweets_list= list(tweets_filter.qs.values('country_code').annotate(Sum('sentiment_compound_polarity')))
	tweets_list= json.dumps({"data": tweets_list})
	print('date',datetime.date.today())
	return render(request, 'sentiments_analysis/carte.html',{'liste':tweets_list,'tweets_filter': tweets_filter })
	
def graphique(request):
    tweets_filter = filters.GraphiqueFilter(request.GET, queryset=Tweets.objects.all())
    attributs = {'tweets_filter': tweets_filter }
    
    tf = filters.GraphiqueFilter(request.GET, queryset=Tweets.objects.all())
    
    chrono = request.GET.get('chrono','1')
    sentiment = request.GET.get('type_valeur','0')
    if( sentiment=="0"):
        type_graphique = "1"
    else:
        type_graphique = "2"
    data = getData(type_graphique, chrono, sentiment, tf)
    
    #tweets_list= [{"date":"05-25", "value":35},{"date":"05-26", "value":43}]
    data = json.dumps({"data": data})
    attributs["data"]=data
    
    if( type_graphique=='2' and sentiment=='1'):
        attributs["columns"]=['date','positive','neutral','negative']
    elif( type_graphique=='2' and sentiment=='2'):
        attributs["columns"]=['date','men','unknown','women']
    else:
        attributs["columns"]=0
        
    attributs["chrono"]=chrono
    attributs["type_value"]=sentiment
    return render(request, 'sentiments_analysis/graphique.html',attributs)
	
def liste_tweet(request):
	
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
	print(response.next_page_number())
	
	return render(request, 'sentiments_analysis/liste_tweet.html',{'response': response,'tweets_filter': tweets_filter })



def getData(type_graphique, chrono, sentiment, tf):
    """
    type_graphique =
        1 -> histogram vanilla
        2 -> histogram stacked 100%
        3 -> heatmap
    
    chrono =
        1 -> per day in the month
        2 -> per day of the week
        3 -> per hour
    
    ( sentiment is used only for heatmap and histogram-stacked-100%)
    sentiment =
        0 -> show the totalnumber  ( only for heatmap )
        1 -> show by sentiment_type
        2 -> show by gender
    """
    if( type_graphique=='1' and chrono=='1'):        
        listTweets = list(tf.qs.extra(select={'date': 'date( dateTime )'}).values('date').annotate(value=Count('dateTime')))
        
        dico = {}
        for d in listTweets:
            jour = datetime.datetime.strptime(d['date'], "%Y-%m-%d")
            dico[jour]=d['value']
        
        debut = min(dico.keys())
        fin = max(dico.keys())
        intervalle = fin - debut
        
        data = []
        for i in range(intervalle.days+1):
            jour = debut + timedelta(days=i)
            if jour in dico:
                data.append({'date': jour.strftime("%m-%d"), 'value':str(dico[jour])})
            else:
                data.append({'date': jour.strftime("%m-%d"), 'value':'0'})
            
        return data
    
    elif( type_graphique=='1' and chrono=='3'):
        data = []
        for h in range(24):
            
                sql = tf.qs.filter(dateTime__hour = h)
                cpt = sql.count()
                
                heureTexte = ""+str(h)
                data.append({'date':heureTexte, 'value':cpt})
                
        return data
    
    elif(  type_graphique=='1' and chrono=='2'):
        data = []
        for d in range(1,8):
            
                sql = tf.qs.filter(dateTime__week_day = d)
                cpt = sql.count()
                
                dico = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                jourTexte = dico[d-1]
                data.append({'date':jourTexte, 'value':cpt})
                
        return data
    
    elif( type_graphique=='2' and chrono=='1' and sentiment=='1'):
        listTweets = list(tf.qs.extra(select={'date': 'date( dateTime )'}).values('date','sentiment_type').annotate(value=Count('dateTime','sentiment_type')))
        
        dico = {}
        for d in listTweets:
            jour = datetime.datetime.strptime(d['date'], "%Y-%m-%d")
            if( not jour in dico):
                dico[jour]=[0,0,0]
            triplet = dico[jour]
            if( d["sentiment_type"]=='Positive'):
                triplet[0]=d['value']
            if( d["sentiment_type"]=='Neutral'):
                triplet[1]=d['value']
            if( d["sentiment_type"]=='Negative'):
                triplet[2]=d['value']
            dico[jour]=triplet
        
        debut = min(dico.keys())
        fin = max(dico.keys())
        intervalle = fin - debut
        
        data = []
        for i in range(intervalle.days+1):
            jour = debut + timedelta(days=i)
            if( not jour in dico ):
                dico[jour]=[0,0,0]
            triplet = dico[jour]
            data.append({'date': jour.strftime("%m-%d"), 
                         'positive':triplet[0], 
                         'neutral':triplet[1], 
                         'negative':triplet[2]})
        columns=['date','positive','neutral','negative']
        return data
    
    elif( type_graphique=='2' and chrono=='2' and sentiment=='1'):
        liste = []
        for d in range(1,8):
            
                sql_pos = tf.qs.filter(dateTime__week_day = d,
                                       sentiment_type__startswith='P')
                cpt_pos = sql_pos.count()
                
                sql_neg = tf.qs.filter(dateTime__week_day = d,
                                       sentiment_type__startswith='NEG')
                cpt_neg = sql_neg.count()
                
                sql_neutral = tf.qs.filter(dateTime__week_day = d,
                                       sentiment_type__startswith='NEU')
                cpt_neutral = sql_neutral.count()
                
                dico = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                jourTexte = dico[d-1]
                liste.append({'date':jourTexte, 'positive':cpt_pos, 'neutral':cpt_neutral, 'negative':cpt_neg })
                
        columns=['date','positive','neutral','negative']
        
        return liste
        
    elif( type_graphique=='2' and chrono=='3' and sentiment=='1'):
        liste = []
        for h in range(24):
            
                sql_pos = tf.qs.filter(dateTime__hour = h,
                                       sentiment_type__startswith='P')
                cpt_pos = sql_pos.count()
                
                sql_neg = tf.qs.filter(dateTime__hour = h,
                                       sentiment_type__startswith='NEG')
                cpt_neg = sql_neg.count()
                
                sql_neutral = tf.qs.filter(dateTime__hour = h,
                                       sentiment_type__startswith='NEU')
                cpt_neutral = sql_neutral.count()
                
                heureTexte = ""+str(h)
                
                liste.append({'date':heureTexte, 'positive':cpt_pos, 'neutral':cpt_neutral, 'negative':cpt_neg })
                
        columns=['date','positive','neutral','negative']
                
        return liste
        
    elif( type_graphique=='2' and chrono=='1' and sentiment=='2'):
        listTweets = list(tf.qs.extra(select={'date': 'date( dateTime )'}).values('date','gender_predicted').annotate(value=Count('dateTime','gender_predicted')))
        
        dico = {}
        for d in listTweets:
            jour = datetime.datetime.strptime(d['date'], "%Y-%m-%d")
            if( not jour in dico):
                dico[jour]=[0,0,0]
            triplet = dico[jour]
            if( d["gender_predicted"]=='Male'):
                triplet[0]=d['value']
            if( d["gender_predicted"]=='Female'):
                triplet[1]=d['value']
            if( d["gender_predicted"]=='Unknown'):
                triplet[2]=d['value']
            dico[jour]=triplet
        
        debut = min(dico.keys())
        fin = max(dico.keys())
        intervalle = fin - debut
        
        data = []
        for i in range(intervalle.days+1):
            jour = debut + timedelta(days=i)
            if( not jour in dico ):
                dico[jour]=[0,0,0]
            triplet = dico[jour]
            data.append({'date': jour.strftime("%m-%d"), 
                         'men':triplet[0], 
                         'unknown':triplet[1], 
                         'women':triplet[2]})
        columns=['date','men','unknown','women']
        return data
    
    elif( type_graphique=='2' and chrono=='2' and sentiment=='2'):
        liste = []
        for d in range(1,8):
            
                sql_m = tf.qs.filter(dateTime__week_day = d,
                                       gender_predicted__startswith='M')
                cpt_m = sql_m.count()
                
                sql_f = tf.qs.filter(dateTime__week_day = d,
                                       gender_predicted__startswith='F')
                cpt_f = sql_f.count()
                
                sql_u = tf.qs.filter(dateTime__week_day = d,
                                       gender_predicted__startswith='U')
                cpt_u = sql_u.count()
                
                dico = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                jourTexte = dico[d-1]
                liste.append({'date':jourTexte, 'men':cpt_m, 'unknown':cpt_u, 'women':cpt_f })
                
        columns=['date','men','unknown','women']
        return liste
    
    elif( type_graphique=='2' and chrono=='3' and sentiment=='2'):
        liste = []
        for h in range(24):
            
                sql_m = tf.qs.filter(dateTime__hour = h,
                                       gender_predicted__startswith='M')
                cpt_m = sql_m.count()
                
                sql_f = tf.qs.filter(dateTime__hour = h,
                                       gender_predicted__startswith='F')
                cpt_f = sql_f.count()
                
                sql_u = tf.qs.filter(dateTime__hour = h,
                                       gender_predicted__startswith='U')
                cpt_u = sql_u.count()
                
                heureTexte = ""+str(h)
                
                liste.append({'date':heureTexte, 'men':cpt_m, 'unknown':cpt_u, 'women':cpt_f })
                
        columns=['date','men','unknown','women']
                
        return liste
    
    print( "WTF:", type_graphique, chrono, sentiment)
    return 0

	
	

