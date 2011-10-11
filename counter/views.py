
from models import Input,EventAddress,Ratio,ParentEvent,StatName,Stat, UserStat

from django.shortcuts import render_to_response
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.auth.decorators import login_required
from django import forms
from page_maker import NamePaginator
from google.appengine.api import urlfetch
from django.http import *
from django.conf import settings
from xml.dom import minidom

from google.appengine.api import users
from google.appengine.ext.db import djangoforms

import base64, urllib, urllib2, re, oauth, httplib, simplejson, datetime, time, google.appengine.ext.db,google.appengine.ext.webapp

## does the twitter stuff.
import tweepy


###Forms

class InputForm(djangoforms.ModelForm):
	class Meta:
		model = Input

class RatioForm(djangoforms.ModelForm):
	class Meta:
		model = Ratio
		
class AddressForm(djangoforms.ModelForm):
	class Meta:
		model = EventAddress

class ParentForm(djangoforms.ModelForm):
	class Meta:
		model = ParentEvent

class StatNameForm(djangoforms.ModelForm):
	class Meta:
		model = StatName
		exclude = ['created_by']
		
class UserStatForm(djangoforms.ModelForm):
	class Meta:
		model=UserStat



class StatForm(forms.Form):
	stat = forms.CharField(max_length = 100)
	num = forms.IntegerField()
	
	def __init__(self, StatName=None, *args, **kwargs):
		self.StatName = StatName
		super(StatForm, self).__init__(*args, **kwargs)
		
	def save(self):
		something = Stat(StatName = self.StatName, stat = self.cleaned_data['stat'], num=self.cleaned_data['num'],)
		something.put()



###Navigation View

def navi(request):
	if str(request.POST.get('submit','')) == 'ADD EVENT':
		return HttpResponsePermanentRedirect('/')
	if str(request.POST.get('submit','')) == 'ADD MULTI-SESSION EVENT':
		return HttpResponsePermanentRedirect('/CountNow/?ShowMultisession=1')
	if str(request.POST.get('submit','')) == 'ALL EVENTS':
		return HttpResponsePermanentRedirect('/recent')
	if str(request.POST.get('submit','')) == 'STATS':
		return HttpResponsePermanentRedirect('/contributor_stats')
	if str(request.POST.get('submit','')) == 'API':
		return HttpResponsePermanentRedirect('/api')
	if str(request.POST.get('submit','')) == 'WHY?':
		return HttpResponsePermanentRedirect('/why')
	if str(request.POST.get('submit','')) == 'FAQ':
		return HttpResponsePermanentRedirect('/faq')
	else:
		return HttpResponsePermanentRedirect('/')
	

###Main views


####This function creates the page for the event statistics.

def event_detail(request, event_key):
	event_in = Input.get(event_key)
	ratio_in = Ratio.all().filter('Input = ', event_in)
	ratio_in = ratio_in.fetch(limit=300)
	addstats  = 0
	addgeotag = 0
	
	
	
	
	if event_in.created_by == users.get_current_user() and not event_in.Address:
		addgeotag=1
	
	stats_in = StatName.all().filter("event =", event_in)
	stats_in = stats_in.fetch(limit=300)
	if len(stats_in) > 0: 
		stats = len(stats_in)
		s = 1
	
	
	else:
		stats=0
		s = 0 
		
	for y in ratio_in:
		if y.created_by == users.get_current_user():
		
			addstats = 1
	
	
		
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	
	return render_to_response('event_detail.html',{'stats': s,'stats_in': stats,'event': event_in, 'ratio_all':ratio_in,  'user': users.get_current_user(), 'addstats':addstats, 'addgeotag':addgeotag,'authenticated':yes_no})


####This creates the page that shows the statistics for multi-session events.

def multisession_event_detail(request, event_key):
	multi_event = ParentEvent.get(event_key)
	addstats1 = 0
	
	ratio = Ratio.all().filter('ParentEvent = ',multi_event)
	ratio=ratio.fetch(limit=300)
	w =0
	m=0
	o=0
	c=0
	
	if len(ratio) > 0:
		for r in ratio:
			if r.created_by == users.get_current_user():
				addstats1 = 1
		
			w += int(r.Women)
			m += int(r.Men)
			o += int(r.Other)
			c += 1
		if w==0 and m==0 and o==0:
			estimate=0
		else:
			if w!=0:
				w = float(w)/float(c)
			if m!=0:
				m = float(m)/float(c)
			if o!=0:
				o = float(o)/float(c)
			estimate= str(w)+' women, '+str(m)+' men, and '+str(o)+' other.'
	elif len(ratio) == 0:
		estimate = 0
	
	
		
	
	events= Input.all().filter('Parent = ', multi_event)
	events = events.fetch(limit=300)
	stats_in = StatName.all().filter("event =", multi_event)
	stats_in = stats_in.fetch(limit=300)
	addgeotag = 0

	if multi_event.created_by == users.get_current_user() and not multi_event.Address:
		addgeotag=1
	yo = ''
	zo = []
	for x in events:
		yo = []
		yo.append(x)
		women = 0 
		men = 0
		other = 0
		ratio = Ratio.all().filter('Input = ', x)
		ratio = ratio.fetch(limit = 100)
		i=0
		
		
		for r in ratio:
			
			women += r.Women
			men +=r.Men
			other += r.Other
			i = i+1
		if women != 0:
			women = (float(women)/ float(i))
		if men !=0:
			men = (float(men)/float(i))
		if other != 0:
			other = (float(other)/float(i))
		yo.append(str(women)+' women '+str(men)+' men , and '+str(other)+' other. <br/><span class="smalltxt"> Counting '+str.lower(str(r.WhatRatio))+ '</span><br />')
		zo.append(yo)
		
	
	
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
		
	return render_to_response('multi_event_detail.html',{'multi_event': multi_event,'addstats': addstats1, 'estimate':estimate,'ratio':ratio, 'zo': zo, 'yo':yo, 'event':request.GET.get('event',''), 'addgeotag':addgeotag, 'events': events, 'user': users.get_current_user(), 'authenticated':yes_no})


#### I think this displays the multisession ratios.
def multisession_event_ratio(request, event_key):
	multi_event = ParentEvent.get(event_key)
	
	ratio_in = Ratio.all().filter('ParentEvent = ',multi_event)
	
	addstats =0
	addgeotag=0
	
	if multi_event.created_by == users.get_current_user() and not multi_event.Address:
		addgeotag=1
	
	stats_in = StatName.all().filter("ParentEvent =", multi_event)
	stats_in = stats_in.fetch(limit=300)
	if len(stats_in) > 0: 
		stats = len(stats_in)
		s = 1
	
	
	else:
		stats=0
		s = 0 
		
		
		
	for y in ratio_in:
		if y.created_by == users.get_current_user():
			addstats = 1
		

		
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	

	return render_to_response('multi_event_ratio.html',{'stats': s,'stats_in': stats,'event': multi_event,'ratio_all':ratio_in,  'user': users.get_current_user(),'addstats':addstats, 'addgeotag':addgeotag, 'authenticated':yes_no})


####This is the page that is available only to logged in users and shows their own stats.

def about_me(request):
	if users.get_current_user():
		
		get_stat = UserStat.all().filter('Contributor =',users.get_current_user())
		get_stat= get_stat.fetch(limit=1)
		if len(get_stat) > 0:
			get_stat = get_stat[0]
		else:
			get_stat = 0
			
		get_ratios = Ratio.all().filter('created_by =', users.get_current_user())
		if get_ratios.count() ==0:
			get_ratios =0
		
		get_events = Input.all().filter('created_by =', users.get_current_user())
		if get_events.count() ==0:
			get_events =0
		
		get_multi_events = ParentEvent.all().filter('created_by', users.get_current_user())
		if get_multi_events.count() == 0:
			get_multi_events =0
		
		
		
		get_other_stats = StatName.all().filter('created_by =', users.get_current_user())
		if get_other_stats.count() == 0:
			get_other_stats = 0
		
		
		if request.method == 'GET':
			
			return render_to_response('about_me.html', {'user': users.get_current_user(), 'events':get_events, 'multi_events':get_multi_events, 'get_stat' : get_stat, 'get_ratios': get_ratios, 'get_other_stats':get_other_stats, })
		elif request.method== 'POST':
			if request.POST.get('gender') != "-----":
				get_stat.Gender = request.POST.get('gender','')
				get_stat.put()
				return render_to_response('about_me.html', {'msg':'Thanks!','user': users.get_current_user(), 'events':get_events, 'multi_events':get_multi_events, 'get_stat' : get_stat, 'get_ratios': get_ratios, 'get_other_stats':get_other_stats })
			else:
				return render_to_response('about_me.html',  {'msg': 'Sorry, "----" is not a valid entry :) ','user': users.get_current_user(),  'events':get_events, 'multi_events':get_multi_events, 'get_stat' : get_stat, 'get_ratios': get_ratios, 'get_other_stats':get_other_stats, })
	else:
		return HttpResponsePermanentRedirect(users.create_login_url('/'))



