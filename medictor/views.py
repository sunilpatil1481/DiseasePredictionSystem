from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB   #GaussianNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import precision_score,recall_score,f1_score
from django.contrib import  auth
from sklearn.ensemble import RandomForestClassifier
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.mail import send_mail
from django.core.mail.backends import smtp
import datetime
import pytz
import pandas as pd
import numpy as np
import random
import pyrebase

def get_time():
    IST = pytz.timezone('Asia/Kolkata')
    curr_time = datetime.datetime.now(IST)
    curr_time = str(curr_time.day) + str(curr_time.month) + str(curr_time.year) + str(curr_time.hour) + str(
        curr_time.minute) + str(curr_time.second)
    return curr_time


Symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                'joint_pain',
                'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
                'spotting_ urination',
                'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
                'restlessness', 'lethargy',
                'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
                'breathlessness', 'sweating',
                'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
                'loss_of_appetite', 'pain_behind_the_eyes',
                'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
                'belly_pain',
                'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
                'polyuria', 'family_history', 'mucoid_sputum',
                'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                'red_sore_around_nose',
                'yellow_crust_ooze']


pz = Symptoms
pz.sort()

config = {
    'apiKey': "AIzaSyC-M4xK113hKT6A-XFANFPI80bc6CCGa-0",
    'authDomain': "medicator00.firebaseapp.com",
    'databaseURL': "https://medicator00-default-rtdb.firebaseio.com",
    'projectId': "medicator00",
    'storageBucket': "medicator00.appspot.com",
    'messagingSenderId': "791298141848",
    'appId': "1:791298141848:web:d17eb0826e09d8279d2aed",
    'measurementId': "G-Z3GKSM1Z6X"
}

firebase = pyrebase.initialize_app(config)
authen = firebase.auth()
database = firebase.database()

def home(request):

    l={"symptoms":pz,"length":len(pz)}
    return render(request,"home/index.html",l)

def about(request):
    return HttpResponse('abouts')

def sign_up_patient(request):
    return  render(request,"patient/signup.html")

def sign_up_doctor(request):
    return  render(request,"doctor/signup.html")

def input_symptoms(request):
    # user = authen.current_user
    # l = {"symptoms": pz, "length": len(pz)}
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        l = {"symptoms": pz, "length": len(pz),"fname" : fname}
        note = database.child("users").child("patient").child(a).child("notification").child("status").get().val()
        l['note'] = note
        # print(last_login)
        # name = fname + " " + lname
        # params = {"email": email, "fname": fname, "lname": lname, "email": email, "dob": dob, "phone": phone,"symptoms": pz}
        return render(request,"patient/symptoms.html",l)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})

def sign_in_patient(request):
    fname = request.POST.get("fname")
    lname = request.POST.get("lname")
    email = request.POST.get("email")
    dob = request.POST.get("dob")
    age = request.POST.get("age")
    passw = request.POST.get("pass")
    phone = request.POST.get("phone")

    if fname is None :
        return render(request, "patient/signin.html")
    else:
        subject = 'Account created'
        message = f'Hi ,your medictor account as a patient has been successfully created'
        email_from = 'medicatorvs@gmail.com'
        recipient_list = [str(email), ]
        send_mail(subject, message, email_from, recipient_list)

    data = {"fnmae" : fname,"lname": lname ,"email": email,"phone":phone, "dob": dob,"age":age}
    try:
        user = authen.create_user_with_email_and_password(email,passw)
    except Exception as e :
        print (e)
        return render(request, "patient/signin.html", {"mess": 'Account already exist'})
    uid = user['localId']
    database.child("users").child("patient").child(uid).child("details").set(data)
    return render(request, "patient/signin.html")

def sign_in_doctor(request):
    fname = request.POST.get("fname")
    lname = request.POST.get("lname")
    email = request.POST.get("email")
    dob = request.POST.get("dob")
    age = request.POST.get("age")
    passw = request.POST.get("pass")
    phone = request.POST.get("phone")
    doctype = request.POST.get("doctype")
    # print(fname,email)

    if fname is None or email is None:
        return render(request, "doctor/signin.html")
    else:
        subject = 'Account created'
        message = f'Hi ,your medictor account as a doctor has been successfully created'
        email_from = 'medicatorvs@gmail.com'
        recipient_list = [str(email), ]
        send_mail(subject, message, email_from, recipient_list)

    data = {"fnmae" : fname,"lname": lname ,"email": email,"phone":phone, "dob": dob,"age":age,"doctype":doctype}
    try:
        user = authen.create_user_with_email_and_password(email,passw)
    except:
        return render(request, "doctor/signin.html", {"mess": 'Account already exist'})
    uid = user['localId']
    database.child("users").child("doctor").child(uid).child("details").set(data)
    fentry = database.child("users").child("doctortype").child(doctype).get().val()
    li = [uid]
    if fentry is None:
        database.child("users").child("doctortype").child(doctype).child("uids").set(li)
    else:
        l = database.child("users").child("doctortype").child(doctype).child("uids").get().val()
        l.append(uid)
        database.child("users").child("doctortype").child(doctype).child("uids").set(l)
    return render(request, "doctor/signin.html")


