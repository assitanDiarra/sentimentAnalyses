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
from django.db.models.functions import Extract
from django.views.decorators.csrf import csrf_exempt
import smtplib
        
def accueil(request):
    
    tweets= Tweets.objects.all()
    
    return render(request, 'sentiments_analysis/accueil.html',{'table': tweets})
	

@csrf_exempt
def sendMail(request):
    name = request.POST.get("name",0)
    email = request.POST.get("email",0)
    message = request.POST.get("message",0)
    
    try:

        gmail_user = 'sentiment.analysis.ensae'  
        gmail_password = '49f8wu5z-$e'
        
        sent_from = gmail_user  
        to = ['simon.aubeneau@gmail.com']  
        subject = 'mail from SentimentAnalyses'  
        body = \
"""Name: %s
Email: %s
Message:
  
%s

""" % (name, email, message)
        
        email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except Exception: 
        print("exception lors de l'envoi de mail : ", name,", ", email)
        return 0
    
    print("mail envoye : ", name,", ", email)
    return HttpResponse(request,'sentiments_analysis/index.html')
	
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
                data.append({'date': jour.strftime("%d-%m"), 'value':str(dico[jour])})
            else:
                data.append({'date': jour.strftime("%d-%m"), 'value':'0'})
            
        return data
    
    elif( type_graphique=='1' and chrono=='3'):
        listTweets = list(tf.qs.values(time=Extract('dateTime', 'hour')).annotate(value=Count('time')))
        
        data = []
        for d in listTweets:
                hour = str(d['time'])
                data.append({'date':hour, 'value':d['value']})
                
        return data
    
        data = []
        print( tf.qs.values(hour=Extract('dateTime', 'hour')).annotate(value=Count('hour')))
        for h in range(24):
            
                sql = tf.qs.filter(dateTime__hour = h)
                cpt = sql.count()
                
                heureTexte = ""+str(h)
                data.append({'date':heureTexte, 'value':cpt})
                
        return data
    
    elif( type_graphique=='1' and chrono=='2'):
        
        listTweets = list(tf.qs.values(time=Extract('dateTime', 'week_day')).annotate(value=Count('time')))
        jours = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        
        data = []
        for d in listTweets:
                jour = d['time']-1
                jourTexte = jours[jour]
                data.append({'date':jourTexte, 'value':d['value']})
                
        return data
    
    else:
        if( chrono=='3'):
            time = 'hour'
        if( chrono=='2'):
            time = 'week_day'
        if( chrono=='1'):
            time = 'date'
        if( sentiment=='1'):
            colonne = 'sentiment_type'
            valeurs_colonne = ('Positive','Neutral','Negative' )
            labels = ('positive','neutral','negative' )
        if( sentiment=='2'):
            colonne = 'gender_predicted'
            valeurs_colonne = ('Male','Unknown','Female' )
            labels = ('men','unknown','women' )
            
        if( chrono=='2' or chrono=='3'):
            listTweets= list( tf.qs.values(colonne,time=Extract('dateTime', time)).annotate(value=Count(colonne)))
        if( chrono=='1'):
            listTweets = list(tf.qs.extra(select={'time': 'date( dateTime )'}).values('time',colonne).annotate(value=Count('dateTime',colonne)))
        
        dico = {}
        for d in listTweets:
            time = d['time']
            cle = time
            if( chrono=='1'):
                cle = datetime.datetime.strptime(d['time'], "%Y-%m-%d")
            if( not cle in dico):
                dico[cle]=[0,0,0]
            triplet = dico[cle]
            if( d[colonne]==valeurs_colonne[0]):
                triplet[0]=d['value']
            if( d[colonne]==valeurs_colonne[1]):
                triplet[1]=d['value']
            if( d[colonne]==valeurs_colonne[2]):
                triplet[2]=d['value']
            dico[cle]=triplet
        
        if( chrono=='1'):
            newdico = {}
            debut = min(dico.keys())
            fin = max(dico.keys())
            intervalle = fin - debut
            for i in range(intervalle.days+1):
                jour = debut + timedelta(days=i)
                if( not jour in dico ):
                    newdico[jour]=(0,0,0)
                else:
                    newdico[jour]=dico[jour]
            dico = newdico
            
        liste=[]
        for k, t in dico.items():
            jours = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            if( chrono=='2'):
                time = jours[k-1]
            if( chrono=='3'):
                time = str(k)
            if( chrono=='1'):
                time = k.strftime("%d-%m")
            liste.append({'date':time, labels[0]:t[0], labels[1]:t[1], labels[2]:t[2]  })
                
        return liste

	
	