#### This shows the list of all events.
		
def all_events(request):
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	event_list = Input.all()
	paginator = NamePaginator(event_list, on="Event", per_page=10)
	page = int(request.GET.get('page', '1'))
	page = paginator.page(page)
	return render_to_response('event_all.html', {'page': page, 'user': users.get_current_user(), 'authenticated': yes_no})
	

#### this shows a list of all multisession events.

def all_multisession_events(request):
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
		
	event_list = ParentEvent.all()
	sub_event_list = Input.all()
	paginator = NamePaginator(event_list, on="Name", per_page=10)
	page = int(request.GET.get('page', '1'))
	page = paginator.page(page)
	
	if request.GET.get('add',''):
		
		return render_to_response('event_all_multisession.html', {'page': page, 'user': users.get_current_user(), 'authenticated': yes_no,'Women':request.GET.get('Women',''),'Men':request.GET.get('Men',''),'Other': request.GET.get('Other',''),'key': request.GET.get('key',''),'Event': request.GET.get('Event',''), 'add':1})
	else:

		return render_to_response('event_all_multisession.html', {'page': page, 'user': users.get_current_user(), 'authenticated': yes_no},)

#### Dispalys form to add multi session events

def all_multisession_events_add(request):
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	event_list = ParentEvent.all()
	sub_event_list = Input.all()
	paginator = NamePaginator(event_list, on="Name", per_page=10)
	page = int(request.GET.get('page', '1'))
	page = paginator.page(page)
	return render_to_response('event_all_multisession_add.html', {'page': page, 'user': users.get_current_user(), 'authenticated': yes_no})

####This is for adding statistics about an event - These are different from the gender ratio. The idea is to enable people to add other statistics to an event, not just gender ratios.		

def addstatsform(request):
	ratioform = RatioForm()	
	
	
	if request.method == 'POST' and request.POST.get('key',''):
		if request.POST.get('otherstats',''):
			
			statnameform= StatNameForm()
			statforms = []
			for i in range(7):
				statforms.append(StatForm(prefix = 'f%s'%i))
			payload = dict(statnameform=statnameform, statforms=statforms)
			
			if request.POST.get('multisession','')=='1':
				return render_to_response('addstats.html',{'multi':1,'statnameform':statnameform,'user': users.get_current_user(),'authenticated':'yes', 'statforms':statforms, 'ratioform':ratioform, 'key': request.POST.get('key',''), 'multisession':1,})
			else:
			
				return render_to_response('addstats.html',{'multi':0,'statnameform':statnameform,'user': users.get_current_user(),'authenticated':'yes', 'statforms':statforms, 'ratioform':ratioform, 'key': request.POST.get('key','')})
		
		
			
		if request.POST.get('ratio',''):
			if request.POST.get('multisession','')=='1':
				return render_to_response('ratioform.html',{'CheckContributor':CheckContributor(),'ratioform':ratioform,'key': request.POST.get('key',''),'multisession': 1, 'authenticated':'yes','user': users.get_current_user(),'multisession':1,})		
			else:
				return render_to_response('ratioform.html',{'CheckContributor':CheckContributor(),'ratioform':ratioform,'key': request.POST.get('key',''),'multisession': request.POST.get('multisession',''), 'authenticated':'yes','user': users.get_current_user()})	
		#for update
		if str(request.POST.get('update1',''))=="yes" and str(request.POST.get('multisession','')) != "yes":
			ratioform = RatioForm(request.POST)
			return render_to_response('ratioform.html',{'CheckContributor':CheckContributor(),'ratioform':ratioform,'key': request.POST.get('key',''),'authenticated':'yes','user': users.get_current_user()})		
		
		if str(request.POST.get('update1',''))=="yes" and str(request.POST.get('multisession','')) == "yes":
			ratioform = RatioForm(request.POST)
			return render_to_response('ratioform.html',{'CheckContributor':CheckContributor(),'ratioform':ratioform,'key': request.POST.get('key',''),'authenticated':'yes','user': users.get_current_user(),'multisession':1})
		
	if users.get_current_user() and request.method == 'GET' and request.GET.get('key',''):
		statnameform= StatNameForm()
		statforms = []
		for i in range(7):
			statforms.append(StatForm(prefix = 'f%s'%i))
		payload = dict(statnameform=statnameform, statforms=statforms)
		return render_to_response('addstats.html',{'statnameform':statnameform, 'statforms':statforms, 'ratioform':ratioform, 'error':"Please complete the form",'user': users.get_current_user(),'authenticated':'yes', 'key': request.GET.get('key','')})	
		
	else:
		
		return HttpResponsePermanentRedirect('/all')

