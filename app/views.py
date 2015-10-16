#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.core.context_processors import csrf
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.template import Context, loader
from django.contrib.auth import logout, login, authenticate
from django.utils.translation import ugettext as _
from app.models import Project, Dashboard, Attribute
from app.models import Dead, Sprite, Mastery, Duplicate, File
from app.forms import UploadFileForm, UserForm, NewUserForm, UrlForm
from django.contrib.auth.models import User
from datetime import datetime, date
import os
import ast
import json
import sys
import unicodedata
import urllib2
import shutil
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
            else:
                print "DICCIONARIO ---> ", d
                url = request.POST['urlProject']
                dic = {'url': url}
                d.update(dic)
                
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
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
        	fileSaved = fileSaved.split(".")[0] + "(1).json" # sb2? --> Dr.Scratch.
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
        print form
        if form.is_valid():
            url = form.cleaned_data['urlProject']
            print url
            idProject = processStringUrl(url) #http://sarabc.pencilcode.net/load/first
            print "Project to analyze:", idProject
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
                    d = analyzeProject(request, pathProject)
                except IndentationError: # FIXME
                    #There is an error with kutz or hairball
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

    #http://sarabc.pencilcode.net/load/first
    # idProject = ''
    idProject = "error"
    
    try:
        protocol, blank, server, edit, name = url.split('/')
    except ValueError:
        return idProject

    print "protocol ---> ", protocol
    print "server ---> ", server #sarabc.pencilcode.net
    print "name ---> ", name
    
    if protocol != "http:": #se puede hacer como en drScratch? auxString == ''?
        return idProject

    login, pencilcode, net = server.split('.')
    if pencilcode != "pencilcode" or net != "net":
        return idProject
    else:
        if name == '':
            return idProject

    idProject = protocol + '/' + blank + '/' + server + '/' + "load" + '/' + name

    print "idProject ---> ", idProject
    return idProject

def sendRequestgetJSON(idProject):
    """First request to getJSON"""
    fileURL = idProject + ".json" #http://sarabc.pencilcode.net/load/first.json
    print fileURL

    # Create DB of files
    now = datetime.now()
    fileName = File (filename = fileURL, method = "url", time = now,
                     score = 0, abstraction = 0, parallelism = 0,
                     logic = 0, synchronization = 0, flowControl = 0,
                     userInteractivity = 0, dataRepresentation = 0)


    # Guardamos en la base de datos.
    fileName.save() 
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    fileSaved = dir_zips + str(fileName.id) + ".json" 
    #fileName.id -> models añaden el campo id automaticamente.

    # /home/sara/drPencilcode-master/uploads/15.json    

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
   # print "Retrieving: ", idProject
    jsonFile = urllib2.urlopen(idProject) # http://sarabc.pencilcode.net/load/first 
    # abre la url(urlopen) y lee los datos de esa url(urllib2).
    outputFile.write(jsonFile.read()) 
    outputFile.close() #lo escribe todo en un .json.
    return (file_name, fileName)

# ________________________ LEARN MORE __________________________________#

#def learn(request):
#    if request.user.is_authenticated():
#        return render_to_response("learn/learn-unregistered.html",
#                                RC(request))
#    else:
#        return render_to_response("learn/learn-unregistered.html",
#                                RC(request))

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

def learnUnregistered(request):
       
    return render_to_response("learn/learn-unregistered.html",)


# ________________________ TO REGISTERED USER __________________________#

def loginUser(request):
    """Log in app to user"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/myDashboard')
            else:
                flag = True
                return render_to_response("main/main.html",
                                            {'flag': flag},
                                            context_instance=RC(request))

    else:
        return HttpResponseRedirect("/")


def logoutUser(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

def createUser(request):
    """Method for to sign up in the platform"""
    logout(request)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            nickName = form.cleaned_data['nickname']
            emailUser = form.cleaned_data['emailUser']
            passUser = form.cleaned_data['passUser']
            user = User.objects.create_user(nickName, emailUser, passUser)
            return render_to_response("profile.html", {'user': user}, context_instance=RC(request))

# ________________________ PROFILE ____________________________#


def updateProfile(request):
    """Update the pass, email and avatar"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            newPass = form.cleaned_data['newPass']
            newEmail = form.cleaned_data['newEmail']
            choiceField = forms.ChoiceField(widget=forms.RadioSelect())
            return HttpResponseRedirect('/mydashboard')
        else:
            return HttpResponseRedirect('/')