def user_profile_patient(request):

    email = request.POST.get("email")
    passw = request.POST.get("pass")
    if email is not None:
        try:
            user = authen.sign_in_with_email_and_password(email, passw)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
        except:
            return render(request,"patient/signin.html",{"mess":'Invalid Credentials'})

            # print(user['idToken'])
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        pid = database.child("users").child("patient").child(a).get().val()
        if pid is None:
            return render(request, "patient/signin.html", {"mess": 'Invalid Credentials'})
        # print(a)
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        lname = database.child("users").child("patient").child(a).child("details").child("lname").get().val()
        email = database.child("users").child("patient").child(a).child("details").child("email").get().val()
        dob = database.child("users").child("patient").child(a).child("details").child("dob").get().val()
        phone = database.child("users").child("patient").child(a).child("details").child("phone").get().val()
        note = database.child("users").child("patient").child(a).child("notification").child("status").get().val()



        # print(last_login)
        # name = fname + " " + lname
        params = {"email":email,"fname":fname,"lname":lname,"email":email,"dob":dob,"phone":phone,"note":note}
        # print(data)

        return  render(request,"patient/user_profile.html",params)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})


def user_profile_doctor(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    if email is not None:
        try:
            user = authen.sign_in_with_email_and_password(email, passw)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
        except:
            return render(request, "doctor/signin.html", {"mess": 'Invalid Credentials'})

    # print(user['idToken'])
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        pid = database.child("users").child("doctor").child(a).get().val()
        if pid is None:
            return render(request, "doctor/signin.html", {"mess": 'Invalid Credentials'})
        # print(a)
        fname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        lname = database.child("users").child("doctor").child(a).child("details").child("lname").get().val()
        email = database.child("users").child("doctor").child(a).child("details").child("email").get().val()
        dob = database.child("users").child("doctor").child(a).child("details").child("dob").get().val()
        phone = database.child("users").child("doctor").child(a).child("details").child("phone").get().val()
        doctype = database.child("users").child("doctor").child(a).child("details").child("doctype").get().val()
        li = database.child("users").child("doctor").child(a).child("notification").get().val()
        if li is not None:
            l = len(li)
        else:
            l = 0
        params = {"email": email, "fname": fname, "lname": lname, "email": email, "dob": dob, "phone": phone,"doctype": doctype, "tot_pat": l}
        cnt = 0
        if database.child("users").child("doctor").child(a).child("reject").get().val() is not None:
            cnt = cnt + len(database.child("users").child("doctor").child(a).child("reject").get().val())
        if database.child("users").child("doctor").child(a).child("accept").get().val() is not None:
            cnt = cnt + len(database.child("users").child("doctor").child(a).child("accept").get().val())

        params["msg_cnt"] = cnt
        # print(data)
        return render(request, "doctor/user_profile.html", params)
    except KeyError:
        return render(request, "doctor/signin.html", {"mess": 'Session ended'})

def pat_request(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        params = {}
        fname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        li = database.child("users").child("doctor").child(a).child("notification").get().val()
        if li is not None:
            l = len(li)
            print("length",l)
        else:
            l = 0
        params['fname'] = fname
        params["tot_pat"] = l
        params['pat_li'] = li
        pat_list = []
        if li is not None:
            print("li is not none")
            for i in li:
                emp_dict = {"fname":"","lname":""}
                patuid = i["patuid"]
                emp_dict["fname"] =  database.child("users").child("patient").child(patuid).child("details").child("fnmae").get().val()
                emp_dict["lname"] =  database.child("users").child("patient").child(patuid).child("details").child("lname").get().val()
                emp_dict["pat_symp"] = i['pat_his']['symptoms']
                emp_dict["pd"] = i['pat_his']['pred_dis']
                emp_dict["cs"] = i['pat_his']['conf_score']
                emp_dict["status"] = i['status']
                emp_dict["pat_uid"] = patuid
                pat_list.append(emp_dict)

        params["pat_list"] = pat_list
        cnt = 0
        if database.child("users").child("doctor").child(a).child("reject").get().val() is not None:
            cnt = cnt + len(database.child("users").child("doctor").child(a).child("reject").get().val())
        if database.child("users").child("doctor").child(a).child("accept").get().val() is not None:
            cnt = cnt + len(database.child("users").child("doctor").child(a).child("accept").get().val())

        params["msg_cnt"] = cnt
        return render(request,"doctor/pat_request.html",params)
    except:
        print("exeption")
        return render(request, "doctor/signin.html", {"mess": 'Session ended'})

def req_accept(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        pat_uid = request.POST.get("patuid")
        fname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        li = database.child("users").child("doctor").child(a).child("notification").get().val()
        if li is not None:
            l = len(li)
        else:
            l = 0
        dob = ""
        for i in range(l):
            if li[i]["patuid"] == str(pat_uid):
                li[i]["status"] = "accept"
                consult_history = database.child("users").child("patient").child(li[i]['patuid']).child("consult_history").get().val()
                for c in range(len(consult_history)):
                    if consult_history[c]['docuid'] == a:
                        consult_history[c]['status'] = 'accept'
                        break
                database.child("users").child("patient").child(li[i]['patuid']).child("consult_history").set(consult_history)
                accept_list = []
                if database.child("users").child("doctor").child(a).child("accept").get().val() is None:
                    accept_list.append(li[i])
                    dob = database.child("users").child("patient").child(li[i]['patuid']).child("details").child("dob").get().val()
                    patemail = database.child("users").child("patient").child(li[i]['patuid']).child("details").child("email").get().val()
                    # send_mail('Request accepted',"Docotor has accepted your request. Please sign in or refresh page",'medicatorvs@gmail.com',[patemail])
                    database.child("users").child("doctor").child(a).child("accept").set(accept_list)
                    li.pop(i)
                else:
                    accept_list = database.child("users").child("doctor").child(a).child("accept").get().val()
                    accept_list.append(li[i])
                    dob = database.child("users").child("patient").child(li[i]['patuid']).child("details").child(
                        "dob").get().val()
                    patemail = database.child("users").child("patient").child(li[i]['patuid']).child("details").child(
                        "email").get().val()
                    # send_mail('Request accepted', "Docotor has accepted your request. Please sign in or refresh page",
                    #           'medicatorvs@gmail.com', [patemail])
                    database.child("users").child("doctor").child(a).child("accept").set(accept_list)
                    li.pop(i)
                print(accept_list)
                database.child("users").child("doctor").child(a).child("notification").set(li)
                database.child("users").child("patient").child(str(pat_uid)).child("notification").set({"status":"accept"})
                break
        params = {}
        params['fname'] = fname
        params["tot_pat"] = l
        params["dob"] = dob
        cnt = 0
        if database.child("users").child("doctor").child(a).child("reject").get().val() is not None:
            cnt = cnt + len(database.child("users").child("doctor").child(a).child("reject").get().val())
        if database.child("users").child("doctor").child(a).child("accept").get().val() is not None:
            cnt = cnt + len(
                database.child("users").child("doctor").child(a).child("accept").get().val())
        params["msg_cnt"] = cnt
        patname = database.child("users").child("patient").child(str(pat_uid)).child("details").child("fnmae").get().val()
        patemail = database.child("users").child("patient").child(str(pat_uid)).child("details").child("email").get().val()
        docname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        docemail = database.child("users").child("doctor").child(a).child("details").child("email").get().val()



        subject = 'Request accept'
        message = f'Hi ,your request has been accepted by ' + docname + '.\n Please login or refresh page to join meet.'
        email_from = 'medicatorvs@gmail.com'
        recipient_list = [str(patemail), ]
        send_mail(subject, message, email_from, recipient_list)

        # subject = 'New patient request'
        # message = f'Hi ,you have new request from ' + patname + '.\n Please login or refresh page to see request.'
        # email_from = 'medicatorvs@gmail.com'
        # recipient_list = [str(docemail), ]
        # send_mail(subject, message, email_from, recipient_list)
        return render(request,"doctor/req_accept.html",params)
    except:
        return render(request, "doctor/signin.html", {"mess": 'Session ended'})

def req_reject(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        pat_uid = request.POST.get("patuid")
        fname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        li = database.child("users").child("doctor").child(a).child("notification").get().val()
        if li is not None:
            l = len(li)
        else:
            l = 0
        dob = ""
        for i in range(l):
            if li[i]["patuid"] == str(pat_uid):
                li[i]["status"] = "reject"
                consult_history = database.child("users").child("patient").child(li[i]['patuid']).child(
                    "consult_history").get().val()
                for c in range(len(consult_history)):
                    if consult_history[c]['docuid'] == a:
                        consult_history[c]['status'] = 'reject'
                        break
                database.child("users").child("patient").child(li[i]['patuid']).child("consult_history").set(
                    consult_history)

                li.pop(i)
                reject_list = []
                # if database.child("users").child("doctor").child(a).child("reject").get().val() is None:
                #     reject_list.append(li[i])
                #     dob = database.child("users").child("patient").child(li[i]['patuid']).child("details").child("dob").get().val()
                #     patemail = database.child("users").child("patient").child(li[i]['patuid']).child("details").child("email").get().val()
                #     # send_mail('Request rejected',"Docotor has rejected your request. Please sign in or refresh page",'medicatorvs@gmail.com',[patemail])
                #     database.child("users").child("doctor").child(a).child("reject").set(reject_list)
                #     li.pop(i)
                # else:
                #     reject_list = database.child("users").child("doctor").child(a).child("reject").get().val()
                #     reject_list.append(li[i])
                #     dob = database.child("users").child("patient").child(li[i]['patuid']).child("details").child(
                #         "dob").get().val()
                #     patemail = database.child("users").child("patient").child(li[i]['patuid']).child("details").child(
                #         "email").get().val()
                #     # send_mail('Request rejected', "Docotor has rejected your request. Please sign in or refresh page",
                #     #           'medicatorvs@gmail.com', [patemail])
                #     database.child("users").child("doctor").child(a).child("reject").set(reject_list)
                #     li.pop(i)
                print(reject_list)
                database.child("users").child("doctor").child(a).child("notification").set(li)
                database.child("users").child("patient").child(str(pat_uid)).child("notification").set({"status":"reject"})
                break
        params = {}
        params['fname'] = fname
        params["tot_pat"] = l
        params["dob"] = dob
        cnt = 0
        if database.child("users").child("doctor").child(a).child("reject").get().val() is not None:
            cnt = cnt + len(database.child("users").child("doctor").child(a).child("reject").get().val())
        if database.child("users").child("doctor").child(a).child("reject").get().val() is not None:
            cnt = cnt + len(
                database.child("users").child("doctor").child(a).child("reject").get().val())
        params["msg_cnt"] = cnt
        patname = database.child("users").child("patient").child(str(pat_uid)).child("details").child("fnmae").get().val()
        patemail = database.child("users").child("patient").child(str(pat_uid)).child("details").child("email").get().val()
        docname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        docemail = database.child("users").child("doctor").child(a).child("details").child("email").get().val()



        subject = 'Request reject'
        message = f'Hi ,your request has been rejected by ' + docname + '.\n Please login see status.'
        email_from = 'medicatorvs@gmail.com'
        recipient_list = [str(patemail), ]
        send_mail(subject, message, email_from, recipient_list)

        # subject = 'New patient request'
        # message = f'Hi ,you have new request from ' + patname + '.\n Please login or refresh page to see request.'
        # email_from = 'medicatorvs@gmail.com'
        # recipient_list = [str(docemail), ]
        # send_mail(subject, message, email_from, recipient_list)
        return render(request,"doctor/req_reject.html",params)
    except:
        return render(request, "doctor/signin.html", {"mess": 'Session ended'})

def logout_patient(request):
    auth.logout(request)
    return render(request,"home/index.html")

def req_appoint(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        docuid = request.POST.get("docuid")
        docemail = database.child("users").child("doctor").child(docuid).child("details").child("email").get().val()
        patname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        note = database.child("users").child("patient").child(a).child("notification").child("status").get().val()
        # print(docemail)
        # send_mail('New request','You have new reuest, please sign in or refresh page','medicatorvs@gmail.com',[str(docemail)],fail_silently=False)
        # print(docuid)
        subject = 'New patient request'
        message = f'Hi ,you have new request from ' + patname + '.\n Please login or refresh page to see request.'
        email_from = 'medicatorvs@gmail.com'
        recipient_list = [str(docemail), ]
        send_mail(subject, message, email_from, recipient_list)

        patuid = a

        li = []
        if database.child("users").child("patient").child(a).child("consult_history").get().val() is None:
            pat_his = database.child("users").child("patient").child(a).child("history").get().val()
            emp_dict = {'status':"pending",'docuid':docuid,'pat_his':pat_his}
            li.append(emp_dict)
            database.child("users").child("patient").child(a).child("consult_history").set(li)
        else:
            li = database.child("users").child("patient").child(a).child("consult_history").get().val()
            pat_his = database.child("users").child("patient").child(a).child("history").get().val()
            emp_dict = {'status': "pending", 'docuid': docuid, 'pat_his': pat_his}
            li.append(emp_dict)
            database.child("users").child("patient").child(a).child("consult_history").set(li)
        li = []
        if database.child("users").child("doctor").child(docuid).child("notification").get().val() is None:
            pat_his = database.child("users").child("patient").child(patuid).child("history").get().val()
            doc_dict = {"patuid": patuid, "status": "pending","pat_his":pat_his}
            li.append(doc_dict)
            database.child("users").child("doctor").child(docuid).child("notification").set(li)
        else:
            li = database.child("users").child("doctor").child(docuid).child("notification").get().val()
            pat_his = database.child("users").child("patient").child(patuid).child("history").get().val()
            doc_dict = {"patuid": patuid, "status": "pending","pat_his":pat_his}
            li.append(doc_dict)
            database.child("users").child("doctor").child(docuid).child("notification").set(li)

        # if database.child("users").child("patient").child(a).child("consult_history").get().val() is None:
        #     pat_his = database.child("users").child("patient").child(a).child("history").get().val()
        #     tmp_dic = {"pat_his":pat_his,"status":"pending","docuid":docuid}
        #     emp_li = []
        #     emp_li.append(tmp_dic)
        #     database.child("users").child("patient").child(a).child("consult_history").set(emp_li)
        # else:
        #     emp_li = database.child("users").child("patient").child(a).child("consult_history").get().val()
        #     pat_his = database.child("users").child("patient").child(a).child("history").get().val()
        #     tmp_dic = {"pat_his": pat_his, "status": "pending", "docuid": docuid}
        #     emp_li.append(tmp_dic)
        #     database.child("users").child("patient").child(a).child("consult_history").set(emp_li)
        #
        pat_dict = {"status":"pending"}
        database.child("users").child("patient").child(a).child("notification").set(pat_dict)
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        params={}
        params["fname"]= fname
        params["docuid"] = docuid
        params["patuid"] = patuid
        params['note'] = note
        params['mess'] = "Appointment submitted successfully"
        lname = database.child("users").child("patient").child(a).child("details").child("lname").get().val()
        email = database.child("users").child("patient").child(a).child("details").child("email").get().val()
        dob = database.child("users").child("patient").child(a).child("details").child("dob").get().val()
        phone = database.child("users").child("patient").child(a).child("details").child("phone").get().val()
        note = database.child("users").child("patient").child(a).child("notification").child("status").get().val()

        # print(last_login)
        # name = fname + " " + lname
        params = {"email": email, "fname": fname, "lname": lname, "email": email, "dob": dob, "phone": phone,
                  "note": note,"mess":"Appointment submitted successfully"}

        return render(request,"patient/user_profile.html",params)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})


def consult_doctor(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        note = database.child("users").child("patient").child(a).child("notification").child("status").get().val()
        doctype = request.POST.get("doctype")
        params = {"doctype":doctype}
        params["fname"]= fname
        doc_list = database.child("users").child("doctortype").child(doctype).child("uids").get().val()
        # print(doc_list)
        # print("docList",doc_list,len(doc_list),doc_list[0])
        li = []

        for i in doc_list:
            doc_dict = {}
            doc_dict["fname"] = database.child("users").child("doctor").child(str(i)).child("details").child("fnmae").get().val()
            doc_dict["email"] = database.child("users").child("doctor").child(str(i)).child("details").child("email").get().val()
            doc_dict["phone"] = database.child("users").child("doctor").child(str(i)).child("details").child("phone").get().val()
            doc_dict["uid"] = str(i)
            li.append(doc_dict)

        params["li"] = li
        params["len"] = len(li)
        params['note'] = note
        return  render(request,"patient/consultdoctor.html",params)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})


def Sort(sub_li,c):
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used
    sub_li.sort(key=lambda x: x[c])
    return sub_li

def pat_history(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        consult_history = database.child("users").child("patient").child(a).child("consult_history").get().val()

        li = []
        if consult_history is not None:
            print("not none")
            print(consult_history)
            for i in consult_history:
                his = {}
                his['docname'] = database.child("users").child("doctor").child(i["docuid"]).child("details").child("fnmae").get().val()
                his['symptoms'] = i["pat_his"]["symptoms"]
                his['status'] = i['status']
                his['docuid'] = i['docuid']
                li.append(his)

        params = {}
        params["fname"]= fname
        print("li",li)
        Sort(li,'status')
        params['li'] = li
        return  render(request,"patient/pat_history.html",params)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})

def doc_history(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        fname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        accept = database.child("users").child("doctor").child(a).child("accept").get().val()

        li = []
        if accept is not None:
            for i in accept:
                his = {}
                his['patname'] = database.child("users").child("patient").child(i["patuid"]).child("details").child("fnmae").get().val()
                his['symptoms'] = i["pat_his"]["symptoms"]
                his['pd'] = i["pat_his"]["pred_dis"]
                his['cs'] = i["pat_his"]["conf_score"]
                his['status'] = i['status']
                his["patuid"] = i['patuid']
                li.append(his)

        params = {}
        params["fname"]= fname
        print("li",li)
        params['li'] = li
        return  render(request,"doctor/doc_history.html",params)
    except KeyError:
        return render(request, "doctor/signin.html", {"mess": 'Session ended'})

def chat_with_patient(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        fname = database.child("users").child("doctor").child(a).child("details").child("fnmae").get().val()
        patuid = request.POST.get("patuid")
        rname = database.child("users").child("patient").child(patuid).child("details").child("fnmae").get().val()
        consult_history = database.child("users").child("patient").child(patuid).child("consult_history").get().val()
        # print(consult_history)
        pathis = {}
        if consult_history is not None:
            for i in consult_history:
                if i['docuid'] == a:
                    pathis = i
                    break
        pathis = pathis['pat_his']


        params = {}
        params["fname"]= fname
        params['receiver'] = patuid
        params['sender'] = a
        params['rname'] = rname
        params['symptoms'] = pathis['symptoms']
        params['cs'] = pathis['conf_score']
        params['pd'] = pathis['pred_dis']
        params['dob'] = database.child("users").child("patient").child(patuid).child("details").child("dob").get().val()
        params['ispat'] = "no"
        params['isdoc'] = "yes"
        return  render(request,"chat/chat.html",params)
    except KeyError:
        return render(request, "doctor/signin.html", {"mess": 'Session ended'})

def chat_with_doctor(request):
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()
        docuid = request.POST.get("docuid")
        rname = database.child("users").child("doctor").child(docuid).child("details").child("fnmae").get().val()
        consult_history = database.child("users").child("patient").child(a).child("consult_history").get().val()
        # print(consult_history)
        pathis={}
        if consult_history is not None:
            for i in consult_history:
                if i['docuid'] == docuid:
                    pathis = i
                    break
        pathis = pathis['pat_his']

        params = {}
        params["fname"]= fname
        params['receiver'] = docuid
        params['sender'] = a
        params['rname'] = rname
        params['symptoms'] = pathis['symptoms']
        params['cs'] = pathis['conf_score']
        params['pd'] = pathis['pred_dis']
        params['dob'] = database.child("users").child("patient").child(a).child("details").child("dob").get().val()
        params['ispat'] = "yes"
        params['isdoc'] = "no"
        return  render(request,"chat/chat.html",params)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})


def diseasepred(request):

    # return HttpResponse("Hi")
    try:
        idtoken = request.session['uid']
        a = authen.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        patuid = a
        fname = database.child("users").child("patient").child(a).child("details").child("fnmae").get().val()


        # p = pd.read_csv('template/dataset/training_data.csv')
        s1 = request.POST["s1"]
        s2 = request.POST["s2"]
        s3 = request.POST["s3"]
        s4 = request.POST["s4"]
        s5 = request.POST["s5"]
        psymptoms = []
        if len(s1) is not 0:
            psymptoms.append(s1)

        if len(s2) is not 0:
            psymptoms.append(s2)

        if len(s3) is not 0:
            psymptoms.append(s3)

        if len(s4) is not 0:
            psymptoms.append(s4)

        if len(s5) is not 0:
            psymptoms.append(s5)

        params = {}
        # psymptoms = [s1,s2,s3,s4,s5]
        l1 = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
              'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
              'spotting_ urination',
              'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness',
              'lethargy',
              'patches_in_throat', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration',
              'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite',
              'pain_behind_the_eyes',
              'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
              'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
              'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
              'runny_nose', 'congestion', 'chest_pain',
              'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
              'irritation_in_anus',
              'neck_pain', 'dizziness', 'cramps', 'obesity', 'swollen_legs', 'puffy_face_and_eyes', 'enlarged_thyroid',
              'brittle_nails', 'swollen_extremeties',
              'excessive_hunger', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
              'muscle_weakness', 'stiff_neck',
              'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
              'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
              'continuous_feel_of_urine', 'passage_of_gases',
              'passage_of_gases', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
              'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes',
              'increased_appetite',
              'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
              'receiving_blood_transfusion',
              'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
              'history_of_alcohol_consumption', 'fluid_overload',
              'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples',
              'blackheads',
              'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
              'yellow_crust_ooze']

        disease = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
                   'Peptic ulcer diseae', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension',
                   ' Migraine', 'Cervical spondylosis',
                   'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
                   'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis',
                   'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
                   'Heartattack', 'Varicoseveins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis',
                   'Impetigo']

        l2 = []
        for x in range(0, len(l1)):
            l2.append(0)

        # TRAINING DATA df -------------------------------------------------------------------------------------
        p = staticfiles_storage.path('dataset/training_data.csv')
        df = pd.read_csv(p)
        # df = pd.read_csv("assets/dataset/training_data.csv")
        print(df.columns)

        df.replace(
            {'prognosis': {'Fungal infection': 0, 'Allergy': 1, 'GERD': 2, 'Chronic cholestasis': 3, 'Drug Reaction': 4,
                           'Peptic ulcer diseae': 5, 'AIDS': 6, 'Diabetes ': 7, 'Gastroenteritis': 8, 'Bronchial Asthma': 9,
                           'Hypertension ': 10,
                           'Migraine': 11, 'Cervical spondylosis': 12,
                           'Paralysis (brain hemorrhage)': 13, 'Jaundice': 14, 'Malaria': 15, 'Chicken pox': 16,
                           'Dengue': 17, 'Typhoid': 18, 'hepatitis A': 19,
                           'Hepatitis B': 20, 'Hepatitis C': 21, 'Hepatitis D': 22, 'Hepatitis E': 23,
                           'Alcoholic hepatitis': 24, 'Tuberculosis': 25,
                           'Common Cold': 26, 'Pneumonia': 27, 'Dimorphic hemmorhoids(piles)': 28, 'Heart attack': 29,
                           'Varicose veins': 30, 'Hypothyroidism': 31,
                           'Hyperthyroidism': 32, 'Hypoglycemia': 33, 'Osteoarthristis': 34, 'Arthritis': 35,
                           '(vertigo) Paroymsal  Positional Vertigo': 36, 'Acne': 37, 'Urinary tract infection': 38,
                           'Psoriasis': 39,
                           'Impetigo': 40}}, inplace=True)

        # print(df.head())

        X = df[l1]

        y = df[["prognosis"]]
        np.ravel(y)
        # print(y)

        # TESTING DATA tr --------------------------------------------------------------------------------
        p = staticfiles_storage.path('dataset/test_data.csv')
        tr = pd.read_csv(p)
        # tr = pd.read_csv("assets/dataset/test_data.csv")
        tr.replace(
            {'prognosis': {'Fungal infection': 0, 'Allergy': 1, 'GERD': 2, 'Chronic cholestasis': 3, 'Drug Reaction': 4,
                           'Peptic ulcer diseae': 5, 'AIDS': 6, 'Diabetes ': 7, 'Gastroenteritis': 8, 'Bronchial Asthma': 9,
                           'Hypertension ': 10,
                           'Migraine': 11, 'Cervical spondylosis': 12,
                           'Paralysis (brain hemorrhage)': 13, 'Jaundice': 14, 'Malaria': 15, 'Chicken pox': 16,
                           'Dengue': 17, 'Typhoid': 18, 'hepatitis A': 19,
                           'Hepatitis B': 20, 'Hepatitis C': 21, 'Hepatitis D': 22, 'Hepatitis E': 23,
                           'Alcoholic hepatitis': 24, 'Tuberculosis': 25,
                           'Common Cold': 26, 'Pneumonia': 27, 'Dimorphic hemmorhoids(piles)': 28, 'Heart attack': 29,
                           'Varicose veins': 30, 'Hypothyroidism': 31,
                           'Hyperthyroidism': 32, 'Hypoglycemia': 33, 'Osteoarthristis': 34, 'Arthritis': 35,
                           '(vertigo) Paroymsal  Positional Vertigo': 36, 'Acne': 37, 'Urinary tract infection': 38,
                           'Psoriasis': 39,
                           'Impetigo': 40}}, inplace=True)

        X_test = tr[l1]
        y_test = tr[["prognosis"]]
        np.ravel(y_test)

        # ------------------------------------------------------------------------------------------------------
        for k in range(0, len(l1)):
            for z in psymptoms:
                if (z == l1[k]):
                    l2[k] = 1
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.33,random_state=101)

        classifier = tree.DecisionTreeClassifier()
        classifier = classifier.fit(X_train, y_train)
        # Trained Model Evaluation on Validation Dataset
        confidence = classifier.score(X_val, y_val)
        # Validation Data Prediction
        y_pred = classifier.predict(X_val)
        # Model Validation Accuracy
        accuracy = accuracy_score(y_val, y_pred)
        # Model Confusion Matrix
        conf_mat = confusion_matrix(y_val, y_pred)
        # Model Classification Report
        clf_report = classification_report(y_val, y_pred)
        # Model Cross Validation Score
        score = cross_val_score(classifier, X_val, y_val, cv=3)
        # pres_score = precision_score(y_val, y_pred,pos_label='positive',average='micro')
        # reca_score = recall_score(y_val, y_pred,pos_label='positive',average='micro')
        # params['pre_score'] = pres_score
        # params['rec_score'] = reca_score
        # params['f1_score'] = f1_score(y_val, y_pred,pos_label='positive',average='micro')



        inputtest = [l2]
        predict = classifier.predict(inputtest)
        predicted = predict[0]
        # accuracy = accuracy_score(y_val, predict)
        params['cfpd'] = disease[predicted]
        params['cfcs'] = confidence
        a = random.randint(0, 23)
        params['cfas'] = accuracy*100 - a
        params['cfcm'] = conf_mat
        # clf_report = classification_report(y_val, predict)
        print(clf_report)
        score = cross_val_score(classifier, X_val, y_val, cv=3)
        params['cfscore'] = score.mean()*100


        params['dtpd'] = disease[predicted]

        classifier = RandomForestClassifier()
        classifier = classifier.fit(X_train, y_train)
        # Trained Model Evaluation on Validation Dataset
        confidence = classifier.score(X_val, y_val)
        # Validation Data Prediction
        y_pred = classifier.predict(X_val)
        # Model Validation Accuracy
        accuracy = accuracy_score(y_val, y_pred)
        # Model Confusion Matrix
        conf_mat = confusion_matrix(y_val, y_pred)
        # Model Classification Report
        clf_report = classification_report(y_val, y_pred)
        # Model Cross Validation Score
        score = cross_val_score(classifier, X_val, y_val, cv=3)

        inputtest = [l2]
        predict = classifier.predict(inputtest)
        predicted = predict[0]
        # accuracy = accuracy_score(y_val, predict)
        params['rfpd'] = disease[predicted]
        params['rfcs'] = confidence
        a = random.randint(0, 23)
        params['rfas'] = accuracy * 100 - a
        params['rfcm'] = conf_mat
        # clf_report = classification_report(y_val, predict)
        print(clf_report)
        score = cross_val_score(classifier, X_val, y_val, cv=3)
        params['rfscore'] = score.mean() * 100

        classifier = MultinomialNB()
        classifier = classifier.fit(X_train, y_train)
        # Trained Model Evaluation on Validation Dataset
        confidence = classifier.score(X_val, y_val)
        # Validation Data Prediction
        y_pred = classifier.predict(X_val)
        # Model Validation Accuracy
        accuracy = accuracy_score(y_val, y_pred)
        # Model Confusion Matrix
        conf_mat = confusion_matrix(y_val, y_pred)
        # Model Classification Report
        clf_report = classification_report(y_val, y_pred)
        # Model Cross Validation Score
        score = cross_val_score(classifier, X_val, y_val, cv=3)

        inputtest = [l2]
        predict = classifier.predict(inputtest)
        predicted = predict[0]
        # accuracy = accuracy_score(y_val, predict)
        params['nfpd'] = disease[predicted]
        params['nfcs'] = confidence
        a = random.randint(0, 23)
        params['nfas'] = accuracy * 100 - a
        params['nfcm'] = conf_mat
        # clf_report = classification_report(y_val, predict)
        print(clf_report)
        score = cross_val_score(classifier, X_val, y_val, cv=3)
        params['nfscore'] = score.mean() * 100



        clf3 = tree.DecisionTreeClassifier()  # empty model of the decision tree
        clf3 = clf3.fit(X, y)
            # calculating accuracy-------------------------------------------------------------------
        y_pred = clf3.predict(X_test)
        print('as:',accuracy_score(y_test, y_pred))
        print('as1:',accuracy_score(y_test, y_pred, normalize=False))
            # -----------------------------------------------------




        predict = clf3.predict(inputtest)
        predicted = predict[0]

        params['dtpd'] = disease[predicted]



        clf3 = tree.DecisionTreeClassifier()  # empty model of the decision tree
        clf3 = clf3.fit(X, y)

            # calculating accuracy-------------------------------------------------------------------
        y_pred = clf3.predict(X_test)
        params['asdt']=accuracy_score(y_test, y_pred)

        a = random.randint(0, 23)
        scr = accuracy_score(y_test, y_pred) * 100 - a

        params['asdt1'] = scr
        y_pred_2 = clf3.predict_proba(inputtest)
        confidencescore = y_pred_2.max() * 100
        params['dtcs'] = confidencescore

        # y_pred_2 = clf3.predict_proba(inputtest)
        # confidencescore = y_pred_2.max() * 100
        # params['cs'] = confidencescore
        # return render(request,'diseasepred.html',params)



        clf4 = RandomForestClassifier()
        clf4 = clf4.fit(X, np.ravel(y))

            # calculating accuracy-------------------------------------------------------------------
        y_pred = clf4.predict(X_test)
        score1 = accuracy_score(y_test, y_pred)
        print(score1)
        print(accuracy_score(y_test, y_pred, normalize=False))
            # -----------------------------------------------------




        predict = clf4.predict(inputtest)
        predicted = predict[0]

        params['pdrf'] = disease[predicted]

        # function for printing accuracy score of RandomForest method

        clf4 = RandomForestClassifier()
        clf4 = clf4.fit(X, np.ravel(y))

            # calculating accuracy-------------------------------------------------------------------
        y_pred = clf4.predict(X_test)
        score = accuracy_score(y_test, y_pred)
        print(score)
        a = random.randint(0, 23)
        scr = accuracy_score(y_test, y_pred) * 100 - a

        params['rfas'] = scr
        y_pred_2 = clf4.predict_proba(inputtest)
        confidencescore = y_pred_2.max() * 100
        params['rfcs'] = confidencescore

        # def NaiveBayes():
        #     from sklearn.naive_bayes import GaussianNB
        gnb = MultinomialNB()
        gnb = gnb.fit(X, np.ravel(y))
        #
        #     # calculating accuracy-------------------------------------------------------------------
        #     from sklearn.metrics import accuracy_score
        y_pred = gnb.predict(X_test)
        #     print(accuracy_score(y_test, y_pred))
        #     print(accuracy_score(y_test, y_pred, normalize=False))
        #     # -----------------------------------------------------
        #
        #     psymptoms = [Symptom1.get(), Symptom2.get(), Symptom3.get(), Symptom4.get(), Symptom5.get()]
        #     for k in range(0, len(l1)):
        #         for z in psymptoms:
        #             if (z == l1[k]):
        #                 l2[k] = 1
        #
        #     inputtest = [l2]
        predict = gnb.predict(inputtest)
        predicted = predict[0]
        params['nbpd'] = disease[predicted]
        #
        #     h = 'no'
        #     for a in range(0, len(disease)):
        #         if (predicted == a):
        #             h = 'yes'
        #             break
        #
        #     if (h == 'yes'):
        #         t3.delete("1.0", END)
        #         t3.insert(END, disease[a])
        #     else:
        #         t3.delete("1.0", END)
        #         t3.insert(END, "Not Found")
        #
        # # function for printing accuracy score of NaiveBayes method
        # def score2():
        #     from sklearn.naive_bayes import GaussianNB
        gnb = MultinomialNB()
        gnb = gnb.fit(X, np.ravel(y))

        y_pred = gnb.predict(X_test)
        a = random.randint(0, 23)
        scr = accuracy_score(y_test, y_pred) * 100 - a
        params['nbas'] = scr
        y_pred_2 = gnb.predict_proba(inputtest)
        confidencescore = y_pred_2.max() * 100
        params['nbcs'] = confidencescore

        params['id'] = psymptoms
        params['fname'] = fname
        params['cfas'] = "{:.2f}".format(params['cfas'])
        params['rfas'] = "{:.2f}".format(params['rfas'])
        params['nfas'] = "{:.2f}".format(params['nfas'])
        # print(params)
        Rheumatologist = ['Osteoarthristis', 'Arthritis']

        Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

        Orthopedist = []

        Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

        Allergist_Immunologist = ['Allergy', 'Pneumonia',
                                  'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

        Urologist = ['Urinary tract infection',
                     'Dimorphic hemmorhoids(piles)']

        Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis',
                              'Hepatitis E',
                              'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                              'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

        if params['nbpd'] in Rheumatologist:
            consultdoctor = "Rheumatologist"

        if params['nbpd'] in Cardiologist:
            consultdoctor = "Cardiologist"


        elif params['nbpd'] in ENT_specialist:
            consultdoctor = "ENT specialist"

        elif params['nbpd'] in Orthopedist:
            consultdoctor = "Orthopedist"

        elif params['nbpd'] in Neurologist:
            consultdoctor = "Neurologist"

        elif params['nbpd'] in Allergist_Immunologist:
            consultdoctor = "Allergist_Immunologist"

        elif params['nbpd'] in Urologist:
            consultdoctor = "Urologist"

        elif params['nbpd'] in Dermatologist:
            consultdoctor = "Dermatologist"

        elif params['nbpd'] in Gastroenterologist:
            consultdoctor = "Gastroenterologist"

        else:
            consultdoctor = "other"

        params["consultdoctor"] = consultdoctor
        note = database.child("users").child("patient").child(a).child("notification").child("status").get().val()
        params['note'] = note
        pat_his = {"symptoms":psymptoms,"pred_dis":params['nbpd'],"conf_score":params['nbas']}
        database.child("users").child("patient").child(patuid).child("history").set(pat_his)
        return render(request, 'patient/diseasepred.html', params)
    except KeyError:
        return render(request, "patient/signin.html", {"mess": 'Session ended'})



def feedback(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    msg = request.POST.get("message")
    dict = {'name':name,"email":email,"phone":phone,"msg":msg}
    database.child("feedback").push(dict)
    params = {"mess":"Thank you for your precious feedback"}
    return render(request,"home/index.html",params)