####This is for adding statistics about an event - These are different from the gender ratio. The idea is to enable people to add other statistics to an event, not just gender ratios.	
def addstats(request):
	ratioform = RatioForm()	
	check = UserStat.all().filter('Contributor = ', users.get_current_user())
	check = check.fetch(limit=300)
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	
	#error if something is not filled out correctly.
	try:
		int(request.POST.get('Women',''))
	except:
		if request.POST.get('multisession','')!='yes':
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''), 'error': 1})
		else:
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''),'multisession':1, 'error': 1})
	try:
		int(request.POST.get('Men',''))
	except:
		if request.POST.get('multisession','')!='yes':
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''), 'error': 1})
		else:
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''),'multisession':1, 'error': 1})
	try:
		int(request.POST.get('Other',''))
	except:
		if request.POST.get('multisession','')!='yes':
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''), 'error': 1})
		else:
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''),'multisession':1, 'error': 1})
			
	
	
	if request.method=='POST' and request.POST.get('key','') and (int(request.POST.get('Women','',))==0 and int(request.POST.get('Men',''))==0 and int(request.POST.get('Other','',))==0) or (str(request.POST.get('gender','')) == '----'):

		ratioform = RatioForm(request.POST)
		
		
		#return HttpResponsePermanentRedirect('/addstatsform/?key='+request.POST.get('key','')+'&error=complete')
		if request.POST.get('multisession','')!='yes':
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''), 'error': 1})
		else:
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''),'multisession':1, 'error': 1})
	#if request.method=='POST' and int(request.POST.get('Women','',))==0 and int(request.POST.get('Men',''))==0 and int(request.POST.get('Other','',)) ==0 and str(request.POST.get('gender','')) == '----':
	#	if users.get_current_user():
	#		yes_no = 'yes'
	#	else:
	#		yes_no = 'no'
	#	ratioform = RatioForm(request.POST)
	#	return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.POST.get('key',''),})
	
	
	#this is for multisession events.
	
	if request.method == 'POST' and request.POST.get('key','') and request.POST.get('multisession','')=='yes':
	
	
	
		#it shows this if there is no other info being posted to the form..
		if (int(request.POST.get('Women','')) ==0 and int(request.POST.get('Men','')) ==0 and int(request.POST.get('Other','')) == 0) or str(request.POST.get('gender','')) == '----':
				return HttpResponsePermanentRedirect('/addsessionform/?key='+request.POST.get('key','')+'&multisession=yes&error=complete')
				
		if users.get_current_user():
			
			event_in = ParentEvent.get(request.POST.get('key',''))
			#this checks if an update is needed.
			ratio_in1 = Ratio.all().filter('ParentEvent = ',event_in).filter('created_by = ',users.get_current_user())
			
			ratio = ratio_in1.fetch(limit=300)
			
			if ratio:
				#update database...
				ratio[0].Women = int(request.POST.get('Women',''))
				ratio[0].Men = int(request.POST.get('Men',''))
				ratio[0].Other = int(request.POST.get('Other',''))
				ratio[0].ShortDescription = str(request.POST.get('ShortDescription',''))
				ratio[0].put()
				
				
			else:
				save_me = Ratio(created_by = users.get_current_user(),pub_date=datetime.datetime.now(), ParentEvent = event_in, Women = int(request.POST.get('Women','')),Men = int(request.POST.get('Men','')),Other =int(request.POST.get('Other','')), ShortDescription = request.POST.get('ShortDescription',''))
				save_me.save()
				event_in.up_date = datetime.datetime.now() 
				event_in.put()
				#enter user stats...
				ContributorStat(' ')		
				
			ratio_in = Ratio.all().filter('ParentEvent = ', event_in)
			ratio_in = ratio_in.fetch(limit=300)
			if event_in.Address == None:	
				return render_to_response('multi_event_ratio.html',{'addgeotag':1,'event': event_in, 'addstats':1,'ratio_all':ratio_in, 'user': users.get_current_user(), 'authenticated':'yes'})
			else:
				return render_to_response('multi_event_ratio.html',{'event': event_in, 'addstats':1,'ratio_all':ratio_in, 'user': users.get_current_user(), 'authenticated':'yes'})
		
		#if user is not users.get_current_user()	
		else:
			return HttpResponsePermanentRedirect(users.create_login_url('/addstats/?key='+request.POST.get('key','')+'&Women='+request.POST.get('Women','')+'&Men='+request.POST.get('Men','')+'&Other='+request.POST.get('Other','')+'&ShortDescription='+request.POST.get('ShortDescription','')+'&multisession=yes'))
				
			
	#this is for single-session events...
	
	if request.method == 'POST' and request.POST.get('key','') and request.POST.get('multisession','')!='yes' and request.POST.get('gender','')!='----':
		if users.get_current_user():
			
			event_in = Input.get(request.POST.get('key',''))
			#this checks if an update is needed.
			ratio_in1 = Ratio.all().filter('Input = ',event_in).filter('created_by = ',users.get_current_user())
			
			ratio = ratio_in1.fetch(limit=300)
			
			if ratio:
				#update database...
				ratio[0].Women = int(request.POST.get('Women',''))
				ratio[0].Men = int(request.POST.get('Men',''))
				ratio[0].Other = int(request.POST.get('Other',''))
				ratio[0].ShortDescription = str(request.POST.get('ShortDescription',''))
				ratio[0].put()
				
				
			else:
				save_me = Ratio(created_by = users.get_current_user(),pub_date=datetime.datetime.now(), Input = event_in, Women = int(request.POST.get('Women','')),Men = int(request.POST.get('Men','')),Other =int(request.POST.get('Other','')), ShortDescription = request.POST.get('ShortDescription',''))
				save_me.save()
				
		
		
				event_in.up_date = datetime.datetime.now() 
				event_in.put()
				
				
				ContributorStat(request.POST.get('gender',''))	
				#enter user stats...
				
				
		

					
		
			ratio_in = Ratio.all().filter('Input = ', event_in)
			ratio_in = ratio_in.fetch(limit=300)
			return render_to_response('event_detail.html',{'event': event_in, 'addstats':1,'ratio_all':ratio_in, 'user': users.get_current_user(), 'authenticated':'yes'})
		else:
		
			#if user is not current user
			return HttpResponsePermanentRedirect(users.create_login_url('/addstats/?key='+request.POST.get('key','')+'&Women='+request.POST.get('Women','')+'&Men='+request.POST.get('Men','')+'&Other='+request.POST.get('Other','')+'&ShortDescription='+request.POST.get('ShortDescription','')))
	
	
	
	#this is what happens after they log in. If they have to log in. 
	if request.method=='GET' and request.GET.get('key','')!='':
	
		if users.get_current_user():
			yes_no = 'yes'
		else:
			yes_no = 'no'
		ratioform = RatioForm(request.GET)
		if str(request.GET.get('multisession','',)):
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.GET.get('key',''), 'name': request.GET.get('name',''),'multisession':1,})

		else:	
			return render_to_response('ratioform.html',{'checkContributor':check,'authenticated':yes_no, 'CheckContributor':CheckContributor(),'user': users.get_current_user(),'ratioform': ratioform, 'key': request.GET.get('key',''), 'name': request.GET.get('name','')})
		
#### This creates the form to add sessions.
def addsessionform(request):
	form = InputForm()
	ratioform= RatioForm()
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
		
	if request.method == 'GET' and request.GET.get('key','') and request.GET.get('multisession','') == 'yes' and request.GET.get('ratio','')=='0': 
		return render_to_response('inputform.html',{'authenticated':yes_no, 'CheckContributor':CheckContributor(),'key':request.GET.get('key',''),'form':form,'user': users.get_current_user(),'ratioform': ratioform, 'key': request.GET.get('key',''), 'name': request.GET.get('name',''), 'url': request.GET.get('url',''),})
	if users.get_current_user() and request.method == 'GET' and request.GET.get('key','') and request.GET.get('multisession','')=='yes' and request.GET.get('ratio','')=='1':
		return render_to_response('ratioform.html',{'multisession': 1, 'CheckContributor':CheckContributor(), 'authenticated':yes_no, 'ratioform':ratioform,'user': users.get_current_user(), 'key': request.GET.get('key',''),})		
	if users.get_current_user() and request.method == 'GET' and request.GET.get('key','') and request.GET.get('multisession','')=='no' and request.GET.get('ratio','')=='1':
		return render_to_response('ratioform.html',{'CheckContributor':CheckContributor(), 'authenticated':yes_no, 'ratioform':ratioform,'user': users.get_current_user(), 'key': request.GET.get('key',''),})
	if request.GET.get('key','') and request.GET.get('multisession','')=='no' and request.GET.get('session','')=='1':
		return render_to_response('ratioform.html',{'CheckContributor':CheckContributor(), 'authenticated':yes_no, 'ratioform':ratioform,'user': users.get_current_user(), 'key': request.GET.get('key',''),})
	if request.GET.get('key','') and request.GET.get('session','')=='1':
		form = InputForm(request.GET)
		ratioform = RatioForm(request.GET)
		return render_to_response('inputform.html',{'CheckContributor':CheckContributor(), 'authenticated':yes_no, 'form': form, 'ratioform':ratioform,'user': users.get_current_user(), 'key': request.GET.get('key',''),})
	
	
	#else:
		#return HttpResponsePermanentRedirect(users.create_login_url('/all'))



####this adds the user-defined statistics --- this is only possible if they have already entered some gender related stats. Therefore, they are already registered as a contributor in the UserStats table.


def addmorestats(request):
    if request.method == 'POST':      
    	if request.POST.get('key','') != '' and request.POST.get('name','') != '' and request.POST.get('f0-stat','') != '':
    		#save the title of the stat
    		if str(request.POST.get('multisession',''))=='1':
    			ev = ParentEvent.get(request.POST.get('key',''))
    			enter = StatName(name = request.POST.get('name','').decode('iso-8859-1'), ParentEvent = ev, created_by=users.get_current_user())
    		else:
    			ev = Input.get(request.POST.get('key',''))
    			enter = StatName(name = request.POST.get('name','').decode('iso-8859-1'), event = ev, created_by=users.get_current_user())
    			
    		
    		ev.up_date = datetime.datetime.now()
    		ev.put()
    		name = enter.save()
    		statforms = []
    		for i in range(7):
    			statforms.append(StatForm(StatName=name, prefix = 'f%s'%i, data=request.POST))
    		for f in statforms:
    			if f.is_valid():
    				f.save()
    		
    		
    		
    		#update the user stats...
    		ContributorStatStat()
    		
    	
    		stat = Stat.all().filter('StatName = ', name)
    			
    		if str(request.POST.get('multisession',''))=='1':
    			return render_to_response('stat.html',{'StatName': enter, 'stat': stat , 'user': users.get_current_user(), 'authenticated':'yes', 'multi': 1})
    		else:
    			return render_to_response('stat.html',{'StatName': enter, 'stat': stat , 'user': users.get_current_user(), 'authenticated':'yes'})
    	
    	elif request.POST.get('key','') == '' or request.POST.get('name','') == '':
			if request.POST.get('multisession','') =='1':
				return HttpResponsePermanentRedirect('/addstatsform?key='+str(request.POST.get('key',''))+'&multisession=1')
			else:
				return HttpResponsePermanentRedirect('/addstatsform?key='+str(request.POST.get('key','')))
    	else:
    		return render_to_response('thanks.html',{'user': users.get_current_user(),})

