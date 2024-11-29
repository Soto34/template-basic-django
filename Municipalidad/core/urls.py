from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('register',register,name='register'),

    #crud adultos
    path('detalleAdultos',detalleAdultos,name='detalleAdultos'),
    path('detalleAdultos/add/',adultoAdd,name='adultoAdd'),
    path('detalleAdultos/update/<id>/',adultoUpdate,name='adultoUpdate'),
    path('detalleAdultos/Delete/<id>/',adultoDelete,name='adultoDelete'),
    

    #crud talletes
    path('detalleTalleres',detalleTalleres,name='detalleTalleres'),
    path('detalleTalleres/add/',tallerAdd,name='tallerAdd'),
    path('detalleTalleres/update/<id>/',tallerUpdate,name='tallerUpdate'),
    path('detalleTalleres/Delete/<id>/',tallerDelete,name='tallerDelete'),
    
]