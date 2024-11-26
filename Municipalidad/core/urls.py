from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('detalleTalleres',detalleTalleres,name='detalleTalleres'),
    path('detalleTalleres/add/',tallerAdd,name='tallerAdd'),
    path('detalleTalleres/update/<id>/',tallerUpdate,name='tallerUpdate'),
    path('detalleTalleres/Delete/<id>/',tallerDelete,name='tallerDelete'),
    path('register',register,name='register')
]