def api(request):
	return render_to_response('api.html',{'user': users.get_current_user(),})
		
def showstats(request,event_key):
	if str(request.GET.get('multi','')) == '1':
		event_in = ParentEvent.get(event_key)
		stat_names = StatName.all().filter('ParentEvent = ',event_in)
	else:
		event_in = Input.get(event_key)
		stat_names = StatName.all().filter('event = ',event_in)
	
	stat_names = stat_names.fetch(limit=300)
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	if str(request.GET.get('multi','')) == '1':
		return render_to_response('show_stats.html',{'event': event_in, 'stat_names': stat_names, 'user': users.get_current_user(), 'multi': 1, 'authenticated':yes_no})
	if str(request.GET.get('multi',''))!='1':
		return render_to_response('show_stats.html',{'event': event_in, 'stat_names': stat_names, 'user': users.get_current_user(), 'authenticated':yes_no})

def stat(request,stat_key):
	stat_in = StatName.get(stat_key)
	stat = Stat.all().filter('StatName = ', stat_in)
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	if str(request.GET.get('multi','')) =='1':	
		return render_to_response('stat.html',{'StatName': stat_in, 'stat': stat, 'user': users.get_current_user(), 'authenticated':yes_no, 'multi':1})	
	else:
		return render_to_response('stat.html',{'StatName': stat_in, 'stat': stat, 'user': users.get_current_user(), 'authenticated':yes_no})


def Show_ContributorStat(request):
	fem = UserStat.all().filter('Gender = ','female').count()
	men = UserStat.all().filter('Gender = ','male').count()
	other = UserStat.all().filter('Gender = ','other').count()
	
	
	fem_stats = 0
	men_stats =0
	other_stats =0 
	
	fem_ratios = 0
	men_ratios =0
	other_ratios =0
	
	fem_events = 0
	men_events =0
	other_events =0 
	
	fem_multievents = 0
	men_multievents =0
	other_multievents =0 
	
	for x in UserStat.all().filter('Gender = ','female'):
		fem_ratios += x.Ratios
		fem_stats += x.Stats
		fem_events +=x.Events
		fem_multievents +=x.Multi_Events
	
	for y in UserStat.all().filter('Gender = ','male'):
		men_ratios += y.Ratios
		men_stats += y.Stats
		men_events +=y.Events
		men_multievents +=y.Multi_Events
		
	for z in UserStat.all().filter('Gender = ','other'):
		other_ratios += z.Ratios
		other_stats += z.Stats
		other_events +=z.Events
		other_multievents +=z.Multi_Events
	
	return render_to_response('contributor_stats.html',{ 'user': users.get_current_user(), 'fem_stats':fem_stats, 'women': fem, 'men':men, 'other':other, 'men_stats': men_stats, 'other_stats':other_stats, 'fem_ratios': fem_ratios, 'men_ratios':men_ratios, 'other_ratios':other_ratios,  'fem_events': fem_events, 'men_events':men_events, 'other_events':other_events,'fem_multievents': fem_multievents, 'men_multievents':men_multievents, 'other_multievents':other_multievents, })


#this updates the UserStat table.

def ContributorStat(gender):
	obj = UserStat.all().filter('Contributor = ', users.get_current_user())
	obj1 = obj.fetch(limit=1)
			

	if len(obj1) >0:
		#if yes, just update the ratio number	

		obj1[0].Ratios += 1
		obj1[0].put()
		
				
	else: 
		check = UserStat(Contributor = users.get_current_user(), Gender = gender, Ratios = 1,)  
		check.save()


def ContributorMultiEventStat(gender):
	obj = UserStat.all().filter('Contributor =', users.get_current_user())
	obj1 = obj.fetch(limit=1)
	
	if len(obj1) >0:
		obj1[0].Multi_Events += 1
		obj1[0].put()
	else: 
		check = UserStat(Contributor = users.get_current_user(), Gender = gender, Multi_Events = 1,)  
		check.save()



def ContributorStatStat():
	obj = UserStat.all().filter('Contributor =', users.get_current_user())
	obj1 = obj.fetch(limit=1)
	if  obj1[0].Stats!=None:	
		obj1[0].Stats += 1
		obj1[0].put()
	else: 
		obj1[0].Stats=1
		obj1[0].put()


def ContributorEventStat(gender):
	obj = UserStat.all().filter('Contributor =', users.get_current_user())
	obj1 = obj.fetch(limit=1)
	if  obj1 != []:	
		obj1[0].Events += 1
		obj1[0].put()
	else: 
		check = UserStat(Contributor = users.get_current_user(), Gender = gender, Events = 1,)  
		check.save()
		
#### Checks if the person who contributes is registered.
def CheckContributor():
	check = UserStat.all().filter('Contributor = ', users.get_current_user())
	check1 = check.fetch(limit=1)
	if len(check1) >0:
		return 0
	else:
		return 1

 
##### this just displays the front page.		
def CountMe(request):
	form = InputForm()	
	ratioform= RatioForm()
	form.created_by = users.get_current_user()
	#if there is a 
	
	if request.GET.get('Women','') and request.GET.get('Men','') and request.GET.get('Other','') and request.GET.get('Event',''):
		form = InputForm(request.GET)
		ratioform= RatioForm(request.GET)
		return render_to_response('form.html',{'form':form, 'ratioform': ratioform,'user': users.get_current_user(),'CheckContributor':CheckContributor()})
	else:
		return render_to_response('form.html',{'form':form, 'ratioform': ratioform,'user': users.get_current_user(),'CheckContributor':CheckContributor()})

 
###This handels everything involved in the "Add an event form"

