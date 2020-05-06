import django_filters
from django_filters import DateFilter,CharFilter
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class FilterServeds(django_filters.FilterSet):
    startDate =DateFilter(field_name ='date_created',lookup_expr='gte')
    endDate =DateFilter(field_name ='date_created',lookup_expr='lte')
    #endDate =CharFilter(field_name ='note',lookup_expr='icontain')
    startDate = django_filters.DateFilter(

        widget=DateInput(
            attrs={
            
                'class': 'datepicker'
            }
        )
        )
    endDate = django_filters.DateFilter(

        widget=DateInput(
            attrs={
            
                'class': 'datepicker'
            }
        )
        )

    class Meta:
        model = servedPatients
        fields= '__all__'

        exclude = ['date_created']

        
       
        #exclude=['date_created']
class FilterServeds2(django_filters.FilterSet):
   

    class Meta:
        model = servedPatients
        fields= ['MCH']

        

        

