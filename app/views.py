#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.template import Context, loader
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate,get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models import Avg
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils import timezone
from app.models import Dashboard, Activity
from app.models import File, Survey
from app.forms import UploadFileForm, UserForm, NewUserForm, UrlForm, SurveyForm
from app import pyploma
from django.contrib.auth.models import User
from datetime import datetime,timedelta,date
from django.contrib.auth.decorators import login_required
from email.MIMEText import MIMEText
from django.utils.encoding import smart_str
from django.utils.translation import activate
from django.template import RequestContext
import smtplib
import ast
import email.utils
import os
import ast
import json
import sys
import urllib2
import shutil
import unicodedata
import csv
import zipfile
from zipfile import ZipFile


# ___________________________ MAIN _________________________________ #

def main(request):
    """Main page"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None

    print "USER -----> ", user
    print request
    # The first time one user enters
    # Create the dashboards associated to users
    createDashboards()
    return render_to_response('main/main.html',
                              {'user': user},
                              RC(request))


def redirectMain(request):
    """Page not found redirect to main"""
    return HttpResponseRedirect('/')

# _____________________________ ERROR ______________________________ #

def error404(request):
    response = render_to_response('404.html', {},
                                  context_instance = RC(request))
    response.status_code = 404
    return response


def error505(request):
    response = render_to_response('500.html', {},
                                  context_instance = RC(request))
    return response

# ___________________ TO UNREGISTERED USER _______________________ #

def selector(request):
    if request.method == 'POST':
        print request.POST

        error = False
        id_error = False
        no_exists = False
        if '_url' in request.POST:
            d = urlUnregistered(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            elif d['Error'] == 'id_error':
                id_error = True
                return render_to_response('main/main.html',
                            {'id_error':id_error},
                            RC(request))
            elif d['Error'] == 'no_exists':
                no_exists = True
                return render_to_response('main/main.html',
                    {'no_exists':no_exists},
                    RC(request))

            elif d['Error'] == 'code_error':
                code_error = True
                return render_to_response('main/main.html',
                    {'code_error':code_error},
                    RC(request))
            else:
                url = request.POST['urlProject'] # urlProject es el nombre de la url que metes para analizar
                dic = {'url': url}
                d.update(dic)

                return render_to_response("upload/dashboard.html", d, context_instance=RequestContext(request))
                         
    else:
        return HttpResponseRedirect('/')


def handler_upload(fileSaved, counter):
    """ Necessary to uploadUnregistered"""
    # If file exists,it will save it with new name: name(x)
    # Primera vez que entra en handler_uppload
    # ---> fileSaved = /home/sara/drPencilcode-master/uploads/15.json
    # ---> counter = 0
    
    if os.path.exists(fileSaved):
        counter = counter + 1
        if counter == 1:
        	fileSaved = fileSaved.split(".")[0] + "(1).json" 
        else:
            fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").json"

        file_name = handler_upload(fileSaved, counter)
        return file_name
    else:
        file_name = fileSaved
        return file_name


# _______________________URL Analysis Project_________________________________#


def urlUnregistered(request):
    """Process Request of form URL"""
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            d = {}
            url = form.cleaned_data['urlProject']
            idProject = processStringUrl(url) #http://sarabc.pencilcode.net/load/first
            if idProject == "error":
                d = {'Error': 'id_error'}
                return d
            else:
                try:
                    (pathProject, file) = sendRequestgetJSON(idProject)
                except: #WHEN YOUR PROJECT DOESN'T EXIST
                    d = {'Error': 'no_exists'}
                    return d
                try:
                    # pathProject -> /home/sara/drPencilcode-master/uploads/47.json
                    # request -> <WSGIRequest: POST '/selector'>
                    d = analyzeProject(request, pathProject, file)
                    if d == "error":
                        d = {'Error': 'code_error'}
                        return d
                except IndentationError: 
                    #There is an error with coffee-mastery
                    #We save the project in folder called error_analyzing
                    print "Something went wrong"
                    file.method = 'url/error'
                    file.save()
                    oldPathProject = pathProject
                    newPathProject = pathProject.split("/uploads/")[0] + \
                                     "/error_analyzing/" + \
                                     pathProject.split("/uploads/")[1]
                    shutil.copy(oldPathProject, newPathProject)
                    d = {'Error': 'analyzing'}
                    return d
                # Redirect to dashboard for unregistered user
                d['Error'] = 'None'
                return d
        else:
            d = {'Error': 'MultiValueDict'}
            return  d
    else:
        return HttpResponseRedirect('/')


def processStringUrl(url):
    """Process String of URL from Form

    We allow URLs fof the type:
    http://login.pencilcode.net/edit/project

    Responds the JSON URL
    or "error" else
    """

    idProject = "error"
    counter = 0
    name = ''

    try:
        lista = url.split('/')
        try:
            protocol = lista[0]
            blank = lista[1]
            server = lista[2]
        except IndexError:
            return idProject

        for i in lista:
            if counter > 3: 
                if counter == 4:
                    name = name + lista[counter]
                else:
                    name = name + '/' + lista[counter]              
            counter = counter + 1

    except ValueError:
        idProject = 'error';
        return idProject

    if protocol == "https:":
        protocol = "http:"

    if protocol != "http:": 
        return idProject

    login, pencilcode, net = server.split('.')
    if pencilcode != "pencilcode" or net != "net":
        return idProject
    else:
        if name == '':
            return idProject


    idProject = protocol + '/' + blank + '/' + server + '/' + "load" + '/' + name

    return idProject

def sendRequestgetJSON(idProject):
    """First request to getJSON"""
    fileURL = idProject + ".json" #http://sarabc.pencilcode.net/load/first.json

    # Create DB of files
    now = datetime.now()
    fileName = File (filename = fileURL, method = "url", time = now,
                     move = "", art = "", text = "", sound = "",
                     control = "", operators = "")

    # Guardamos en la base de datos.
    fileName.save()


    dir_json = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    fileSaved = dir_json + str(fileName.id) + ".json" #fileName.id registro en el que se guarda de base de datos
    #fileName.id -> models añaden el campo id automaticamente.

    print "FILE_SAVED ", fileSaved

    # /home/sara/drPencilcode/uploads/15.json

    # Log
    pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    logFile = open (pathLog + "logFile.txt", "a")
    logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
    str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
    "Time: " + str(fileName.time) + "\n")

    # Save file in server
    counter = 0
    file_name = handler_upload(fileSaved, counter)  # /home/sara/drPencilcode-master/uploads/15.json
    outputFile = open(file_name, 'wb')

    jsonFile = urllib2.urlopen(idProject) # http://sarabc.pencilcode.net/load/first
    # abre la url(urlopen) y lee los datos de esa url(urllib2).
    outputFile.write(jsonFile.read())
    outputFile.close() #lo escribe todo en un .json.

    jsonerror = json.loads(open(file_name).read())
        
    for key in jsonerror:
        if key == "error":
            raise

    return (file_name, fileName)

# ________________________ LEARN MORE __________________________________#

def learn(request, page):
    #Unicode to string(page)
    page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')

    page = "learn/" + page + ".html"

    if request.user.is_authenticated():

        return render_to_response(page,
                                RC(request))
    else:

        return render_to_response(page,
                                RC(request))


# ________________________ DASHBOARD ____________________________#

def createDashboards():
    """Get users and create dashboards"""
    allUsers = User.objects.all()
    print "allUsers ---> ", allUsers

    for user in allUsers:
        try:
            newdash = Dashboard.objects.get(user=user)
            print newdash
        except:
            fupdate = datetime.now()
            newDash = Dashboard(user=user.username, frelease=fupdate)
            newDash.save()
            print newDash


# _______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(request, file_name, filename): #ESTA FUNCION DEVUELVE UN DICCIONARIO
    dictionary = {}
    # request -> <WSGIRequest: POST '/selector'>
    # file_name -> /home/sara/drPencilcode-master/uploads/47.json

    if os.path.exists(file_name):
        list_file = file_name.split('(')

        # list_file -> ['/home/sara/drPencilcodeGAMMA/uploads/47.json']

        if len(list_file) > 1:
            file_name = list_file[0] + '\(' + list_file[1]
            list_file = file_name.split(')')
            file_name = list_file[0] + '\)' + list_file[1]

        # file_name -> /home/sara/drPencilcodeGAMMA/uploads/47.json

        # Request to coffee-mastery
        with open(file_name) as data_file:
            data = json.load(data_file)  #todo lo que hay escrito en 47.json (diccionario) lo guarda en data

        print "DATA -> ",data
        with open(file_name.replace(".json", ".coffee"), "w") as coffee_file:
            coffee_file.write(data["data"]) # copia el valor de la llave data del diccionario data en 47.coffee

        metricMastery = "python /home/sara/coffee-masteryBETA/coffee-mastery.py " + file_name.replace(".json", ".coffee")

        try:
            resultMastery = os.popen(metricMastery).read() 
            # resultmastery datos json(sin comentarios, comas, etc) mas los niveles basic, developing.. de cada categoria.
        except:
            print "error en mastery"
            raise

        metricLint = "coffeelint --reporter raw " + file_name.replace(".json", ".coffee")
        # devuelve diccionario con errores del proyecto .coffee (si hay o no hay)

        try:
            resultLint = os.popen(metricLint).read()
            print "RESULT LINT -----> ", resultLint
        except:
            print "error en lint"

        # resultLint= ast.literal_eval(resultLint)

        resultLint = resultLint.split(str(file_name.replace(".json", ".coffee")))[1]

        try:
            if len(resultLint) > 10:
                print "El programa no está bien escrito"
                raise
        except:
            dictionary = "error"
            return dictionary

        print "\n resultMastery --> ",resultMastery

        # Create a dictionary with necessary information
        dictionary.update(procMastery(request, resultMastery, filename))

        # print dictionary
        return dictionary
    else:
        return HttpResponseRedirect('/')


# __________________________ PROCESSORS _____________________________#

def procMastery(request, lines, fileName):
    """Mastery"""
    d = {}
    lint = {}
    diccduplic = {}
    diccblocks = {}
    diccpuntos = {}
    mssg = ''
    diccpoints = {}
    MaxBonus = [1, 2, 3, 4]
    current_points = 0
    lint_data = json.dumps(lines)
    categories = ['Move', 'Art', 'Text', 'Sound', 'Control', 'Operators', 'Duplicados']

    aux = lint_data.split('Move: ')[1]
    dicc = {}
    dicclevels = {}
    n = 1

    # Creo un diccionario con el nombre de las categorias y los bloques que se están usando 
    # en cada una de ellas.

    for i in categories:
        if i != 'Duplicados' and i != 'Levels':
            a = categories[n] + ": "        
            dicc[i] = aux.split(a)[0].split('\\n')[0]
            aux = aux.split(a)[1]
            n = n + 1
        else:
            diccduplic = aux.split("\\n")[0]
            dicclevels = aux.split("\\n")[1].split('Levels: ')[1]
         
    dicclevels = ast.literal_eval(dicclevels)

    for elem in dicc:
        value = dicc[elem]
        listblocks = []
        if value == 'false':
            diccblocks[elem] = 'false'
        else:
            value = ast.literal_eval(value)
            dicc[elem] = value
            lista = value.values()
            for i in lista:
                if i != 'false':
                    listblocks = listblocks + i
                    diccblocks[elem] = listblocks

    
    for elem in dicclevels:
        current_points = current_points + dicclevels[elem]

    # BONUS
    score = calculoBonus(categories, diccblocks, dicc, current_points, diccduplic, MaxBonus)

    mssg = wtimprove(dicclevels)

    #Save in DB

    fileName.move = dicc["Move"]
    fileName.art = dicc["Art"]
    fileName.text = dicc["Text"]
    fileName.sound = dicc["Sound"]
    fileName.control = dicc["Control"]
    fileName.operators = dicc["Operators"]
    fileName.bonus = diccblocks["Bonus"]
    fileName.score = score
    fileName.save()
    
    d["mastery"] = {}
    d["mastery"] = diccblocks
    d["lint"] = dicclevels
    d["mastery"]["points"] = score
    d["mastery"]["emptybonus"] = MaxBonus
    d["mastery"]["message"] = mssg

    print str(d) + "\n"

    return d

#_________________________ Feedback Messages _______________________________#

def wtimprove(dicclevels):

    level0 = []
    level1 = []
    level2 = []
    level3 = []
    lowlevel = 'false'
    basiclevel = 'false'
    intermediatelevel = 'false'
    highlevel = 'false'

    for element in dicclevels:
        value = dicclevels[element]
        if value == 0:
            level0.append(element)
            lowlevel = 'true'


    if lowlevel == 'true':
        if len(level0) == 1:
                string = str('Ohh! You have not used blocks from ' + level0[0] + 
        ' category..\nCheck out the examples and blocks that you can use in this class to raise your level.')
        else:
            categ = ''
            for elem in level0:
                if categ == '':
                    categ = str(elem)
                else:
                    categ = categ + ', ' + elem

            string = str('Ohh! You have not used blocks from ' + categ + 
            ' categories.. \nCheck out the examples and blocks that you can use in these classes to raise your level!')
    elif lowlevel == 'false':
        for element in dicclevels:
            value = dicclevels[element]
            if value == 1:
                level1.append(element)
                basiclevel = 'true'


    if basiclevel == 'true' and lowlevel == 'false':
        if len(level1) == 1:
                string = str("You're good! but you can still raise your level working on " + level1[0] + 
                " category.\nCheck out the examples for more help!")
        else:
            categ = ''
            for elem in level1:
                if categ == '':
                    categ = str(elem)
                else:
                    categ = categ + ', ' + elem
            string = str("You're good! but you can still raise your level working on " + categ + 
            " categories.\nCheck out the examples for more help!")

    elif basiclevel == 'false':
        for element in dicclevels:
            value = dicclevels[element]
            if value == 2:
                level2.append(element)
                intermediatelevel = 'true'

    if intermediatelevel == 'true' and lowlevel == 'false' and basiclevel == 'false':
        if len(level2) == 1:
                string = str("You're almost a master! Take a look on " + level2[0] + 
                " category. \nCheck the examples to level up. You will make it!")
        else:
            categ = ''
            for elem in level2:
                if categ == '':
                    categ = str(elem)
                else:
                    categ = categ + ', ' + elem
            string = str("You're almost a master! Take a look on " + categ + 
            " categories.\nCheck the examples to level up. You will make it!")

    elif intermediatelevel == 'false':
        if lowlevel == 'false' and basiclevel == 'false':
            highlevel = 'true'

    return string

#_________________________ Calculo de Bonus _______________________________#

def calculoBonus(categories, diccblocks, dicc, current_points, diccduplic, MaxBonus):
    listbonus = []
    allcategor = 0
    bonuscomplex = []
    bonusdiversi = []
    for element in categories:
        if element != 'Duplicados' and diccblocks[element] != 'false':
            allcategor = allcategor + 1
            
    if allcategor == 6:
        listbonus.append("You have used blocks of all categories!")
        current_points = current_points + 1 
        MaxBonus.pop()  

    categ = []
    alLevels = 'false'
    complexity = 'false'
    for elem in dicc:
        cont = 0
        value = dicc[elem]
        if value != 'false': # value = {'1': ['write'], '3': 'false', '2': 'false'}
            alLevels = 0
            for level in value:
               blocks = value[level]
               if blocks != 'false':
                    cont = cont + 1
        if cont == 3:        
            alLevels = 'true'
            bonusdiversi.append(elem)
            num1 = len(value['1'])
            num2 = len(value['2'])
            num3 = len(value['3'])
            if num1 < num3 and num2 < num3:
                complexity = 'true'
                bonuscomplex.append(elem)

    if alLevels == 'true':
        # Bonus por diversidad
        if len(bonusdiversi) == 1:
            string = str('You have used blocks of three different levels in ' + bonusdiversi[0] + ' category!')
        else:
            categ = ''
            for elem in bonusdiversi:
                if categ == '':
                    categ = str(elem)
                else:
                    categ = categ + ', ' + elem
            string = str('You have used blocks of three different levels in ' + categ + ' categories!')
      	
        listbonus.append(string)
        current_points = current_points + 1
        MaxBonus.pop()

        # Bonus por complejidad
        if complexity == 'true':
            listbonus.append(str("Bonus for complexity, you have used more blocks of level 3 than 1 and 2."))
            current_points = current_points + 1
            MaxBonus.pop()
    
    diccduplic = ast.literal_eval(diccduplic)
      
    if diccduplic != dict():
        listbonus.append("You have use the same block more than once!")
        current_points = current_points + 1
        MaxBonus.pop()

    diccblocks["Bonus"] = listbonus
    return current_points


#_________________________ Download Certificate _______________________________#

def download_certificate(request):
    if request.method == "POST":
        filename = str(request.POST['url'])
        level = str(request.POST['score'])
        pyploma.generate(filename,level)
        path_to_file = os.path.dirname(os.path.dirname(__file__)) + "/app/output.pdf"
        pdf_data = open(path_to_file, 'r')
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
        return response

def csrf_failure(request, reason=""):
    ctx = {'message': 'CSRF no furula'}
    return render_to_response('csrf/fallo.html', ctx)


# _________________________ SURVEY FOR FEEDBACK _______________________________ #


def getFeedback(request):
    form = SurveyForm(request.POST or None)
    form_filled = False
    data_exist = False

    if request.method == 'POST':
        if form.is_valid():
            form_diccionario = form.cleaned_data
            form_filled = True
            #para conseguir la "informacion limpia" sin los corchetes y demas
            save_name = form_diccionario.get("name")
            save_user = form_diccionario.get("user")
            save_date = datetime.now()
            save_question1a = form_diccionario.get("question1a")
            save_question1b = form_diccionario.get("question1b")
            save_question2a = form_diccionario.get("question2a")
            save_question2b = form_diccionario.get("question2b")
            save_question2c = form_diccionario.get("question2c")
            save_question2d = form_diccionario.get("question2d")
            save_question3a = form_diccionario.get("question3a")
            save_question3b = form_diccionario.get("question3b")
            save_question3c = form_diccionario.get("question3c")
            save_question4 = form_diccionario.get("question4")
            save_question5 = form_diccionario.get("question5")
            save_question6 = form_diccionario.get("question6")
          
            if form_filled:
                contador = Survey.objects.filter(name=save_name,user=save_user).count()
                if contador > 1:
                    data_exist = True
                else:
                    #Guardar en la base de datos
                    Encuesta = Survey()
                    Encuesta.name = save_name
                    Encuesta.user = save_user
                    Encuesta.date = save_date
                    Encuesta.question1a = save_question1a
                    Encuesta.question1b = save_question1b
                    Encuesta.question2a = save_question2a
                    Encuesta.question2b = save_question2b
                    Encuesta.question2c = save_question2c
                    Encuesta.question2d = save_question2d
                    Encuesta.question3a = save_question3a
                    Encuesta.question3b = save_question3b
                    Encuesta.question3c = save_question3c
                    Encuesta.question4 = save_question4
                    Encuesta.question5 = save_question5
                    Encuesta.question6 = save_question6
                    Encuesta.save()


    print form_filled
    context = {
    "form":form,
    "form_filled": form_filled,
    "data_exist": data_exist
	}
        
    return render(request, 'feedback/Helpus.html', context)