def CountNow(request):	
	form = InputForm()	
	ratioform = RatioForm()
	parentform = ParentForm()
	userform = UserStatForm()
	form.user = users.get_current_user()
	InForm = InputForm(request.POST)	
	event_list = ParentEvent.all()
	paginator = NamePaginator(event_list, on="Name", per_page=10)
	page = int(request.GET.get('page', '1'))
	page = paginator.page(page)
	
	#This shows the multisession form
	if request.method =='GET':
		if request.GET.get('ShowMultisession','')=='1' and not request.GET.get('Event',''):
			get_stat = UserStat.all().filter('Contributor =',users.get_current_user())
			
			if get_stat.count() > 0:
				return render_to_response('form2.html',{'form':InForm, 'ratioform':ratioform, 'parentform': parentform, 'page' : page, 'user': users.get_current_user()} )
			else:
				return render_to_response('form2.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform':ratioform, 'parentform': parentform, 'page' : page, 'user': users.get_current_user()} )
		
		#This shows the multisession form with values when the person was previously re-directed to the login screen.
		elif request.GET.get('ShowMultisession','') =='1' and request.GET.get('Event',''):
			form = InputForm(request.GET)	
			ratioform = RatioForm(request.GET)
			parentform = ParentForm(request.GET)
			userform = UserStatForm(request.GET)
			get_stat = UserStat.all().filter('Contributor =',users.get_current_user())
			
			if get_stat.count() > 0:
				return render_to_response('form2.html',{'form':form, 'Women1':request.GET.get('Women1'),'Men1':request.GET.get('Men1'),'Other1':request.GET.get('Other1'),'Event_URL1':request.GET.get('Event_URL1'), 'ShortDescription':request.GET.get('ShortDescription'),'ShortDescription1':request.GET.get('ShortDescription1'), 'ratioform':ratioform, 'parentform': parentform, 'page' : page, 'user': users.get_current_user()} )
			else:
				return render_to_response('form2.html',{'CheckContributor':CheckContributor(),'form':form, 'Women1':request.GET.get('Women1'),'Men1':request.GET.get('Men1'),'Other1':request.GET.get('Other1'),'Event_URL1':request.GET.get('Event_URL1'),'ShortDescription':request.GET.get('ShortDescription'),'ShortDescription1':request.GET.get('ShortDescription1'),   'ratioform':ratioform, 'parentform': parentform, 'page' : page, 'user': users.get_current_user()} )
		
		else:
			return HttpResponsePermanentRedirect('/')
		
	
	if request.method == 'POST':
		
		#the following handles forms that are not complete... or filled out incorrectly...
		try:
			int(request.POST.get('Women',''))
		except:
			return render_to_response('form.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform': ratioform,'user': users.get_current_user(),'error':'Please fill the form out completely',})
		try:
			int(request.POST.get('Men',''))
		except:
			return render_to_response('form.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform': ratioform,'user': users.get_current_user(),'error':'Please fill the form out completely',})
		try:
			int(request.POST.get('Other',''))
		except:
			return render_to_response('form.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform': ratioform,'user': users.get_current_user(),'error':'Please fill the form out completely',})
			
		
		if (int(request.POST.get('Women',''))==0 and int(request.POST.get('Men',''))==0 and int(request.POST.get('Other',''))==0) or (str(request.POST.get('gender','',))=='----'):
			if  request.POST.get('MultiEvent','')!='1' and request.POST.get('key','') == '':
				return render_to_response('form.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform': ratioform,'user': users.get_current_user(),'error':'Please fill the form out completely',})	
			
			
			elif (request.POST.get('MultiEvent','')=='1' and request.POST.get('key','') == '') or str(request.POST.get('gender','',))=='----':
				return render_to_response('form2.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform':ratioform, 'parentform': parentform, 'page' : page, 'user': users.get_current_user(), 'error':'Please fill the form out completely' })
			elif request.POST.get('key','')!= '' and request.POST.get('multisession','') != 'yes':
				return HttpResponsePermanentRedirect('/addsessionform/?key='+request.POST.get('key','')+'&multisession=no&error=complete')
			elif request.POST.get('key','') != '' and request.POST.get('multisession','')=='yes' and request.POST.get('session','')!='1' :
				return HttpResponsePermanentRedirect('/addsessionform/?key='+request.POST.get('key','')+'&multisession=yes&error=complete')
			elif request.POST.get('key','')!='' and request.POST.get('session','')=='1' and request.POST.get('multisession','')=='yes':
				if users.get_current_user():
					yes_no = 'yes'
				else:
					yes_no = 'no'
				return render_to_response('inputform.html',{'authenticated':yes_no,'key':str(request.POST.get('key','')),'blah': 'fasdfs', 'CheckContributor':CheckContributor(), 'form':form,'user': users.get_current_user(),'ratioform': ratioform, 'name': request.GET.get('name',''), 'url': request.GET.get('url',''),'error':'complete'})

				
		if  request.POST.get('MultiEvent','')!='1' and request.POST.get('key','') == '' and request.POST.get('Event','')=='':
			return render_to_response('form.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform': ratioform,'user': users.get_current_user(),'error':'Please fill the form out completely',})
			
		
		if request.POST.get('MultiEvent','')!='' and request.POST.get('key','') == '' and request.POST.get('Name','') == '' or request.POST.get('Event','') == '':
			if request.POST.get('session'):
				if users.get_current_user():
					yes_no = 'yes'
				else:
					yes_no = 'no'
				return render_to_response('inputform.html',{'authenticated':yes_no, 'key':request.POST.get('key',''), 'CheckContributor':CheckContributor(), 'form':form,'user': users.get_current_user(),'ratioform': ratioform, 'name': request.GET.get('name',''), 'url': request.GET.get('url',''),'error':'complete'})
			else:
				return render_to_response('form2.html',{'CheckContributor':CheckContributor(),'form':InForm, 'ratioform':ratioform, 'parentform': parentform, 'page' : page, 'user': users.get_current_user(), 'error':'Please fill the form out completely' })	
		
		
		else:
		
			if users.get_current_user():
				#insert stuff into DB first then add the form for geotagging if necessary.
				#This is just for a normal event. not attached to a multisession event.
				if InForm.is_valid() and str(request.POST.get('JustEvent'))=='1':
					
					year, month, day = map(int, request.POST.get('EventDay').split("-"))

					#db_enter = Input(Event = request.POST.get('Event',''),Event_URL = request.POST.get('Event_URL',''),EventDay = date(year, month,day), up_date=datetime.datetime.now(), pub_date=datetime.datetime.now(),ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())
					
					db_enter = Input(Event = request.POST.get('Event','').decode('iso-8859-1'),Event_URL = request.POST.get('Event_URL',''),EventDay = datetime.date(year,month,day),up_date=datetime.datetime.now(), pub_date=datetime.datetime.now(),ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())
					db_enter.save()
					
					#enter contributor stats
					ContributorEventStat(str(request.POST.get('gender','')))
					
					ratio_enter = Ratio(Input = db_enter,WhatRatio=str(request.POST.get('WhatRatio','')), Women = int(request.POST.get('Women','')),Men = int(request.POST.get('Men','')), Other = int(request.POST.get('Other','')),  pub_date=datetime.datetime.now(),ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())	
					ratio_enter.save()
				
				
				
					#enter contributor stats...
					ContributorStat(request.POST.get('gender',''))
				
					t_str='Gender Ratio Report:'
					#update twitter
					hashtag = ""
					
					if str(request.POST.get('hashtag',''))!="#":
						hashtag = str(request.POST.get('hashtag',''));
						
					truncated = (str(request.POST.get('Event',''))[:47] + '...') 
					twitter_string = truncated+' '+str(request.POST.get('Women',''))+' women, '+str(request.POST.get('Men',''))+' men, '+str(request.POST.get('Other',''))+' other. '+URLshorten('http://b-counted.appspot.com/event/'+str(db_enter.key()))+' #GenderRatioReport ' + hashtag
		
					##update_twitter(twitter_string)
					return HttpResponsePermanentRedirect('/event/'+str(db_enter.key())+'/')
					
				#this is for the data that comes from the multi-session event form.
				#_______________
				elif InForm.is_valid() and str(request.POST.get('MultiEvent'))=='1' and request.POST.get('Event','') !='':
				
					year, month, day = map(int, request.POST.get('EventDay').split("-"))
					Multisession= ParentEvent(Name = str(request.POST.get('Name','')).decode('iso-8859-1'),  Event_URL = str(request.POST.get('Event_URL1','')), created_by = users.get_current_user(),up_date=datetime.datetime.now(), pub_date=datetime.datetime.now(),NumEvents=1,)
					Multisession.save()
					
					#update contributor stats
					ContributorMultiEventStat(request.POST.get('gender',''))
					
					db_enter = Input(Event = request.POST.get('Event','').decode('iso-8859-1'), Parent = Multisession, Event_URL = str(request.POST.get('Event_URL1','')),EventDay = datetime.date(year,month,day),pub_date=datetime.datetime.now(),up_date=datetime.datetime.now(), ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())
					db_enter.save()
					
					ContributorEventStat(str(request.POST.get('gender','')))
					
					ratio_enter = Ratio(Input = db_enter, WhatRatio=str(request.POST.get('WhatRatio','')),Women = int(request.POST.get('Women','')),Men = int(request.POST.get('Men','')), Other = int(request.POST.get('Other','')),  pub_date=datetime.datetime.now(),ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())	
					ratio_enter.save()
					ContributorStat(request.POST.get('gender',''))	
					
					if int(request.POST.get('Men1','')) != 0 or int(request.POST.get('Women1','')) != 0 or int(request.POST.get('Other1','')) !=0:
						ratio_enter1 = Ratio(ParentEvent = Multisession, Women = int(request.POST.get('Women1','')),Men = int(request.POST.get('Men1','')), Other = int(request.POST.get('Other1','')),  pub_date=datetime.datetime.now(),ShortDescription=str(request.POST.get('ShortDescription1','')),created_by = users.get_current_user())	
						ratio_enter1.save()
				
						ContributorStat(request.POST.get('gender',''))	
				
					t_str='Gender Ratio Report: '
					
					hashtag = "";
					if str(request.POST.get('hashtag',''))!="#":
						hashtag = str(request.POST.get('hashtag',''));
						
					truncated = (str(request.POST.get('Event',''))[:47] + '...') 
					##twitter_string =truncated+' '+str(request.POST.get('Women',''))+' women, '+str(request.POST.get('Men',''))+' men, '+str(request.POST.get('Other',''))+' other. '+URLshorten('http://b-counted.appspot.com/event/'+str(db_enter.key()))+ ' #GenderRatioReport ' + hashtag
					#update_twitter(twitter_string)
					return HttpResponsePermanentRedirect('/multisession-event/'+str(Multisession.key())+'/?event='+str(db_enter.key()))
				
				#this is for sessions that get connected to a multisession event after the multisession event has already been entered in the database by another person.
				#_______________________
				elif InForm.is_valid() and request.POST.get('Event','') !='' and request.POST.get('key'):
			
					key = ParentEvent.get(request.POST.get('key',''))
					year, month, day = map(int, request.POST.get('EventDay').split("-"))
					
					
					db_enter = Input(Event = str(request.POST.get('Event','')).decode('iso-8859-1'), Parent = key, Event_URL = str(request.POST.get('Event_URL','')),EventDay = datetime.date(year,month,day), pub_date=datetime.datetime.now(),up_date=datetime.datetime.now(), ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())
					db_enter.save()
					if str(request.POST.get('gender',''))!='':
						ContributorEventStat(str(request.POST.get('gender','')))
					else:
						ContributorEventStat('')
						
					ratio_enter = Ratio(Input = db_enter, WhatRatio=str(request.POST.get('WhatRatio','')),Women = int(request.POST.get('Women','')),Men = int(request.POST.get('Men','')), Other = int(request.POST.get('Other','')),  pub_date=datetime.datetime.now(),ShortDescription=str(request.POST.get('ShortDescription','')),created_by = users.get_current_user())	
					ratio_enter.save()
				
					#enter contributor stats...
					if str(request.POST.get('gender',''))!='':
						ContributorStat(request.POST.get('gender',''))
					else:
						ContributorStat(request.POST.get('gender',''))

				
					#enter the updated_by
				
					key.up_date = datetime.datetime.now()
								
					#enter the 
					key.NumEvents = key.NumEvents + 1
					key.put()
				 	hashtag = ""
					
					#update twitter
					if str(request.POST.get('hashtag',''))!="#":
						hashtag = str(request.POST.get('hashtag',''));
					
						
				  	truncated = (str(request.POST.get('Event',''))[:47] + '...') 
					twitter_string =truncated+' '+str(request.POST.get('Women',''))+' women, '+str(request.POST.get('Men',''))+' men, '+str(request.POST.get('Other',''))+' other. '+URLshorten('http://b-counted.appspot.com/event/'+str(db_enter.key())) + ' #GenderRatioReport '+hashtag
					##update_twitter(twitter_string)
					return HttpResponsePermanentRedirect('/event/'+str(db_enter.key())+'/')					
				
				else:
					return render_to_response('form.html',{'form':InForm, 'ratioform': ratioform,'user': users.get_current_user(),'error':'Please fill the form out completely',})				
			
			
			elif str(request.POST.get('MultiEvent'))=='1' and not users.get_current_user() and str(request.POST.get('session'))!='1':

				return HttpResponsePermanentRedirect(users.create_login_url('/CountNow/?ShowMultisession=1&Women='+str(request.POST.get('Women',''))+'&Men='+str(request.POST.get('Men',''))+'&Other='+str(request.POST.get('Other',''))+'&Event='+str(request.POST.get('Event',''))+'&Name='+str(request.POST.get('Name',''))+'&Women1='+str(request.POST.get('Women1',''))+'&Men1='+str(request.POST.get('Men1',''))+'&Other1='+str(request.POST.get('Other1',''))+'&Event_URL='+str(request.POST.get('Event_URL',''))+'&Event_URL1='+str(request.POST.get('Event_URL1',''))+'&Name='+str(request.POST.get('Name',''))+'&Women1='+str(request.POST.get('Women1',''))+'&Men1='+str(request.POST.get('Men1',''))+'&Other1='+str(request.POST.get('Other1',''))+'&Event_URL='+str(request.POST.get('Event_URL',''))+'&ShortDescription='+str(request.POST.get('ShortDescription',''))+'&ShortDescription1='+str(request.POST.get('ShortDescription1',''))))
			
			elif not users.get_current_user() and str(request.POST.get('session'))=='1':
				return HttpResponsePermanentRedirect(users.create_login_url('/addsessionform/?session=1&key='+str(request.POST.get('key',''))+'&Women='+str(request.POST.get('Women',''))+'&Men='+str(request.POST.get('Men',''))+'&Other='+str(request.POST.get('Other',''))+'&Event='+str(request.POST.get('Event',''))+'&Name='+str(request.POST.get('Name',''))+'&Event_URL'+str(request.POST.get('Event_URL',''))))

			else:
				return HttpResponsePermanentRedirect(users.create_login_url('/CountMe/?Women='+str(request.POST.get('Women',''))+'&Men='+str(request.POST.get('Men',''))+'&Other='+str(request.POST.get('Other',''))+'&Event='+str(request.POST.get('Event',''))+'&Name='+str(request.POST.get('Name',''))+'&Women1='+str(request.POST.get('Women1',''))+'&Men1='+str(request.POST.get('Men1',''))+'&Other1='+str(request.POST.get('Other1',''))+'&Event_URL'+str(request.POST.get('Event_URL',''))+'&Event_URL1='+str(request.POST.get('Event_URL1',''))+'&ShortDescription1='+str(request.POST.get('ShortDescription1',''))))

				
