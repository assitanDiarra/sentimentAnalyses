from django import forms
from sentiments_analysis.models import  Tweets
import django_filters
from datetime import date
import datetime
from django.utils import timezone
#import timezone 
#from timezone import now

gender_choice=(
('Male','Male'),
('Female','Female'),
('Unknown','Unknown'))
sentiment_choice=(
('Positive','Positive'),
('Negative','Negative'),
('Neutral','Neutral'))
class TweetFilter(django_filters.FilterSet):
	tweet = django_filters.CharFilter(lookup_expr='icontains', label='Search terms')
	country = django_filters.CharFilter(lookup_expr='icontains', label='Country')
	gender_predicted = django_filters.MultipleChoiceFilter(choices=gender_choice,
        widget=forms.CheckboxSelectMultiple)
	#(queryset=Tweets.objects.values_list('gender_predicted',flat=True).distinct(),
     #   widget=forms.CheckboxSelectMultiple)
	sentiment_type = django_filters.MultipleChoiceFilter(choices=sentiment_choice,
        widget=forms.CheckboxSelectMultiple)

    
	class Meta:
		model = Tweets
		fields = ['tweet', 'country', 'gender_predicted', 'dateTime', 'sentiment_type']
		

		
class CarteFilter(django_filters.FilterSet):
	tweet = django_filters.CharFilter(lookup_expr='icontains',label='Search terms')
	gender_predicted = django_filters.MultipleChoiceFilter(choices=gender_choice,
        widget=forms.CheckboxSelectMultiple)
		#, widget=forms.SelectDateWidget()
	dateTime = django_filters.DateTimeFilter(widget=forms.SelectDateWidget(), lookup_expr="date", label="Date", initial=timezone.now)

    
	class Meta:
		model = Tweets
		fields = ['tweet', 'country', 'gender_predicted', 'dateTime', 'sentiment_type']

        
class GraphiqueFilter(django_filters.FilterSet):
	tweet = django_filters.CharFilter(lookup_expr='icontains', label='Search terms')
	country = django_filters.CharFilter(lookup_expr='icontains', label='Country')

	class Meta:
		model = Tweets
		fields = ['tweet', 'country', 'gender_predicted', 'dateTime', 'sentiment_type']
