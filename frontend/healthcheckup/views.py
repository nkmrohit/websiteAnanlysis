from django import http
from django.shortcuts import render
from django.http import HttpResponse
import requests
import sys
from bs4 import BeautifulSoup
import re

from requests.api import get
import urllib.request
from time import time
import urllib.request, json
import whois
import xml.etree.cElementTree as ET

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import pdfkit
import pdfcrowd
import sys
import pdfkit
from io import BytesIO
from urllib.request import urlopen

# Create your views here.
def index(self):
    #DataDictionary = {}
    #return render(self,'healthcheckup/test.html',DataDictionary)

    #exit('dsa')            
    alexa_base_url = 'https://alexa.com/siteinfo/'
    site_name = 'https://www.icicibank.com/'
    url_for_rank = alexa_base_url + site_name
    
    #options = FirefoxOptions()
    #options.add_argument("--headless")
    #driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
    #driver.get(url_for_rank)
    #html_doc = driver.page_source
    #soup = BeautifulSoup(html_doc, 'html.parser')
    #driver.close()
    #driver = webdriver.Firefox(executable_path=r'D:\itnsmain\geckodriver.exe')
    page = urlopen(url_for_rank)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    #return HttpResponse('testing ');
    #page = requests.get(url_for_rank)
    #soup = BeautifulSoup(page.content, 'html.parser')
    
    KEY_WORD_OPPORTUNITIES = soup.find_all('div', id='card_mini_kwopps')
    TOP_KEYWORDS_BY_TRAFFIC = soup.find_all('div', id='card_mini_topkw')

    ALEXA_RANK_90_DAY_TREND = soup.find_all('div', id='card_mini_trafficMetrics')
    Traffic_Sources = soup.find_all('div', id='card_trafficsources')

    Referral_Sites = soup.find_all('div', id='card_referralsites')
    Top_Keywords = soup.find_all('div', id='card_topkeywords')
    
    Alexa_Rank = soup.find_all('div', id='card_rank')
    Audience_Geography = soup.find_all('div', id='card_geography')

    Site_Metrics = soup.find_all('div', id='card_metrics')

    #-----------------------Same as Landing Page------------------------------#
    baseurl = site_name
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, 'html.parser')

    robotTxt = ''
     
    #------ Check Robots.txt file exist-----#
    try:
        r = requests.get(baseurl+'robots.txt')
        if r.content:
            robotTxt= "<span style=color:green>Robots.txt file is exist <br> <a target='_blank' href='"+baseurl+'robots.txt'+"'>"+baseurl+'robots.txt'+" </a></span>"
        else:
            robotTxt= "<span style=color:red>Robots.txt file is not exist</span>"
    except requests.exceptions.RequestException as e:
        robotTxt= "<span style=color:red>Some thing going to wrong</span>"
    
    
    # --------------Check Sitemap files ------------#
    
    try:
        siteMap = ['wp-sitemap.xml','sitemap.xml']
        for siteMapCheck in siteMap:
            response = requests.get(baseurl+siteMapCheck)
            if response:
                sitemapXML= "<span style=color:green>Sitemap.xml file is exist</span>"
                break
            else:
                sitemapXML= "<span style=color:red>Sitemap.xml file is not exist</span>"    
    except:
         sitemapXML= "<span style=color:red>Some thing going to wrong</span>"
    # - Google Analytic code check
    try:
        analyticCode = soup(text=re.compile('GoogleAnalyticsObject'))
        if len(analyticCode)!=0:
            analyticCodeExist = '<span style=color:green>Google Analytics Code is Exist</span>';
        else:
            analyticCodeExist = '<span style=color:red>Google Analytics Code is not Exist</span>';
    except:
        analyticCodeExist = '<span style=color:red>Some Thing Going To Wrong</span>';   
    # - Navigation is responsive
    menuResponsive = '';
    try:
        
        # get ranks text in a list
        navResponsiveClasses = ['navbar','navbar-menu','navbar-item','navbar-nav','navbar-toggler','navbar-collapse','navbar','navbar-light','navbar-expand-lg',
        'navbar-light','bg-light','data-toggle','data-target','fusion-menu','fusion-mobile-nav-holder','mobile-nav','menu-item',
        'menu-side','menu-wrap','menu']
        responseData = soup.find_all('div', class_=navResponsiveClasses)
        #print(responseData)
        #imgResponsive = soup.find(class_="img-responsive")
        if len(responseData)!=0:
            menuResponsive = '<span style=color:green>Navigation is responsive</span>';
        else:
            menuResponsive = '<span style=color:red>Navigation is not resposive</span>';
    except:
        menuResponsive = '<span style=color:red>Some Thing Going To Wrong</span>';


    # - web Page is responsive
    pageResponsive = '';
    try:
        # get ranks text in a list
        pageResponsiveClasses = ['column is-6','column','media-content','col-xs-1','col-xs-2','col-xs-3','col-xs-4','col-xs-5','col-xs-6','col-xs-7',
        'col-xs-18','col-xs-9','col-xs-10','col-xs-11','col-xs-12','col-sm-1','col-sm-2','col-sm-3','col-sm-4',
        'col-sm-5','col-sm-6','col-sm-7','col-sm-8','col-sm-9','col-sm-10','col-sm-11','col-sm-12',
        'row','col','col-md','container-fluid','wrap','fusion-row','footer','section']
        pgResponsive = soup.find_all('div', class_=pageResponsiveClasses)
        #imgResponsive = soup.find(class_="img-responsive")
        if len(pgResponsive)!=0:
            pageResponsive = '<span style=color:green>Web page is responsive</span>';
        else:
            pageResponsive = '<span style=color:red>Web page is not resposive</span>';
    except:
        pageResponsive = '<span style=color:red>Some Thing Going To Wrong</span>';

    

    # - Image is responsive
    imgResponsive = '';
    try:
        # get ranks text in a list
        imageResponsive = soup.find_all('img', class_=['img-fluid', 'img-responsive'])
        #imgResponsive = soup.find(class_="img-responsive")
        if len(imageResponsive)!=0:
            imgResponsive = '<span style=color:green>Image is responsive</span>';
        else:
            imgResponsive = '<span style=color:red>Image is not resposive</span>';
    except:
        imgResponsive = '<span style=color:red>Some Thing Going To Wrong</span>';

    # - 404 validation

    page404 = '';
    try:
        errorPage = requests.get(baseurl+'/21071988')
        errorsoup = BeautifulSoup(errorPage.content, 'html.parser')
        search404Txt = errorsoup(text=re.compile(baseurl, re.IGNORECASE))
        
        if len(search404Txt)!=0:
            page404 = '<span style=color:green>404 Page is Exist</span>';
        else:
            page404 = '<span style=color:red>404 is not Exist</span>';
    except:
        page404 = '<span style=color:red>Some Thing Going To Wrong</span>';

    # - meta title tag is exist
    metaTtitleTag = '';
    try:
        # get ranks text in a list
        checkMetaTag = soup.find("meta", property="og:title")
        if checkMetaTag:
            metaTtitleTag = '<span style=color:green>Meta title tag is exist</span>';
        else:
            metaTtitleTag = '<span style=color:red>Meta title tag is exist</span>';
    except:
        metaTtitleTag = '<span style=color:red>Some Thing Going To Wrong</span>';
    
    # - meta title tag lenth
    metaTtitleTagLength = '';
    try:
        # get ranks text in a list
        #checkMetaTagLength = soup.find_all('title')
        #checkMetaTagLength = soup.find_all('title')
        checkMetaTagLength = soup.find("meta", property="og:title")
        if checkMetaTagLength:
            cust = str(len(checkMetaTagLength["content"]))
            metaTtitleTagLength = '<span style=color:green>Meta title length is '+cust+' characters</span>'
        else:
            metaTtitleTagLength = '<span style=color:red>Meta title length is 0 characters</span>'
    except:
        metaTtitleTagLength = '<span style=color:red>Some Thing Going To Wrong</span>'
    
    # - Check Meta description tag
    
    # - Merta description data check
    meetaDescriptiontagCheck = ' ';
    try:
        # get ranks text in a list
        # metaDescriptiontag = soup.findAll('meta',attrs={"name": "description"})
        #metaDescriptiontag = soup.find("meta",  property="og:description")
        metaDescriptiontag = soup.find("meta", property="og:description")
        if metaDescriptiontag:
            meetaDescriptiontagCheck = '<span style=color:green>Meta Description Tag is exist</span>';
        else:
            meetaDescriptiontagCheck = '<span style=color:red>Meta Description Tag is not exist</span>';
    except:
        meetaDescriptiontagCheck = '<span style=color:red>Some thing going to wrong</span>';
    
    # Meta description length check
    meetaDescriptiontagLength = '';
    try:
        # get ranks text in a list
        metaDescriptionlen = soup.find("meta",  property="og:description")
        
        if metaDescriptionlen:
            metaDescriptionCount = str(len(metaDescriptionlen["content"]))
            meetaDescriptiontagLength = '<span style=color:green>Meta Description Length is '+metaDescriptionCount+' characters</span>';
        else:
            meetaDescriptiontagLength = '<span style=color:red>Meta Description Length is 0 characters </span>';
    except:
        meetaDescriptiontagLength = '<span style=color:red>Some thing going to wrong</span>';

    # check h1 tag
    checkH1Tag = '';
    try:
        # get ranks text in a list
        h1tag = soup.find_all(["h1"])
        if len(h1tag)!=0:
            checkH1Tag = '<span style=color:green>H1 Heading Tag is exist</span>';
        else:
            checkH1Tag = '<span style=color:red>H1 Heading Tag is not exist</span>';
    except:
        checkH1Tag = '<span style=color:red>Some Thing Going To Wrong</span>';

    canonicalTagExist = '';
    try:
        # get ranks text in a list
        canonicalTagExistCheck = soup.find("link",  rel="canonical")
        canonicalTagExistCheck = str(len(str(canonicalTagExistCheck["href"])))
        #print(canonicalTagExistCheck)
        if len(canonicalTagExistCheck)!=0:
            
            canonicalTagExist = '<span style=color:green>Canonical Tag is exist</span>';
        else:
            canonicalTagExist = '<span style=color:red>Canonical Tag is not exist</span>';
    except:
        canonicalTagExist = '<span style=color:red>Canonical Tag is not exist</span>';

    imageAltAttributes = '';
    try:
        # get ranks text in a list
        altAttCheck = soup.find_all("img",  alt=True)
        if len(altAttCheck)!=0:
            
            imageAltAttributes = '<span style=color:green>Image alt tag is exist</span>';
        else:
            imageAltAttributes = '<span style=color:red>Image alt tag is not exist</span>';
    except:
        imageAltAttributes = '<span style=color:red>Some Thing Going To Wrong</span>';

    try:
        page = requests.get('https://www.whois.com/whois/'+self.GET.get('inputUrl'))
        soup = BeautifulSoup(page.content, 'html.parser')
        divparent = soup.find_all('div', class_=['df-block'])[0]
        whoData = {}
        for test in divparent:
            textData = test.find_all('div',class_=['df-label'])
            for innerwho in textData:
                textDatavalue = test.find_all('div',class_=['df-value'])
                for innerwhovalue in textDatavalue:
                    whoData.update({innerwho.text:innerwhovalue.text})

        domainRegisterDate = '<span style=color:green>Domain Registered Date is '+str(whoData['Registered On:'])+'</span>';
        domainExpireDate = '<span style=color:green>Domain Registered Date is '+str(whoData['Expires On:'])+'</span>';
        emails = '<span style=color:green>Email is '+str(whoData['Updated On:'])+'</span>';
        registrar = '<span style=color:green>Registrar is '+str(whoData['Registrar:'])+'</span>'
        domainAddress = '<span style=color:green>'+str(whoData['Name Servers:'])+'</span>'
    except Exception as e:
        domainAddress = '<span style=color:green>Some Thing Going To Wrong</span>'
        registrar = '<span style=color:green>Some Thing Going To Wrong</span>'
        emails = '<span style=color:green>Some Thing Going To Wrong</span>'
        domainExpireDate = '<span style=color:green>Some Thing Going To Wrong</span>'
        domainRegisterDate = '<span style=color:green>Some Thing Going To Wrong</span>'
    # Moz Scrapping
    moz_base_url = 'https://moz.com/domain-analysis?site='
    mozData = moz_base_url + baseurl
    # Request formatted url for rank(s)
    mozPage = requests.get(mozData)
    mozSoup = BeautifulSoup(mozPage.content, 'html.parser')
    # get ranks text in a list
    block1 = mozSoup.find_all('div', id='card_gaps')
    test = mozSoup.find_all("h5", string="Domain Authority")
    
    # Count Total Page
    
    try:
        reqs = requests.get(baseurl)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        i=0
        websiteLink = []
        for link in soup.find_all('a'):
            if link.get('href'):
                websiteLink.append(link.get('href'))
        
        totalPage = '<span style=color:green>Total Page is '+str(len(websiteLink))+'</span>'
    except Exception as e:
        totalPage = '<span style=color:red>Some thing is going to wrong</span>'
       
    try:
        r = requests.get(baseurl)
        if 'https' in r.url:
            checkHttps = '<span style=color:green>Site is secure</span>'
        else:
            checkHttps = '<span style=color:red>Site is not secure</span>'
    except:
        checkHttps = '<span style=color:red>Some thing is going to wrong</span>'

    # - No Index Checker
    noIndexChecker = '';
    try:
        # get ranks text in a list
        noIndexChecker = soup.findAll('meta',attrs={"name": "robots"})
        #noIndexChecker = soup.find("meta",  property="og:description")
        if len(noIndexChecker)!=0:
            noIndexChecker = '<span style=color:green>NoIndex & Nofollow Tag is exist</span>';
        else:
            noIndexChecker = '<span style=color:red>NoIndex & Nofollow Tag is not exist</span>';
    except:
        noIndexChecker = '<span style=color:red>Some Thing Going To Wrong</span>';

    # ValidationError
    try:
        validator_base_url = 'https://validator.w3.org/nu/?doc='
        validatorWebsite = validator_base_url + baseurl
        # Request formatted url for rank(s)
        siteValidator = requests.get(validatorWebsite)
        soupValidator = BeautifulSoup(siteValidator.content, 'html.parser')
        # get ranks text in a list
        warningIssue = soupValidator.find_all('li', attrs={'class':'info warning'})
        errorIssue = soupValidator.find_all('li', attrs={'class':'error'})
        domainIssue = '<span style=color:green><span style="color:red">'+str(len(errorIssue))+' Error</span> / <span style="color:#f2dede">'+str(len(warningIssue))+' Warning</span>';
    except:
        domainIssue = '<span style=color:red>Some Thing Going To Wrong</span>';

    #wt = webtech.WebTech()
    #results = wt.start_from_url(baseurl, timeout=1)
    #print(results)
    #print(type(results))

    try:
        alexa_base_url = 'https://alexa.com/siteinfo/'
        url_for_rank = alexa_base_url + baseurl
        # Request formatted url for rank(s)
        page = requests.get(url_for_rank)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # get ranks text in a list
        AlexaRank = soup.find_all('p', attrs={'class':'big data'})
        TotalLinkingSite = soup.find_all('span', attrs={'class':'big data'})
        #engagement = soup.find_all('section', attrs={'class':'engagement'})
        easyToRank  = soup.find_all('section', attrs={'class':'table fancymobile'})
        TrafficSource = soup.find_all('div', attrs={'class':'FolderTarget'})
        
        for alexaint in AlexaRank:
            AlexaRank = alexaint.text

        for sitelinking in TotalLinkingSite:
            TotalLinkingSite = sitelinking.text    
    except:
        AlexaRank = '<span style=color:red>Some Thing Going To Wrong</span>';
        TotalLinkingSite = '<span style=color:red>Some Thing Going To Wrong</span>';
    
    try:
        baseurl
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        search_url = f'https://www.google.com/search?q=site%3A{baseurl}&oq=site%3A{baseurl}&aqs=chrome..69i57j69i58.6029j0j1&sourceid=chrome&ie=UTF-8'
        r = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        index = soup.find('div',{'id':'result-stats'}).text
        googlePageIndex = index.split('About ')[1].split(' results')[0]
        googlePageIndex = '<span style=color:green>Google page indexed is '+str(googlePageIndex)+'</span>';

    except:
        googlePageIndex = '<span style=color:red>Some Thing Going To Wrong</span>';

    try:
        baseurl
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        #search_url = f'https://www.google.com/search?q=site%3A{baseurl}&oq=site%3A{baseurl}&aqs=chrome..69i57j69i58.6029j0j1&sourceid=chrome&ie=UTF-8'
        search_url =f'https://webcache.googleusercontent.com/search?q=cache:odsPWEq8J3AJ:https://www.southmag.com/+&cd=1&hl=en&ct=clnk&gl=in'
        r = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        index = soup.find('div',{'id':'bN015htcoyT__google-cache-hdr'}).text
        googleRecentPageIndex = index.split('Learn more')[0].split(' results')[0]
        googleRecentPageIndex = '<span style=color:green>Google page indexed is '+str(googleRecentPageIndex)+'</span>';
        
    except:
        googleRecentPageIndex = '<span style=color:red>Some Thing Going To Wrong</span>';


    DataDictionary={
        'KEY_WORD_OPPORTUNITIES':KEY_WORD_OPPORTUNITIES,
        'TOP_KEYWORDS_BY_TRAFFIC':TOP_KEYWORDS_BY_TRAFFIC,
        'ALEXA_RANK_90_DAY_TREND':ALEXA_RANK_90_DAY_TREND,
        'Traffic_Sources':Traffic_Sources,
        'Referral_Sites':Referral_Sites,
        'Top_Keywords':Top_Keywords,
        'Alexa_Rank':Alexa_Rank,
        'Audience_Geography':Audience_Geography,
        'Site_Metrics':Site_Metrics,
                'googleRecentPageIndex':googleRecentPageIndex,
        'googlePageIndex':googlePageIndex,
        'AlexaRank':AlexaRank.replace('<br>',' '),
        'TotalLinkingSite':TotalLinkingSite,
        'domainIssue':domainIssue,
        'Process_unprocesslink':'Under Development',
        'noIndexChecker':noIndexChecker,
        'checkHttps':checkHttps,
        'totalPage':totalPage,
        'domainAddress':domainAddress,
        'registrar':registrar,
        'emails':emails,
        'domainExpireDate':domainExpireDate,
        'domainRegisterDate':domainRegisterDate,
        'pageLoadTime':'pageLoadTime',
        'imageAltAttributes':imageAltAttributes,
        'canonicalTagExist':canonicalTagExist,
        'checkH1Tag':checkH1Tag,
        'meetaDescriptiontagLength':meetaDescriptiontagLength,
        'meetaDescriptiontagCheck':meetaDescriptiontagCheck,
        'metaTtitleTagLength':metaTtitleTagLength,
        'metaTtitleTag':metaTtitleTag,
        'page404':page404,
        'analyticCodeExist':analyticCodeExist,
        'menuResponsive':menuResponsive,
        'pageResponsive':pageResponsive,
        'imgResponsive':imgResponsive,
        'robotTxt':robotTxt,
        'sitemapXML':sitemapXML,
        'requestedUrl':self.GET.get('inputUrl')
        }
    return render(self,'healthcheckup/index.html',DataDictionary)

