from django import forms
from sentiments_analysis.models import  Tweets
import django_filters

gender_choice=(
('Male','Male'),
('Female','Female'),
('Unknow','Unknow'))
sentiment_choice=(
('Positive','Positive'),
('Negative','Negative'),
('Neutral','Neutral'))
class TweetFilter(django_filters.FilterSet):
	tweet = django_filters.CharFilter(lookup_expr='icontains')
	country = django_filters.CharFilter(lookup_expr='icontains')
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
	tweet = django_filters.CharFilter(lookup_expr='icontains')
	gender_predicted = django_filters.MultipleChoiceFilter(choices=gender_choice,
        widget=forms.CheckboxSelectMultiple)

    
	class Meta:
		model = Tweets
		fields = ['tweet', 'country', 'gender_predicted', 'dateTime', 'sentiment_type']