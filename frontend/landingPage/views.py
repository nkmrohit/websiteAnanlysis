from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from seoanalyzer import analyze
import urllib.request, sys, re
import xmltodict, json
import requests


# Create your views here.
def index(self):
	
	#xml = urllib.request.urlopen('http://data.alexa.com/data?cli=11&url={}'.format("https://www.google.com/")).read()
	#result= xmltodict.parse(xml)
	#print(result,4)
	tempLayout = loader.get_template('landingPage/index.html')
	context = {
        'latest_question_list': 'tdf',
    }
	#return HttpResponse(tempLayout.render(context,self))
	return render(self,'landingPage/index.html',{'dsaf':'dsfa'})