#geocode apartment address via yahoo maps api
 
def geocode(street, city, zip, country):
	location = street+" "+city+" "+zip+" "+country
	#appid ='xVIdq9TV34EZsdR7UqPO8FGX_.SLZhlzmH2CY1uvhK0E0vD3n0GqWDQFLGeKHA--'
	appid ='uoetVRjV34H4y6VxiliwllX3tj9lmHNLFTag_tfXjQOWNJf4vulF3xvWdtF3WQ--'
	parms = {'appid': appid, 'location': location}
	url = 'http://api.local.yahoo.com/MapsService/V1/geocode?'+urllib.urlencode(parms)
	result = urlfetch.fetch(url)
	if result.status_code==200:
		dom = minidom.parseString(result.content)
		latitude = dom.getElementsByTagName('Latitude')[0].firstChild.data
		longitude = dom.getElementsByTagName('Longitude')[0].firstChild.data
		coords=[latitude,longitude]
		return coords
	else:
		coords=[0,0]
		return coords
	
		
####function for adding geotags to events.		
def Geotag(request):
	Address1 = 0
	Address2=0
	addressform = AddressForm()
			
	#save the address if an address is provided...
	
	
	if request.method == 'POST':
		if request.POST.get('tag',''):
			if users.get_current_user():
			
				#if it is just one event it gets one address
				#--------------------------------------------
				if  request.POST.get('event','')!= '' and request.POST.get('Street','') != '' and request.POST.get('multi_event','') == '':
					coords = geocode(str(request.POST.get('Street','')),str(request.POST.get('City','')),str(request.POST.get('Zip','')),str(request.POST.get('Country','')))
					#print coords[0], coords[1],request.POST.get('Street1',''),request.POST.get('City1',''),request.POST.get('Zip1','')
					
					if coords[0] != 0:
						
						Address1 = EventAddress(Street=str(request.POST.get('Street','')),
							City=str(request.POST.get('City','')),
							State=str(request.POST.get('State','')),
							Zip = str(request.POST.get('Zip','')),
							Country=str(request.POST.get('Country','')),
							latitude =float(coords[0]), 
							longitude =float(coords[1]),
							created_by = users.get_current_user(),)
							
						Address1.save()
						event = Input.get(request.POST.get('event',''))
						event.Address = Address1
						event.put()
						return HttpResponsePermanentRedirect('/event/'+str(event.key())+'/')
					else:
						#send a message...
						return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'Sorry.The geocoder did not recognize this address.'})	
						
				#if it is just a multi-session event without attached session it gets an address.
				#----------------------------------------------------------------------------------------
				
				if request.POST.get('Street1','') != '' and request.POST.get('multi_event','') != '' and request.POST.get('event','')=='':
					coords = geocode(str(request.POST.get('Street1','')),str(request.POST.get('City1','')),str(request.POST.get('Zip1','')),str(request.POST.get('Country1','')))
					#coords = geocode(request.POST.get('Street1','')+' '+request.POST.get('City1','')+' '+request.POST.get('Zip1','')+' '+request.POST.get('Country1',''))
					#print coords[0], coords[1],request.POST.get('Street1',''),request.POST.get('City1',''),request.POST.get('Zip1','')
					if coords[0] != 0:
						Address2 = EventAddress(Street=str(request.POST.get('Street1','')),
							City=str(request.POST.get('City1','')),
							State=str(request.POST.get('State1','')),
							Zip = str(request.POST.get('Zip1','')),
							Country=str(request.POST.get('Country1','')),
							latitude =float(coords[0]), 
							longitude = float(coords[1]),
							created_by = users.get_current_user(),)
						Address2.save()
						multi_event = ParentEvent.get(request.POST.get('multi_event',''))
						multi_event.Address = Address2
						multi_event.put()
						return HttpResponsePermanentRedirect('/multisession-event/'+str(multi_event.key())+'/')
					else:
						return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'please fill the form out completely'})	
					
				#if it is multi-session event with session, then it gets more complicated...	
				#----------------------------------------------------------------------------------------
				if request.POST.get('multi_event','') != '' and request.POST.get('event','') != '' and request.POST.get('Street','') != '':
				
				
		
					
					if request.POST.get('same','') =='no':
						multi_event = ParentEvent.get(request.POST.get('multi_event',''))
						event = Input.get(request.POST.get('event',''))
						
						coords = geocode(str(request.POST.get('Street','')),str(request.POST.get('City','')),str(request.POST.get('Zip','')),str(request.POST.get('Country','')))
						#print coords[0], coords[1],request.POST.get('Street',''),request.POST.get('City',''),request.POST.get('Zip','')
						if coords[0] != 0:
							Address1 = EventAddress(Street=str(request.POST.get('Street','')),
								City=str(request.POST.get('City','')),
								State=str(request.POST.get('State','')),
								Zip = str(request.POST.get('Zip','')),
								Country=str(request.POST.get('Country','')),
								latitude =float(coords[0]), 
								longitude = float(coords[1]),
								created_by = users.get_current_user(),)
								
							Address1.save()
							
							event.Address = Address1
							event.put()
							
						else:
							return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'please fill the form out completely'})						

						coords = geocode(str(request.POST.get('Street1','')),str(request.POST.get('City1','')),str(request.POST.get('Zip1','')),str(request.POST.get('Country1','')))
						
						
						
						
						if coords[0] != 0:
							Address2 = EventAddress(Street=str(request.POST.get('Street1','')),
								City=str(request.POST.get('City1','')),
								State=str(request.POST.get('State1','')),
								Zip = str(request.POST.get('Zip1','')),
								Country=str(request.POST.get('Country1','')),
								latitude =float(coords[0]), 
								longitude = float(coords[1]),
								created_by = users.get_current_user(),)
							Address2.save()
							
							multi_event.Address = Address2
							multi_event.put()
							return HttpResponsePermanentRedirect('/multisession-event/'+str(multi_event.key())+'/')
						else:
							return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'please fill the form out completely'})						
					
					elif request.POST.get('same','') == 'yes':
						multi_event = ParentEvent.get(request.POST.get('multi_event',''))
						coords = geocode(str(request.POST.get('Street','')),str(request.POST.get('City','')),str(request.POST.get('Zip','')),str(request.POST.get('Country','')))
						#print coords[0], coords[1], coords[0], coords[1],request.POST.get('Street',''),request.POST.get('City',''),request.POST.get('Zip','')
						if coords[0] != 0:
							Address1 = EventAddress(Street=str(request.POST.get('Street','')),
								City=str(request.POST.get('City','')),
								State=str(request.POST.get('State','')),
								Zip = str(request.POST.get('Zip','')),
								Country=str(request.POST.get('Country','')),
								latitude =float(coords[0]), 
								longitude = float(coords[1]),
								created_by = users.get_current_user(),)
							Address1.save()
							#yeah... sorry, this needs to be here, so that everything can eventually be cleanly deleted.
							Address2 = EventAddress(Street=str(request.POST.get('Street','')),
								City=str(request.POST.get('City','')),
								State=str(request.POST.get('State','')),
								Zip = str(request.POST.get('Zip','')),
								Country=str(request.POST.get('Country','')),
								latitude =float(coords[0]), 
								longitude = float(coords[1]),
								created_by = users.get_current_user(),)
							Address2.save()
							multi_event.Address=Address1
							multi_event.put()
							event = Input.get(request.POST.get('event',''))
							event.Address = Address2
							event.put()
					
							return HttpResponsePermanentRedirect('/multisession-event/'+str(multi_event.key())+'/')
							
						else:
							return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'please fill the form out completely'})
							
					else:
						return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'please fill the form out completely'})
				else:
					return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user(), 'error': 'please fill the form out completely'})
		
		
			else:
				return HttpResponsePermanentRedirect(users.create_login_url('/'))
		else: 
			return render_to_response('geotag.html',{'form':addressform,'event': request.POST.get('event',''), 'multi_event':request.POST.get('multi_event',''), 'user': users.get_current_user()})
			
		
	else: 
		return HttpResponsePermanentRedirect('/')	
			
			
