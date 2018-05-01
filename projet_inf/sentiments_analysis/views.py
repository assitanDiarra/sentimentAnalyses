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

def accueil(request):

	tweets= Tweets.objects.all()
	
	return render(request, 'sentiments_analysis/accueil.html',{'table': tweets})
	
	
def home(request):

    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """

    return HttpResponse(request,'sentiments_analysis/index.html')
	
	
def carte(request):
	
	tweets_filter = filters.CarteFilter(request.GET, queryset=Tweets.objects.all())
	#tweets_list= list(Tweets.objects.values('country_code').annotate(Sum('sentiment_compound_polarity')))
	tweets_list= list(tweets_filter.qs.values('country_code').annotate(Sum('sentiment_compound_polarity')))
	tweets_list= json.dumps({"data": tweets_list})
	print("blabla")
	#return HttpResponse(tweets_list)
	return render(request, 'sentiments_analysis/carte.html',{'liste':tweets_list})
	
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
	
	return render(request, 'sentiments_analysis/liste_tweet.html',{'response': response,'tweets_filter': tweets_filter })


def getData(request, type_graphique, chrono, sentiment):
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
    print("blabla")
    if( type_graphique=='1' and chrono=='1'):        
        listTweets = list(Tweets.objects.extra(select={'date': 'date( dateTime )'}).values('date').annotate(value=Count('dateTime')))
        print( listTweets )
        
        return JsonResponse({'data': listTweets}, safe=False)
            
        
        data = []
        for m in range(3,5):
            for d in range(1,31):
                if( d<=12 and m==3):
                    continue
                if( d>=10 and m==4):
                    continue
                jour = date(2018, m, d)
                cpt = Tweets.objects.filter(dateTime__date=jour).count()
                jourTexte = ""+str(m)+"-"+str(d)
                data.append({'date':jourTexte, 'value':cpt})
        return JsonResponse({'data': data}, safe=False)
    
    elif( type_graphique=='1' and chrono=='3'):
        data = []
        for h in range(24):
            
                sql = Tweets.objects.filter(dateTime__hour = h)
                cpt = sql.count()
                
                heureTexte = ""+str(h)
                data.append({'date':heureTexte, 'value':cpt})
                
        return JsonResponse({'data': data}, safe=False)
    
    elif(  type_graphique=='1' and chrono=='2'):
        data = []
        for d in range(1,8):
            
                sql = Tweets.objects.filter(dateTime__week_day = d)
                cpt = sql.count()
                
                dico = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                jourTexte = dico[d-1]
                data.append({'date':jourTexte, 'value':cpt})
                
        return JsonResponse({'data': data}, safe=False)
    
    elif( type_graphique=='2' and chrono=='1' and sentiment=='1'):
        liste = []
        for m in range(3,5):
            for d in range(1,31):
                if( d<=12 and m==3):
                    continue
                if( d>=10 and m==4):
                    continue
                
                jour = date(2018, m, d)
            
                sql_pos = Tweets.objects.filter(dateTime__date = jour,
                                       sentiment_type__startswith='P')
                cpt_pos = sql_pos.count()
                
                sql_neg = Tweets.objects.filter(dateTime__date = jour,
                                       sentiment_type__startswith='NEG')
                cpt_neg = sql_neg.count()
                
                sql_neutral = Tweets.objects.filter(dateTime__date = jour,
                                       sentiment_type__startswith='NEU')
                cpt_neutral = sql_neutral.count()
                
                jourTexte = ""+str(m)+"-"+str(d)
                liste.append({'date':jourTexte, 'positive':cpt_pos, 'neutral':cpt_neutral, 'negative':cpt_neg })
                
        columns=['date','positive','neutral','negative']
        return JsonResponse({'liste': liste, 'columns': columns}, safe=False)
    
    elif( type_graphique=='2' and chrono=='2' and sentiment=='1'):
        liste = []
        for d in range(1,8):
            
                sql_pos = Tweets.objects.filter(dateTime__week_day = d,
                                       sentiment_type__startswith='P')
                cpt_pos = sql_pos.count()
                
                sql_neg = Tweets.objects.filter(dateTime__week_day = d,
                                       sentiment_type__startswith='NEG')
                cpt_neg = sql_neg.count()
                
                sql_neutral = Tweets.objects.filter(dateTime__week_day = d,
                                       sentiment_type__startswith='NEU')
                cpt_neutral = sql_neutral.count()
                
                dico = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                jourTexte = dico[d-1]
                liste.append({'date':jourTexte, 'positive':cpt_pos, 'neutral':cpt_neutral, 'negative':cpt_neg })
                
        columns=['date','positive','neutral','negative']
        
        return JsonResponse({'liste': liste, 'columns': columns}, safe=False)
        
    elif( type_graphique=='2' and chrono=='3' and sentiment=='1'):
        liste = []
        for h in range(24):
            
                sql_pos = Tweets.objects.filter(dateTime__hour = h,
                                       sentiment_type__startswith='P')
                cpt_pos = sql_pos.count()
                
                sql_neg = Tweets.objects.filter(dateTime__hour = h,
                                       sentiment_type__startswith='NEG')
                cpt_neg = sql_neg.count()
                
                sql_neutral = Tweets.objects.filter(dateTime__hour = h,
                                       sentiment_type__startswith='NEU')
                cpt_neutral = sql_neutral.count()
                
                heureTexte = ""+str(h)
                
                liste.append({'date':heureTexte, 'positive':cpt_pos, 'neutral':cpt_neutral, 'negative':cpt_neg })
                
        columns=['date','positive','neutral','negative']
                
        return JsonResponse({'liste': liste, 'columns': columns}, safe=False)
        
    elif( type_graphique=='2' and chrono=='1' and sentiment=='2'):
        liste = []
        for m in range(3,5):
            for d in range(1,31):
                if( d<=12 and m==3):
                    continue
                if( d>=10 and m==4):
                    continue
                
                jour = date(2018, m, d)
            
                sql_m = Tweets.objects.filter(dateTime__date = jour,
                                       gender_predicted__startswith='M')
                cpt_m = sql_m.count()
                
                sql_f = Tweets.objects.filter(dateTime__date = jour,
                                       gender_predicted__startswith='F')
                cpt_f = sql_f.count()
                
                sql_u = Tweets.objects.filter(dateTime__date = jour,
                                       gender_predicted__startswith='U')
                cpt_u = sql_u.count()
                
                jourTexte = ""+str(m)+"-"+str(d)
                liste.append({'date':jourTexte, 'men':cpt_m, 'unknown':cpt_u, 'women':cpt_f })
                
        columns=['date','men','unknown','women']
        return JsonResponse({'liste': liste, 'columns': columns}, safe=False)
    
    elif( type_graphique=='2' and chrono=='2' and sentiment=='2'):
        liste = []
        for d in range(1,8):
            
                sql_m = Tweets.objects.filter(dateTime__week_day = d,
                                       gender_predicted__startswith='M')
                cpt_m = sql_m.count()
                
                sql_f = Tweets.objects.filter(dateTime__week_day = d,
                                       gender_predicted__startswith='F')
                cpt_f = sql_f.count()
                
                sql_u = Tweets.objects.filter(dateTime__week_day = d,
                                       gender_predicted__startswith='U')
                cpt_u = sql_u.count()
                
                dico = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                jourTexte = dico[d-1]
                liste.append({'date':jourTexte, 'men':cpt_m, 'unknown':cpt_u, 'women':cpt_f })
                
        columns=['date','men','unknown','women']
        return JsonResponse({'liste': liste, 'columns': columns}, safe=False)
    
    elif( type_graphique=='2' and chrono=='3' and sentiment=='2'):
        liste = []
        for h in range(24):
            
                sql_m = Tweets.objects.filter(dateTime__hour = h,
                                       gender_predicted__startswith='M')
                cpt_m = sql_m.count()
                
                sql_f = Tweets.objects.filter(dateTime__hour = h,
                                       gender_predicted__startswith='F')
                cpt_f = sql_f.count()
                
                sql_u = Tweets.objects.filter(dateTime__hour = h,
                                       gender_predicted__startswith='U')
                cpt_u = sql_u.count()
                
                heureTexte = ""+str(h)
                
                liste.append({'date':heureTexte, 'men':cpt_m, 'unknown':cpt_u, 'women':cpt_f })
                
        columns=['date','men','unknown','women']
                
        return JsonResponse({'liste': liste, 'columns': columns}, safe=False)
    
    return JsonResponse({}, safe=False)

	
	

