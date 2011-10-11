from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.api.users import User
import datetime


#this stores all addresses
class EventAddress(db.Model):
	Street=db.StringProperty()
	City=db.StringProperty()
	State=db.StringProperty()
	Zip = db.StringProperty()
	Country=db.StringProperty()
	latitude = db.FloatProperty()
	longitude = db.FloatProperty()	
	created_by = db.UserProperty()
	def __str__(self):
		return self.EventAddress
	
	def __str__(self):
		return '%s' %self.Contributor

#this stores multisession event names etc.
class ParentEvent(db.Model):
	Address=db.ReferenceProperty(EventAddress)
	Name = db.StringProperty()
	NumEvents = db.IntegerProperty()
	Event_URL = db.StringProperty() 
	pub_date = db.DateTimeProperty()
	up_date = db.DateTimeProperty()
	created_by = db.UserProperty()
	
	
	def __str__(self):
		return self.ParentEvent
	class Meta:
		ordering = ('-pub_date')
		get_latest_by = 'pub_date'
		
	def __str__(self):
		return self.Name
		
	def get_absolute_url(self):
		return '/multisession-event/%s/' % self.key()

#this stores single events or sessions connected to a multi-session event (stored above)
class Input(db.Model):
	Multi = db.BooleanProperty()
	Parent = db.ReferenceProperty(ParentEvent)
	Event = db.StringProperty()
	Event_URL = db.StringProperty() 
	Address= db.ReferenceProperty(EventAddress)
	pub_date = db.DateTimeProperty()
	up_date = db.DateTimeProperty()
	created_by = db.UserProperty()
	#EventDay=db.DateProperty(default=datetime.date.isoformat(datetime.date.today()))
	EventDay=db.DateProperty()

	def __str__(self):
		return self.Event
		
	def get_absolute_url(self):
		return '/event/%s/' % self.key()

#gender distribution is stored here.

class Ratio(db.Model):
	Input= db.ReferenceProperty(Input)
	ParentEvent=db.ReferenceProperty(ParentEvent)
	WhatRatio = db.StringProperty(default='Everyone present: Audience, speakers/panelists, organizers, etc.')
	Men = db.IntegerProperty(default=0)
	Other = db.IntegerProperty(default=0)
	Women= db.IntegerProperty(default=0)
	pub_date = db.DateTimeProperty()
	ShortDescription=db.TextProperty(default='No description')
	created_by = db.UserProperty()
	
	def __str__(self):
		return self.Event

#if users want to add more stats to an event/session		
class StatName(db.Model):
	event = db.ReferenceProperty(Input)
	ParentEvent = db.ReferenceProperty(ParentEvent)
	name = db.StringProperty()
	created_on = db.DateTimeProperty(auto_now_add = 1)
	created_by = db.UserProperty()
	def __str__(self):
		return '%s' %self.name
		
	def get_absolute_url(self):
		return '/stat/%s/' % self.key()

#stats regarding contributors
class UserStat(db.Model):
	Contributor= db.UserProperty()
	Gender=db.StringProperty()
	Stats=db.IntegerProperty(default=0)
	Ratios=db.IntegerProperty(default=0)
	Events =db.IntegerProperty(default=0)
	Multi_Events = db.IntegerProperty(default=0)
	
	

#since the stats are flexible, this is the stat added
class Stat(db.Model):
    StatName = db.ReferenceProperty(StatName)
    stat = db.StringProperty()
    num = db.IntegerProperty(default = 0)
    
    def __str__(self):
        return '%s' %self.stat




    
  
	
    
    
		