# delete ------------------------

####delete the ratio --- and the stats --- and much more

def delete_it(request):
	#get the ratio

	ratio = Ratio.get(request.GET.get('ratio',''))

	
	
	#depending on if this is a multisession event or just an event, the selection process is different.
	if request.GET.get('multi','') !='1':
		all_ratio = Ratio.all().filter('Input = ', ratio.Input)
	else:
		all_ratio = Ratio.all().filter('ParentEvent = ',ratio.ParentEvent) 
	
	
 	all_ratio = all_ratio.fetch(limit = 300)
 	
 	
 	#this happens if there are more ratios connected to one event.
 	if len(all_ratio) > 1:
		ratio.delete()
		Delete_UserStat('Ratios')

	#if this is the only ratio connected to a certain event, delete that event, too. 
	elif len(all_ratio) == 1:
		
		if request.GET.get('multi','') != '1':
			#if there is a multi-session event connected to it 
			#but if it is not a ratio that describes the ratio at a multi-session event.
			#-----------------------------------------------------------------------
			if ratio.Input.Parent:
				#if this is the last event/session connected to this multi-session event delete everything...
				#-----------------------------------------------------------------------
				if ratio.Input.Parent.NumEvents ==1:
					#also delete the stats that go with it
					stats = StatName.all().filter('event =',ratio.Input)
					
					if stats.count() > 0:
						for s in stats:
							sta = Stat.all().filter('StatName =', s)
							for ta in sta:
								ta.delete()
							s.delete()
							Delete_UserStat('Stats')
					#check if multi-session event has ratios connected. 
					ra = Ratio.all().filter('ParentEvent =',ratio.Input.Parent)
					if ra.count() > 0:
						for r in ra:
							r.delete()
							Delete_UserStat('Ratios')
					#check if multi-session event has stats connected. 
					st = Ratio.all().filter('ParentEvent =',ratio.Input.Parent)
					if st.count() > 0:
						for sa in st:
							sta = Stat.all().filter('StatName =', sa)
							for ta in sta:
								ta.delete()
							sa.delete()
							
							Delete_UserStat('Stats')
					
					#delete parent event // a.k.a. the multisession event
					ratio.Input.Parent.delete()
					ratio.Input.delete()
					Delete_UserStat('Events')
					Delete_UserStat('Multi_Events')
				#if it is not the last event/session connected to this multi-session event just subtract 
				# one event along with all the stats that go with it.
				#----------------------------------------------------
				else:
					ratio.Input.Parent.NumEvents = ratio.Input.Parent.NumEvents -1
					ratio.Input.Parent.put()
					#also delete the stats that go with it
					stats = StatName.all().filter('event =',ratio.ParentEvent)
					if stats.count() > 0:
						for s in stats:
							sta = Stat.all().filter('StatName =', s)
							for ta in sta:
								ta.delete()
							s.delete()
							Delete_UserStat('Stats')
					ratio.Input.delete()
					Delete_UserStat('Events')
			
			
			
			#if the event not connected to a multi-session event AND this is the last ratio. 
			#just delete the ratio along with the event
			#----------------------------------------------------
			else:
				
				stats = StatName.all().filter('event =',ratio.Input)
				if stats.count() > 0:
					for s in stats:
						sta = Stat.all().filter('StatName =', s)
						for ta in sta:
							ta.delete()
						s.delete()
						Delete_UserStat('Stats')
				
				ratio.Input.delete()	
				Delete_UserStat('Events')
				
		 	
		 
		ratio.delete()
		Delete_UserStat('Ratios')
	
		

	if len(all_ratio)== 1 and request.GET.get('multi','')=='0':
		return render_to_response('thanks.html',{'user': users.get_current_user(), 'authenticated':'yes'})
	elif len(all_ratio) == 1 and request.GET.get('multi','')=='1':
		return HttpResponsePermanentRedirect('/multisession-event/'+str(ratio.ParentEvent.key())+'/')
	elif len(all_ratio)>1 and request.GET.get('multi','')=='0':
		return HttpResponsePermanentRedirect('/event/'+str(ratio.Input.key())+'/')	
	elif len(all_ratio) >1 and request.GET.get('multi','')!='0':
		return HttpResponsePermanentRedirect('/multisession-ratio/'+str(ratio.ParentEvent.key())+'/')

