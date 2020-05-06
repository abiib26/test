from django.forms import ModelForm
from .models import order,servedPatients,MCH,staff,Comment
from accounts.models import User
from django import forms



class Comments(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body':forms.Textarea(
            attrs ={'class':'form-control','placeholder':'Write your Comment and message in here','rows':4}),
          
          }
        
          
class orderForm(ModelForm):
    class Meta:
        model = order
        fields = ['name','description','done']

        
        
class mchForm(ModelForm):
    class Meta:
        model = MCH
        fields = ['name','district']
        widgets = {
            'name':forms.TextInput(
            attrs ={'class':'form-control','placeholder':'name'}),
            
            

        }
class ServicesForm(ModelForm):
    class Meta:
        model = servedPatients
        fields = ['name','service',]
        widgets = {
            'name':forms.TextInput(
            attrs ={'class':'form-control','placeholder':'name'}),
            
            

        }

       
            
class stafForm(ModelForm):
    class Meta:
        model = staff
        fields = ['name','staffType','MCH','phone','email']
        widgets = {
            'name':forms.TextInput(
            attrs ={'class':'form-control','placeholder':'name'}),
            
            

        }
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email','password','name','staffType','MCH']
   
    
    
    