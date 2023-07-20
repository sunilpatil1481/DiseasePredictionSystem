"""medictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path('about/',views.about,name='about'),
    path('sign_up_patient/',views.sign_up_patient,name='sign_up_patient'),
    path('user_profile_patient/',views.user_profile_patient,name='user_profile_patient'),
    path('sign_in_patient/',views.sign_in_patient,name='sign_in_patient'),
    path('diseasepred/',views.diseasepred,name="diseasepred"),
    path('logout_patient/',views.logout_patient,name="logout_patient"),
    path('input_symptoms/',views.input_symptoms,name="input_symptoms"),
    path('sign_up_doctor/',views.sign_up_doctor,name='sign_up_doctor'),
    path('user_profile_doctor/',views.user_profile_doctor,name='user_profile_doctor'),
    path('sign_in_doctor/',views.sign_in_doctor,name='sign_in_doctor'),
    path('consult_doctor/',views.consult_doctor,name='consult_doctor'),
    path('req_appoint/',views.req_appoint,name='req_appoint'),
    path('pat_request/',views.pat_request,name='pat_request'),
    path('req_accept/',views.req_accept,name='req_accept'),
    path('req_reject/',views.req_reject,name='req_reject'),
    path('pat_history/',views.pat_history,name='pat_history'),
    path('doc_history/',views.doc_history,name='doc_history'),
    path('chat_with_patient/',views.chat_with_patient,name='chat_with_patient'),
    path('chat_with_doctor/',views.chat_with_doctor,name='chat_with_doctor'),
    path('feedback/',views.feedback,name='feedback'),
]