#delete records of stats

def Delete_UserStat(type):
	obj1 = UserStat.all().filter('Contributor =', users.get_current_user())
	obj1 = obj1.fetch(limit=1)
	
	if type == 'Multi_Events':
		obj1[0].Multi_Events= int(obj1[0].Multi_Events) - 1
	if type == 'Events':
		obj1[0].Events= int(obj1[0].Events) - 1
	if type == 'Stats':
		obj1[0].Stats= int(obj1[0].Stats) - 1
	if type == 'Ratios':
		obj1[0].Ratios= int(obj1[0].Ratios) - 1
	
	obj1[0].put()

		
	
#delete statistics (these are different from the gender ratios)
def delete_stat(request):
	#get the name of the stat
	
	stat_name = StatName.get(request.GET.get('stat_key',''))
	
	#get all the individual entries in the Stat table that are connected to this StatName
	all_stats= Stat.all().filter('StatName = ', stat_name)
	all_stats1 = all_stats.fetch(limit=300)
	if len(all_stats1) > 0:
		for stat in all_stats1:
			stat.delete()
	stat_name.delete()
	#this subtracts one from the count in UserStat
	Delete_UserStat('Stats')
	
	if request.GET.get('multi','')=='1':
		#return render_to_response('event_detail.html',{'user': users.get_current_user(), 'authenticated':'yes', 'key': stat_name.event, 'addstats':1})
		return HttpResponsePermanentRedirect('/multisession-ratio/'+str(stat_name.ParentEvent.key())+'/')
	else:
		return HttpResponsePermanentRedirect('/event/'+str(stat_name.event.key())+'/')
		
####Function for deleting address

def delete_address(request, address_key):
	#get the address
	if request.GET.get('event','') == 'event':
		event = Input.get(address_key)
		address = EventAddress.get(event.Address.key())
		event.Address = None
		event.put()
		address.delete()
		return HttpResponsePermanentRedirect('/event/'+str(event.key())+'/')	
	elif request.GET.get('event','') == 'multi_event':
		event = ParentEvent.get(address_key)
		address = EventAddress.get(event.Address.key())
		event.Address = None
		event.put()
		address.delete()
		return HttpResponsePermanentRedirect('/multisession-event/'+str(event.key())+'/')

	
#### output ------------------------


#Update Twitter

#def update_twitter(status_update):
	#consumer_secret ='consumer_secret'
	#consumer_key ='consumer_key'
	#consumer_token ='consumer_token' 
	#consumer_token_secret='consumer_token_secret'

	
	
	#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	#auth.set_access_token(consumer_token, consumer_token_secret)
	#api = tweepy.API(auth)
	#api.update_status(status_update)

#### URL shortener function
def URLshorten(url):
		apikey='R_56b14128f016b9ee3e1503e9211bcab9'
		login='annina'
		request = "http://api.bit.ly/shorten?version=2.0.1&longUrl="
		request += url
		request += "&login=" + login + "&apiKey=" + apikey

		result = urlfetch.fetch(request)
		json = simplejson.loads(result.content)
		shortURL= json['results'][url]['shortUrl']
		return shortURL




 #### This creates the RSS feed	     
def feed(request):
	object_list =Input.all().order('-up_date')[:10]

	link = u'http://b-counted.appspot.com'
	feed = Rss201rev2Feed( u"Be counted! - A Survey of the Gender Distribution at Tech Events", link,
		u'The 10 most recently updated events'  )
	for object in object_list:
		#get the ratios from the database and the stats.
		ra = Ratio.all().filter('Input =',object)
		ra = ra.fetch(limit=300)
		if object.Parent !=  None:
			p = object.Parent.get_absolute_url()
			p_name = object.Parent.Name.encode('utf-8')
			
			Rss_string = 'Event title: '+object.Event.encode('utf-8')+'<br/>This event <a href="'+p+'">is part of the multi-session event '+p_name+'</a><br/>This event has <a href="'+object.get_absolute_url()+'">'+str(len(ra))+' gender ratio report(s)</a> '
		else:
			Rss_string= 'Event title: '+object.Event.encode('utf-8')+'<br/>This event has <a href="'+object.get_absolute_url()+'">'+str(len(ra))+' gender ratio report(s)</a> '
		
		sta = StatName.all().filter('event =', object)
		sta = sta.fetch(limit=300)
		if len(sta)>0:
			Rss_string+='and '+str(len(sta))+' related set(s) of statistics  <br />'
		if object.Event_URL != None:	
			Rss_string+='<br/>Event URL: <a href="'+str(object.Event_URL)+'">'+str(object.Event_URL).encode('utf-8')+'</a>'
	
		Rss_string+='<br/>Published: '+ str(object.pub_date).encode('utf-8')
	
		if object.pub_date == object.up_date:
			Rss_string+='This item has not been updated since it was published'
		else:
			Rss_string+='<br/>Last updated: '+ str(object.pub_date).encode('utf-8')
		
		feed.add_item(object.Event.encode('utf-8'), 'http://b-counted.appspot.com'+str(object.get_absolute_url()), Rss_string, pubdate=object.pub_date)
			
	response = HttpResponse(mimetype='application/xml')
	feed.write(response, 'utf-8')
	return response


####like the feed, it displays the ten most recently updated events.
def recently_updated(request):
	events =Input.all().order('-up_date')[:10]
	
	zo = []
	for x in events:
		stats_in = StatName.all().filter("event =", x)
		stats_in = stats_in.fetch(limit=300)
		
		
		yo = []
		yo.append(x)
		women = 0 
		men = 0
		other = 0
		ratio = Ratio.all().filter('Input = ', x)
		ratio = ratio.fetch(limit = 100)
		i=0
		for r in ratio:
		
			women += r.Women
			men +=r.Men
			other += r.Other
			i = i+1
		if women != 0:
			women = (women / i)
		if men !=0:
			men = (men /i)
		if other != 0:
			other = (other /i)
		
		yo.append(str(women)+' women, '+str(men)+' men , and '+str(other)+' other. <br/><span class="smalltxt"> Counting '+str.lower(str(r.WhatRatio))+ '</span><br />')
		#yo.append(stats_in)
		zo.append(yo)
			
	
	
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	return render_to_response('event_recent.html',{ 'zo': zo, 'yo':yo, 'events': events, 'user': users.get_current_user(), 'authenticated':yes_no})


#### This shows the static pages like the faq the "why" page, etc. ------------------------

def why(request):	
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	return render_to_response('why.html',{'user': users.get_current_user(), 'authenticated':yes_no})

def faq(request):	

	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	return render_to_response('faq.html',{'user': users.get_current_user(), 'authenticated':yes_no})
	
	
def ac(request):
	all_events = Input.all().order('-pub_date')
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	return render_to_response('event_all.html',{'all_events': all_events, 'user': users.get_current_user(), 'authenticated':yes_no})
	
def about(request):	
	if users.get_current_user():
		yes_no = 'yes'
	else:
		yes_no = 'no'
	return render_to_response('about.html',{'user': users.get_current_user(), 'authenticated':yes_no})
