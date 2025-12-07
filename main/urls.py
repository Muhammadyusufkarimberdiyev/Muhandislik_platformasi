# urls.py
from django.urls import path,include
from .views import *

app_name = 'main'

urlpatterns = [
    # Asosiy sahifa
    path('', Home.as_view(), name='home'),
     path('login/', LoginSignupView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
   
    # Kitoblar
    path('books/', BooksPage.as_view(), name='books'),
    path('books/search/', bsearch, name='bsearch'),

    # Videolar
    path('videos/', VideosPage.as_view(), name='videos'),
    path('videos/search/', vsearch, name='vsearch'),
    
    # Tajribalar (Experiments) - Kategoriyalar ro'yxati
    path('experiments/', SectionsPage.as_view(), name='sections'),
    path('experiments/<slug:slug>/', ExperimentSection.as_view(), name='exp_section'),
    
    # Tajribalar - To'g'ridan-to'g'ri sahifalar
    path('robotselect/', RobotSelectPage.as_view(), name='robotselect'),
    path('elektrselect/', ElektrSelectPage.as_view(), name='elektrselect'),
    path('3dselect/', Select3DPage.as_view(), name='3dselect'),
    path('loyihselect/', LoyihSelectPage.as_view(), name='loyihselect'),
    
    # Tajribalar qidiruv
    path('experiments/robot/search/', asearch, name='asearch'),
    path('experiments/elektr/search/', esearch, name='esearch'),
    
    # Sinf darslari (Class)
    path('class/', ClassSectionsPage.as_view(), name='class'),
    path('classselect/', ClassSelectPage.as_view(), name='classselect'),
    path('class/search/', csearch, name='csearch'),
    

    
    # Boshqa sahifalar
    path('ai/', AIPage.as_view(), name='ai'),
    path('program/', ProgramPage.as_view(), name='program'),
    path('back/', Back.as_view(), name='back'),
]