def overview(self):
    
    #print(self.GET,get('inputUrl'))
    #return HttpResponse('testing her')
    regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not self.GET.get('inputUrl'):
        return render(self,'healthcheckup/form.html',{'error':'Please enter url','requestedUrl':self.GET.get('inputUrl')})  
    else:
        if re.match(regex, self.GET.get('inputUrl')) is not None:
            pass
        else:
                return render(self,'healthcheckup/form.html',{'error':'Please enter valid url','requestedUrl':self.GET.get('inputUrl')})  
    #return HttpResponse(self.GET.get('inputUrl'))
    baseurl = self.GET.get('inputUrl')
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, 'html.parser')

    
    
    robotTxt = ''
     
    #------ Check Robots.txt file exist-----#
    try:
        r = requests.get(baseurl+'robots.txt')
        if r.content:
            robotTxt= "<span style=color:green>Robots.txt file is exist <br> <a target='_blank' href='"+baseurl+'robots.txt'+"'>"+baseurl+'robots.txt'+" </a></span>"
        else:
            robotTxt= "<span style=color:red>Robots.txt file is not exist</span>"
    except requests.exceptions.RequestException as e:
        robotTxt= "<span style=color:red>Some thing going to wrong</span>"
    
    
    # --------------Check Sitemap files ------------#
    
    try:
        siteMap = ['wp-sitemap.xml','sitemap.xml']
        for siteMapCheck in siteMap:
            response = requests.get(baseurl+siteMapCheck)
            if response:
                sitemapXML= "<span style=color:green>Sitemap.xml file is exist</span>"
                break
            else:
                sitemapXML= "<span style=color:red>Sitemap.xml file is not exist</span>"    
    except:
         sitemapXML= "<span style=color:red>Some thing going to wrong</span>"
    # - Google Analytic code check
    try:
        analyticCode = soup(text=re.compile('GoogleAnalyticsObject'))
        if len(analyticCode)!=0:
            analyticCodeExist = '<span style=color:green>Google Analytics Code is Exist</span>';
        else:
            analyticCodeExist = '<span style=color:red>Google Analytics Code is not Exist</span>';
    except:
        analyticCodeExist = '<span style=color:red>Some Thing Going To Wrong</span>';   
    # - Navigation is responsive
    menuResponsive = '';
    try:
        
        # get ranks text in a list
        navResponsiveClasses = ['navbar','navbar-menu','navbar-item','navbar-nav','navbar-toggler','navbar-collapse','navbar','navbar-light','navbar-expand-lg',
        'navbar-light','bg-light','data-toggle','data-target','fusion-menu','fusion-mobile-nav-holder','mobile-nav','menu-item',
        'menu-side','menu-wrap','menu']
        responseData = soup.find_all('div', class_=navResponsiveClasses)
        #print(responseData)
        #imgResponsive = soup.find(class_="img-responsive")
        if len(responseData)!=0:
            menuResponsive = '<span style=color:green>Navigation is responsive</span>';
        else:
            menuResponsive = '<span style=color:red>Navigation is not resposive</span>';
    except:
        menuResponsive = '<span style=color:red>Some Thing Going To Wrong</span>';


    # - web Page is responsive
    pageResponsive = '';
    try:
        # get ranks text in a list
        pageResponsiveClasses = ['column is-6','column','media-content','col-xs-1','col-xs-2','col-xs-3','col-xs-4','col-xs-5','col-xs-6','col-xs-7',
        'col-xs-18','col-xs-9','col-xs-10','col-xs-11','col-xs-12','col-sm-1','col-sm-2','col-sm-3','col-sm-4',
        'col-sm-5','col-sm-6','col-sm-7','col-sm-8','col-sm-9','col-sm-10','col-sm-11','col-sm-12',
        'row','col','col-md','container-fluid','wrap','fusion-row','footer','section']
        pgResponsive = soup.find_all('div', class_=pageResponsiveClasses)
        #imgResponsive = soup.find(class_="img-responsive")
        if len(pgResponsive)!=0:
            pageResponsive = '<span style=color:green>Web page is responsive</span>';
        else:
            pageResponsive = '<span style=color:red>Web page is not resposive</span>';
    except:
        pageResponsive = '<span style=color:red>Some Thing Going To Wrong</span>';

   

    # - Image is responsive
    imgResponsive = '';
    try:
        # get ranks text in a list
        imageResponsive = soup.find_all('img', class_=['img-fluid', 'img-responsive'])
        #imgResponsive = soup.find(class_="img-responsive")
        if len(imageResponsive)!=0:
            imgResponsive = '<span style=color:green>Image is responsive</span>';
        else:
            imgResponsive = '<span style=color:red>Image is not resposive</span>';
    except:
        imgResponsive = '<span style=color:red>Some Thing Going To Wrong</span>';

    # - 404 validation

    page404 = '';
    try:
        errorPage = requests.get(baseurl+'/21071988')
        errorsoup = BeautifulSoup(errorPage.content, 'html.parser')
        search404Txt = errorsoup(text=re.compile(baseurl, re.IGNORECASE))
        
        if len(search404Txt)!=0:
            page404 = '<span style=color:green>404 Page is Exist</span>';
        else:
            page404 = '<span style=color:red>404 is not Exist</span>';
    except:
        page404 = '<span style=color:red>Some Thing Going To Wrong</span>';

    # - meta title tag is exist
    metaTtitleTag = '';
    try:
        # get ranks text in a list
        checkMetaTag = soup.find("meta", property="og:title")
        if checkMetaTag:
            metaTtitleTag = '<span style=color:green>Meta title tag is exist</span>';
        else:
            metaTtitleTag = '<span style=color:red>Meta title tag is exist</span>';
    except:
        metaTtitleTag = '<span style=color:red>Some Thing Going To Wrong</span>';
    
    # - meta title tag lenth
    metaTtitleTagLength = '';
    try:
        # get ranks text in a list
        #checkMetaTagLength = soup.find_all('title')
        #checkMetaTagLength = soup.find_all('title')
        checkMetaTagLength = soup.find("meta", property="og:title")
        if checkMetaTagLength:
            cust = str(len(checkMetaTagLength["content"]))
            metaTtitleTagLength = '<span style=color:green>Meta title length is '+cust+' characters</span>'
        else:
            metaTtitleTagLength = '<span style=color:red>Meta title length is 0 characters</span>'
    except:
        metaTtitleTagLength = '<span style=color:red>Some Thing Going To Wrong</span>'
    
    # - Check Meta description tag
    
    # - Merta description data check
    meetaDescriptiontagCheck = ' ';
    try:
        # get ranks text in a list
        # metaDescriptiontag = soup.findAll('meta',attrs={"name": "description"})
        #metaDescriptiontag = soup.find("meta",  property="og:description")
        metaDescriptiontag = soup.find("meta", property="og:description")
        if metaDescriptiontag:
            meetaDescriptiontagCheck = '<span style=color:green>Meta Description Tag is exist</span>';
        else:
            meetaDescriptiontagCheck = '<span style=color:red>Meta Description Tag is not exist</span>';
    except:
        meetaDescriptiontagCheck = '<span style=color:red>Some thing going to wrong</span>';
    
    # Meta description length check
    meetaDescriptiontagLength = '';
    try:
        # get ranks text in a list
        metaDescriptionlen = soup.find("meta",  property="og:description")
        
        if metaDescriptionlen:
            metaDescriptionCount = str(len(metaDescriptionlen["content"]))
            meetaDescriptiontagLength = '<span style=color:green>Meta Description Length is '+metaDescriptionCount+' characters</span>';
        else:
            meetaDescriptiontagLength = '<span style=color:red>Meta Description Length is 0 characters </span>';
    except:
        meetaDescriptiontagLength = '<span style=color:red>Some thing going to wrong</span>';

    # check h1 tag
    checkH1Tag = '';
    try:
        # get ranks text in a list
        h1tag = soup.find_all(["h1"])
        if len(h1tag)!=0:
            checkH1Tag = '<span style=color:green>H1 Heading Tag is exist</span>';
        else:
            checkH1Tag = '<span style=color:red>H1 Heading Tag is not exist</span>';
    except:
        checkH1Tag = '<span style=color:red>Some Thing Going To Wrong</span>';

    canonicalTagExist = '';
    try:
        # get ranks text in a list
        canonicalTagExistCheck = soup.find("link",  rel="canonical")
        canonicalTagExistCheck = str(len(str(canonicalTagExistCheck["href"])))
        #print(canonicalTagExistCheck)
        if len(canonicalTagExistCheck)!=0:
            
            canonicalTagExist = '<span style=color:green>Canonical Tag is exist</span>';
        else:
            canonicalTagExist = '<span style=color:red>Canonical Tag is not exist</span>';
    except:
        canonicalTagExist = '<span style=color:red>Canonical Tag is not exist</span>';

    imageAltAttributes = '';
    try:
        # get ranks text in a list
        altAttCheck = soup.find_all("img",  alt=True)
        if len(altAttCheck)!=0:
            
            imageAltAttributes = '<span style=color:green>Image alt tag is exist</span>';
        else:
            imageAltAttributes = '<span style=color:red>Image alt tag is not exist</span>';
    except:
        imageAltAttributes = '<span style=color:red>Some Thing Going To Wrong</span>';

    try:
        page = requests.get('https://www.whois.com/whois/'+self.GET.get('inputUrl'))
        soup = BeautifulSoup(page.content, 'html.parser')
        divparent = soup.find_all('div', class_=['df-block'])[0]
        whoData = {}
        for test in divparent:
            textData = test.find_all('div',class_=['df-label'])
            for innerwho in textData:
                textDatavalue = test.find_all('div',class_=['df-value'])
                for innerwhovalue in textDatavalue:
                    whoData.update({innerwho.text:innerwhovalue.text})

        domainRegisterDate = '<span style=color:green>Domain Registered Date is '+str(whoData['Registered On:'])+'</span>';
        domainExpireDate = '<span style=color:green>Domain Registered Date is '+str(whoData['Expires On:'])+'</span>';
        emails = '<span style=color:green>Email is '+str(whoData['Updated On:'])+'</span>';
        registrar = '<span style=color:green>Registrar is '+str(whoData['Registrar:'])+'</span>'
        domainAddress = '<span style=color:green>'+str(whoData['Name Servers:'])+'</span>'
    except Exception as e:
        domainAddress = '<span style=color:green>Some Thing Going To Wrong</span>'
        registrar = '<span style=color:green>Some Thing Going To Wrong</span>'
        emails = '<span style=color:green>Some Thing Going To Wrong</span>'
        domainExpireDate = '<span style=color:green>Some Thing Going To Wrong</span>'
        domainRegisterDate = '<span style=color:green>Some Thing Going To Wrong</span>'
    # Moz Scrapping
    moz_base_url = 'https://moz.com/domain-analysis?site='
    mozData = moz_base_url + baseurl
    # Request formatted url for rank(s)
    mozPage = requests.get(mozData)
    mozSoup = BeautifulSoup(mozPage.content, 'html.parser')
    # get ranks text in a list
    block1 = mozSoup.find_all('div', id='card_gaps')
    test = mozSoup.find_all("h5", string="Domain Authority")
    
    # Count Total Page
    
    try:
        reqs = requests.get(baseurl)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        i=0
        websiteLink = []
        for link in soup.find_all('a'):
            if link.get('href'):
                websiteLink.append(link.get('href'))
        
        totalPage = '<span style=color:green>Total Page is '+str(len(websiteLink))+'</span>'
    except Exception as e:
        totalPage = '<span style=color:red>Some thing is going to wrong</span>'
       
    try:
        r = requests.get(baseurl)
        if 'https' in r.url:
            checkHttps = '<span style=color:green>Site is secure</span>'
        else:
            checkHttps = '<span style=color:red>Site is not secure</span>'
    except:
        checkHttps = '<span style=color:red>Some thing is going to wrong</span>'

    # - No Index Checker
    noIndexChecker = '';
    try:
        # get ranks text in a list
        noIndexChecker = soup.findAll('meta',attrs={"name": "robots"})
        #noIndexChecker = soup.find("meta",  property="og:description")
        if len(noIndexChecker)!=0:
            noIndexChecker = '<span style=color:green>NoIndex & Nofollow Tag is exist</span>';
        else:
            noIndexChecker = '<span style=color:red>NoIndex & Nofollow Tag is not exist</span>';
    except:
        noIndexChecker = '<span style=color:red>Some Thing Going To Wrong</span>';

    # ValidationError
    try:
        validator_base_url = 'https://validator.w3.org/nu/?doc='
        validatorWebsite = validator_base_url + baseurl
        # Request formatted url for rank(s)
        siteValidator = requests.get(validatorWebsite)
        soupValidator = BeautifulSoup(siteValidator.content, 'html.parser')
        # get ranks text in a list
        warningIssue = soupValidator.find_all('li', attrs={'class':'info warning'})
        errorIssue = soupValidator.find_all('li', attrs={'class':'error'})
        domainIssue = '<span style=color:green><span style="color:red">'+str(len(errorIssue))+' Error</span> / <span style="color:#f2dede">'+str(len(warningIssue))+' Warning</span>';
    except:
        domainIssue = '<span style=color:red>Some Thing Going To Wrong</span>';

    #wt = webtech.WebTech()
    #results = wt.start_from_url(baseurl, timeout=1)
    #print(results)
    #print(type(results))

    try:
        alexa_base_url = 'https://alexa.com/siteinfo/'
        url_for_rank = alexa_base_url + baseurl
        # Request formatted url for rank(s)
        page = requests.get(url_for_rank)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # get ranks text in a list
        AlexaRank = soup.find_all('p', attrs={'class':'big data'})
        TotalLinkingSite = soup.find_all('span', attrs={'class':'big data'})
        #engagement = soup.find_all('section', attrs={'class':'engagement'})
        easyToRank  = soup.find_all('section', attrs={'class':'table fancymobile'})
        TrafficSource = soup.find_all('div', attrs={'class':'FolderTarget'})
        
        for alexaint in AlexaRank:
            AlexaRank = alexaint.text

        for sitelinking in TotalLinkingSite:
            TotalLinkingSite = sitelinking.text    
    except:
        AlexaRank = '<span style=color:red>Some Thing Going To Wrong</span>';
        TotalLinkingSite = '<span style=color:red>Some Thing Going To Wrong</span>';
    
    try:
        baseurl
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        search_url = f'https://www.google.com/search?q=site%3A{baseurl}&oq=site%3A{baseurl}&aqs=chrome..69i57j69i58.6029j0j1&sourceid=chrome&ie=UTF-8'
        r = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        index = soup.find('div',{'id':'result-stats'}).text
        googlePageIndex = index.split('About ')[1].split(' results')[0]
        googlePageIndex = '<span style=color:green>Google page indexed is '+str(googlePageIndex)+'</span>';

    except:
        googlePageIndex = '<span style=color:red>Some Thing Going To Wrong</span>';

    try:
        baseurl
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        #search_url = f'https://www.google.com/search?q=site%3A{baseurl}&oq=site%3A{baseurl}&aqs=chrome..69i57j69i58.6029j0j1&sourceid=chrome&ie=UTF-8'
        search_url =f'https://webcache.googleusercontent.com/search?q=cache:odsPWEq8J3AJ:https://www.southmag.com/+&cd=1&hl=en&ct=clnk&gl=in'
        r = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        index = soup.find('div',{'id':'bN015htcoyT__google-cache-hdr'}).text
        googleRecentPageIndex = index.split('Learn more')[0].split(' results')[0]
        googleRecentPageIndex = '<span style=color:green>Google page indexed is '+str(googleRecentPageIndex)+'</span>';
        
    except:
        googleRecentPageIndex = '<span style=color:red>Some Thing Going To Wrong</span>';

    containers = {
        'googleRecentPageIndex':googleRecentPageIndex,
        'googlePageIndex':googlePageIndex,
        'AlexaRank':AlexaRank.replace('<br>',' '),
        'TotalLinkingSite':TotalLinkingSite,
        'domainIssue':domainIssue,
        'Process_unprocesslink':'Under Development',
        'noIndexChecker':noIndexChecker,
        'checkHttps':checkHttps,
        'totalPage':totalPage,
        'domainAddress':domainAddress,
        'registrar':registrar,
        'emails':emails,
        'domainExpireDate':domainExpireDate,
        'domainRegisterDate':domainRegisterDate,
        'pageLoadTime':'pageLoadTime',
        'imageAltAttributes':imageAltAttributes,
        'canonicalTagExist':canonicalTagExist,
        'checkH1Tag':checkH1Tag,
        'meetaDescriptiontagLength':meetaDescriptiontagLength,
        'meetaDescriptiontagCheck':meetaDescriptiontagCheck,
        'metaTtitleTagLength':metaTtitleTagLength,
        'metaTtitleTag':metaTtitleTag,
        'page404':page404,
        'analyticCodeExist':analyticCodeExist,
        'menuResponsive':menuResponsive,
        'pageResponsive':pageResponsive,
        'imgResponsive':imgResponsive,
        'robotTxt':robotTxt,
        'sitemapXML':sitemapXML,
        'requestedUrl':self.GET.get('inputUrl')
    }

    return render(self,'healthcheckup/overview.html',containers)  

def websitePdfReport(self):
    options = {
        #'page-width':1366,
        #'page-height':2500,
         #'page-size': 'A4',
         #'margin-top': '0.25in',
         #'margin-right': '0.25in',
         #'margin-bottom': '0.25in',
         #'margin-left': '0.25in',
         'encoding': "UTF-8",
         'custom-header' : [
            ('Accept-Encoding', 'gzip')
         ],
         'no-outline': None,
    }

    path_wkthmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf = path_wkthmltopdf)
    pdfkit.from_url("http://127.0.0.1:8000/healthcheckup/", "out.pdf", options=options, configuration=config) 
    return HttpResponse('Successfully Report Exported')
def test(self):
    return HttpResponse('It is for testing perpose')