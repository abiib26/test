from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms import modelform_factory
from django.db.models import Count
# Create your views here.
from datetime import *
from .models import *
from accounts.models import User
from django.db import connection
from .filters import FilterServeds,FilterServeds2

from .forms import ServicesForm,mchForm,stafForm,orderForm,Comments,UserForm
#
from django.utils import timezone
import pytz
import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .decorators import unauthenticated_user, allowed_users,admin_only



@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def combine(adate, atime, tz=None, is_dst=None):
    """Turn a date and a time into a datetime in given timezone (or default).

    The ``is_dst`` argument controls the handling of ambiguous datetimes
    (e.g. during fall DST changeover), and nonexistent datetimes (e.g. during
    spring DST changeover). If it is ``None`` (the default), these cases will
    return ``None`` instead of a datetime. If it is ``True``, these cases will
    be resolved by always assuming DST, and if ``False`` by assuming no-DST.

    """
    tz = tz or timezone.get_current_timezone()
    naive = dt(adate.year, adate.month, adate.day, atime.hour, atime.minute)
    try:
        return tz.normalize(tz.localize(naive, is_dst=is_dst))
    except pytz.InvalidTimeError:
        return None

@login_required(login_url='login') 
@admin_only
def home(request):
    serveds = servedPatients.objects.all()
    totalstaffs = User.objects.all().count()
    total_serveds = serveds.count()

    today = date.today() 
   
    orders =order.objects.filter(date_created__year=today.year, date_created__month=today.month, date_created__day=today.day).values('id','date_created','name__name')
    cmt = Comment.objects.all()
    pending=cmt.count()


    mch = MCH.objects.all()
    mchs = mch.count()

    




    context = {'serveds':serveds,'mchs':mchs,'mch':mch,'totalstaffs':totalstaffs,'pending':pending,'total_serveds':total_serveds,'orders':orders }

    return render(request, 'dashboard.html', context)
    
def corona(request):
    return render(request, "dwaa.html")
    

def home2(request):
    """sql = '''SELECT name FROM serverPatients s INNER JOIN staff sf
    on s.staff = sf.name INNER JOIN MCH M on sf.MCH = M.name'''
    cursor = connection.cursor()
    serveds = cursor.fetchall()"""
    #serveds = servedPatients.objects.raw('''select * from servedPatients where staff.id==1''')
    #serveds = servedPatients.objects.filter(staff__id=1,mchid=MCH.objects.get(name='jigjiga yar mch'))
    serveds =servedPatients.objects.select_related('User__MCH')

    """cursor = connection.cursor()
    cursor.execute('''SELECT * FROM servedPatients s INNER JOIN staff sf
    on s.staff = sf.name INNER JOIN MCH M on sf.MCH = M.name''')
    solution = cursor.fetchall()
    print(solution)"""
    totalstaffs = staff.objects.all().count()
    total_serveds = len(list(serveds))
    cmt  = Comment.objects.all()

    userr =request.user.name
    userr1 =request.user.MCH
    
    orders = order.objects.all()
    pending=orders.count()
 

    mch = MCH.objects.all() 
    mchs = mch.count()
    print(request.user)

    formt= Comments()
    if request.method == 'POST':
        formt = Comments(request.POST)
        if formt.is_valid():
            commentss=formt.save(commit=False)
            commentss.created_by = str(request.user.name) +"@"+ str(request.user.MCH)
            commentss.save()
            
            return redirect('home')
    



    
    context = {'userr':userr,'userr1':userr1,'cmt':cmt,'formt':formt,'serveds':serveds,'mchs':mchs,'mch':mch,'totalstaffs':totalstaffs,'pending':pending,'total_serveds':total_serveds,'orders':orders }
    #LitAgent.objects.filter(author__book__year_published=2006)

    return render(request, 'dashboard2.html', context)
def comments(request,):
    formt= Comments()
    if request.method == 'POST':
        formt = Comments(request.POST)
        if formt.is_valid():
            commentss=formt.save(commit=False)
            commentss.created_by = str(request.user.name) +"@"+ str(request.user.MCH)
            commentss.save()
            
            return redirect('home')
    
    context = {'formt':formt}
    return render(request, 'dashboard2.html',context)
def report(request):
    serveds = servedPatients.objects.all().values('id','name','service__name','User__name','date_created')

    myFilter = FilterServeds(request.GET, queryset=serveds)
    serveds = myFilter.qs 
    
    


    context = {'serveds':serveds,'myFilter':myFilter,}
    return render(request, 'reports.html', context)

def report2(request):
    #serveds =servedPatients.objects.filter(User__MCH__name='xawaadle mch').values('service__name',"User__MCH__name").annotate(Count('service__name'))
    serveds2 = servedPatients.objects.all().values('service__name').annotate(Count('service'))

    myFilter2 = FilterServeds2(request.GET, queryset=serveds2)
    serveds2 = myFilter2.qs
    


    context = {'serveds2':serveds2,'myFilter2':myFilter2}
    return render(request, 'report2.html', context)
def delete(request, pk):
    note = get_object_or_404(servedPatients, pk=id).delete()
    return HttpResponseRedirect('report')
def resultData(request):
    
    services  =servedPatients.objects.values('service__name').order_by('service__name').annotate(Count('service__name'))
    
    for i in services:
        print({i['service__name']})
    return JsonResponse(list(services),safe =False)
def TestData(request):
    services  =servedPatients.objects.values('service__name').order_by('service__name').annotate(Count('service__name'))
    

    return JsonResponse(list(services),safe =False)