def changePassword(request, new_password):
    """Change the password of user"""
    user = User.objects.get(username=current_user)
    user.set_password(new_password)
    user.save()

# ________________________ DASHBOARD ____________________________#

def createDashboards():
    """Get users and create dashboards"""
    allUsers = User.objects.all()
    print "allUsers ---> ", allUsers

    for user in allUsers:
        print user
        try:
            newdash = Dashboard.objects.get(user=user)
            print newdash
        except:
            fupdate = datetime.now()
            newDash = Dashboard(user=user.username, frelease=fupdate)
            newDash.save()
            print newDash

def myDashboard(request):
    """Dashboard page"""
    if request.user.is_authenticated():
        user = request.user.username
        # The main page of user
        # To obtain the dashboard associated to user
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        beginner = mydashboard.project_set.filter(level="beginner")
        developing = mydashboard.project_set.filter(level="developing")
        advanced = mydashboard.project_set.filter(level="advanced")
        return render_to_response("myDashboard/content-dashboard.html",
                                    {'user': user,
                                    'beginner': beginner,
                                    'developing': developing,
                                    'advanced': advanced,
                                    'projects': projects},
                                    context_instance=RC(request))
    else:
        user = None
        return HttpResponseRedirect("/")

def myProjects(request):
    """Show all projects of dashboard"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myProjects/content-projects.html",
                                {'projects': projects},
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


def myRoles(request):
    """Show the roles in Doctor Pencilcode"""
    if request.user.is_authenticated():
        user = request.user.username
        return render_to_response("myRoles/content-roles.html",
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


def myHistoric(request):
    """Show the progress in the application"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myHistoric/content-historic.html",
                                    {'projects': projects},
                                    context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")

# _______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(request, file_name):
    dictionary = {}
    # request -> <WSGIRequest: POST '/selector'>
    # file_name -> /home/sara/drPencilcode-master/uploads/47.json

    if os.path.exists(file_name):
        list_file = file_name.split('(')
        if len(list_file) > 1:
            file_name = list_file[0] + '\(' + list_file[1]
            list_file = file_name.split(')')
            file_name = list_file[0] + '\)' + list_file[1]
        print "list_file ---> !", list_file
        print "file_name -> ", file_name #/home/sara/drPencilcode-master/uploads/47.json
        # Request to coffeelint
        with open(file_name) as data_file:    
            data = json.load(data_file)  #todo lo que hay escrito en 47.json (diccionario) lo guarda en data
        
        print "DATA -> ",data
        with open(file_name.replace(".json", ".coffee"), "w") as coffee_file:    
            coffee_file.write(data["data"]) # copia el valor de la llave data del diccionario data en 47.coffee

        metricMastery = "python /home/sara/coffee-mastery-master/coffee-mastery.py " + file_name.replace(".json", ".coffee")
        print "Running", metricMastery
        try:
            resultMastery = os.popen(metricMastery).read()
        except:
            print "error en mastery"

        
        metricLint = "coffeelint --reporter raw " + file_name.replace(".json", ".coffee") 
        # devuelve diccionario con errores del proyecto .coffee (si hay o no hay)

        try:
            resultLint = os.popen(metricLint).read()
        except:
            print "error en lint"

        print "\n resultMastery --> ",resultMastery
        print "resultLint --> ", resultLint

        # Create a dictionary with necessary information
        dictionary.update(procMastery(request, resultMastery))
        dictionary.update(procLint(request, resultLint))
        
        print dictionary
        return dictionary
    else:
        return HttpResponseRedirect('/')


# __________________________ JSON Analyzer _____________________________#



# __________________________ PROCESSORS _____________________________#

