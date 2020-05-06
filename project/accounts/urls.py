from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('home', views.home, name="home"),
    path('home2', views.home2, name="home2"),
    path('TesttData', views.TestData, name="TestData"),
    path('report', views.report, name="report"),
    path('report2', views.report2, name="report2"),
    path('create_service', views.create_service, name="create_service"),
    path('create_order', views.create_order, name="create_order"),
    path('create_mch', views.create_mch, name="create_mch"),
    path('create_User', views.create_User, name="create_User"),
    path('create_staff', views.create_staff, name="create_staff"),
    path('resultData', views.resultData, name="resultData"),
    path('TesttData', views.TestData, name="TestData"),
    path('product/', views.product,name='product'),
    path('resultsData/', views.resultsData,name='resultsData'),
    path('corona/', views.corona, name='corona'),
    path('csv_download/', views.csv_download,name='csv_download'),
    path('orderTable/', views.orderTable,name='orderTable'),
    path('MCHome/', views.center,name='MCHome'),
   # path('Bymch/<str:pk>/', views.customer,name='Bymch'),
    path('MCHomes/<str:pk>/', views.customers,name='MCHomes'),
    path('staffs/', views.StaffUser,name='staffs'),
    path('view_order/<int:id>', views.view_order,name='view_order'),
    path('view_comments/', views.view_comments,name='view_comments'),
    #path('delete/<int:id>/$', views.delete,name='delete')
    path('report/delete/<str:pk>/', views.delete_served,name='delete'),
    #path('mchome/<str:pk_test>/', views.mchome, name="mchome"),
]