def create_service(request,):
    formm= ServicesForm()
    if request.method == 'POST':
        formm = ServicesForm(request.POST)
        if formm.is_valid():
            commentss=formm.save(commit=False)
            commentss.User = request.user
            commentss.MCH = request.user.MCH
            commentss.save()
            return redirect('home')
    
    context = {'formm':formm}
    return render(request, 'createService.html',context)
  
def create_order(request,):
    userr =User.objects.filter(email=request.user).values('MCH__name')
    #formm = inlineformset_factory(bills, order, fields=('name','description','created_by','done'), extra=3 )
    orderformset = modelformset_factory(order, form=orderForm,extra=3)
    queryset = order.objects.none()
    formset = orderformset(request.POST or None,queryset=queryset)
    if formset.is_valid():
        formset.save()
        
        return redirect('home')

    #formm = modelform_factory(order, fields=('name','description','created_by','done'), extra=3)
    #ormm= orderForm()
    """if request.method == 'POST':
        formm = formms(request.POST)
        if formm.is_valid():                     
            orders=formm.save(commit=False)
            orders.created_by = request.user
            orders =order.save()            
        return redirect('home')"""
    
    context = {'formset':formset}
    return render(request, 'createOrder.html',context)
def create_mch(request,):
    formm= mchForm()
    if request.method == 'POST':
        formm = mchForm(request.POST)
        if formm.is_valid():
            formm.save()
            return redirect('home')
    
    context = {'formc':formm}
    return render(request, 'createMCH.html',context)
def create_staff(request,):
    formt= stafForm()
    if request.method == 'POST':
        formt = stafForm(request.POST)
        if formt.is_valid():
            formt.save()
            return redirect('home')
    
    context = {'formt':formt}
    return render(request, 'createStaff.html',context)
def create_User(request,):
    formt= UserForm()
    if request.method == 'POST':
        formt = UserForm(request.POST)
        if formt.is_valid():
            formt.save()
            return redirect('home')
    
    context = {'formt':formt}
    return render(request, 'createuser.html',context)

"""def mchome(request, pk_test):
    mchs = MCH.objects.get(id=pk_test)

    #orders = customer.order_set.all()
    #order_count = orders.count()

    #myFilter = OrderFilter(request.GET, queryset=orders)
    #orders = myFilter.qs 

    context = {'mchs':mchs}
    return render(request, 'mchtemple.html',context)"""
    
def product(request):
	#qs = servedPatients.objects.filter(mov_date__month=1).annotate(day=ExtractDay('date_created'),).values('day').annotate(n=Count('id')).order_by('day')
	qs= servedPatients.objects.extra({'created':"date(date_created)"}).values('date_created').annotate(created_count=Count('id'))
	context = {'qs':qs}
	return render(request, 'chart.html',context)
def resultsData(request):
	##votedata=[]

	services  =servedPatients.objects.values('service').order_by('service').annotate(count=Count('service')).values('service', 'count')
	
	return JsonResponse(list(services),safe =False)
    
def orderTable(request):
    water = order.objects.filter(id=1)
    electer = order.objects.filter(id=2)
    infra = order.objects.filter(id=3)
    
    context = {'water':water,'electer':electer,'infra':infra}
    return render(request, 'pricing-table.html',context)
    
    
def csv_download(request):
    serveds = servedPatients.objects.all()

    myFilter = FilterServeds(request.GET, queryset=serveds)
    serveds = myFilter.qs 

    response = HttpResponse(content_type = 'txt/csv')
    response['Content-Dispostion'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response,delimiter =',')
    writer.writerow(['name','service','User','dateCreated'])
    for i in serveds:
        writer.writerow([i.name,i.service,i.User,i.date_created])
    return response

def center(request):

    mchs=MCH.objects.all() 
    context = {'mchs':mchs, }
    return render(request, 'center.html',context)


def customers(request,pk):

    Serveds = servedPatients.objects.filter(User__MCH__id=pk).values('name','service__name','User__name','date_created')
    mchname =MCH.objects.get(id=pk)
    mchnames =MCH.objects.all()

    total_count =Serveds.count()
    a=staff.objects.filter(MCH__id=pk).count()
    b=MCH.objects.all()
    pks= get_object_or_404(MCH, pk=1) 

    serveds1 =servedPatients.objects.filter(User__MCH__name='xawaadle mch').values('User__staffType__name').annotate(Count('User__staffType__name'))

    context = {'Serveds':Serveds,'serveds1':serveds1, 'mchname':mchname, 'total_count':total_count,'a':a,'b':b,'pks':pks}
    return render(request, 'mchtemple.html',context)
def StaffUser(request):

    staffUsers = User.objects.all().values('name','email','staffType__name','MCH__name','last_login')
     
    context = {'staffUsers':staffUsers,}
    return render(request, 'staffs.html',context)

def view_order(request,id):
    obj =get_object_or_404(order,id=id)
    if request.method =='POST':
        a =order.objects.filter(id = id).update(viewed_by =str(request.user))
        return redirect('home')
    
    context = {'obj':obj}
    return render(request, 'vieworder.html',context)

def view_comments(request):
    

    formt= Comments()
    if request.method == 'POST':
        formt = Comments(request.POST)
        if formt.is_valid():
            commentss=formt.save(commit=False)
            commentss.created_by = str(request.user.name) +"@"+ str(request.user.MCH)
            commentss.save()
            
            return redirect('view_comments')
    cmt  = Comment.objects.all()
    context = {'cmt':cmt,'formt':formt}
    return render(request, 'commentviiew.html',context)

def delete_served(request, pk):
	item = servedPatients.objects.get(id=pk)
	if request.method == "POST":
		item.delete()
		return redirect('/report')

	context= {'item':item}
	return render(request, 'delete.html',context)