def procMastery(request, lines):
    """Mastery"""
    #print "In procMastery"
    dic = {}
    d = {}

    lint_data = json.dumps(lines)
    # ast.literal_eval() # pasa a python dicc

    print "\n LINT_DATA --> ", lint_data

    prueba = lint_data.split("]")[-1]
    p2 = prueba.split("\n")
    p3 = p2[0].split('\\n')

    print "\n Prueba --> ", prueba
    print "prueba 2 ---> ", p2
    print "prueba3 -> ", p3
    print "\n"
   
    # capabilities scores
    abstraction = int(p3[1].split(': ')[1])
    parallelism = int(p3[2].split(': ')[1])
    logic = int(p3[3].split(': ')[1])
    synchronization = int(p3[4].split(': ')[1])
    flow = int(p3[5].split(': ')[1])
    userInteractivity = int(p3[6].split(': ')[1])
    dataRepresentation = int(p3[7].split(': ')[1])

    diccionario = {"Abstraction": abstraction, "Parallelism": parallelism}
    d.update(diccionario)
    diccionario = {'Logic': logic, 'Synchronization': synchronization, 'Flow': flow}
    d.update(diccionario)
    diccionario = {'Interactivity': userInteractivity, 'Representation': dataRepresentation}
    d.update(diccionario)
    print d

    score = 0
    for key in d:
        score = score + d[key]

    dic["mastery"] = {}
    dic["mastery"] = d
    dic["mastery"]["points"] = score
    dic["mastery"]["maxi"] = 21
    return dic


def procLint(request, lines):
    """Lint"""
   # print "In procLint"
    dic = {}
    lint_data = json.dumps(lines)
    
    dic["lint"] = {}
    dic["lint"]["points"] = 3
    dic["lint"]["maxi"] = 25
    return dic


# _____________________ CREATE STATS OF ANALYSIS PERFORMED ___________#

def createStats(file_name, dictionary):
    flag = True

    return flag


# _____ ID/BUILDERS ____________#

def idProject(request, idProject):
    """Resource uniquemastery of project"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    dmastery = {}
    project = Project.objects.get(id=idProject)
    item = Mastery.objects.get(myproject=project)
    dmastery = buildMastery(item)
    TotalPoints = dmastery["TotalPoints"]
    dsprite = Sprite.objects.filter(myproject=project)
    ddead = Dead.objects.filter(myproject=project)
    dattribute = Attribute.objects.filter(myproject=project)
    listAttribute = buildAttribute(dattribute)
    numduplicate = Duplicate.objects.filter(myproject=project)[0].numduplicates
    return render_to_response("project.html", {'project': project,
                                               'dmastery': dmastery,
                                               'lattribute': listAttribute,
                                               'numduplicate': numduplicate,
                                               'dsprite': dsprite,
                                               'Total points': TotalPoints,
                                               'ddead': ddead},
                                               context_instance=RequestContext(request))


def buildMastery(item):
    """Generate the dictionary with mastery"""
    dmastery = {}
    dmastery["Total points"] = item.TotalPoints
    dmastery["Abstraction"] = item.abstraction
    dmastery["Parallelism"] = item.paralel
    dmastery["Logic"] = item.logic
    dmastery["Synchronization"] = item.synchronization
    dmastery["Flow Control"] = item.flowcontrol
    return dmastery

def buildAttribute(qattribute):
    """Generate dictionary with attribute"""
    # Build the dictionary
    dic = {}
    for item in qattribute:
        dic[item.character] = {"orientation": item.orientation,
                               "position": item.position,
                               "costume": item.costume,
                               "visibility": item.visibility,
                               "size": item.size}
    listInfo = writeErrorAttribute(dic)
    return listInfo

# _______BUILDERS'S HELPERS ________#


def writeErrorAttribute(dic):
    """Write in a list the form correct of attribute plugin"""
    lErrors = []
    for key in dic.keys():
        text = ''
        dx = dic[key]
        if key != 'stage':
            if dx["orientation"] == 1:
                text = 'orientation,'
            if dx["position"] == 1:
                text += ' position, '
            if dx["visibility"] == 1:
                text += ' visibility,'
            if dx["costume"] == 1:
                text += 'costume,'
            if dx["size"] == 1:
                text += ' size'
            if text != '':
                text = key + ': ' + text + ' modified but not initialized correctly'
                lErrors.append(text)
            text = None
        else:
            if dx["background"] == 1:
                text = key + ' background modified but not initialized correctly'
                lErrors.append(text)
    return lErrors

# _________________________  _______________________________ #


def uncompress_zip(zip_file):
    unziped = ZipFile(zip_file, 'r')
    for file_path in unziped.namelist():
        if file_path == 'project.json':
            file_content = unziped.read(file_path)
    show_file(file_content)
