from django.db import models
from django.contrib.auth.models import User

# Stores all addresses
class EventAddress(models.Model):
	Street  = models.CharField(max_length=10)
	City    = models.CharField(max_length=10)
	State   = models.CharField(max_length=10)
	Zip     = models.CharField(max_length=5)
	Country = models.CharField(max_length=15)
	latitude   = models.FloatField()
	longitude  = models.FloatField()
	created_by = models.ForeignKey(User)

	def __unicode__(self):
	  return self.EventAddress

	def __unicode__(self):
	  return '%s' % self.Contributor

# Stores multisession event names (conferences)
class ParentEvent(models.Model):
	Address    = models.ForeignKey(EventAddress)
	Name       = models.CharField(max_length=30)
	NumEvents  = models.IntegerField()
	Event_URL  = models.URLField() 
	pub_date   = models.DateField()
	up_date    = models.DateField()
	created_by = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.ParentEvent

	class Meta:
		get_latest_by = 'pub_date'
		
	def __unicode__(self):
		return self.Name
		
	def get_absolute_url(self):
		return '/multisession-event/%s/' % self.key()

# Stores single events or sessions connected to a multi-session event (stored above)
class Input(models.Model):
	Multi      = models.BooleanField()
	Parent     = models.ForeignKey(ParentEvent)
	Event      = models.CharField(max_length=30)
	Event_URL  = models.URLField()
	Address    = models.ForeignKey(EventAddress)
	pub_date   = models.DateField()
	up_date    = models.DateField()
	created_by = models.ForeignKey(User)
	EventDay   = models.DateField()

	def __unicode__(self):
		return self.Event
		
	def get_absolute_url(self):
		return '/event/%s/' % self.key()

# Gender distribution is stored here.
class Ratio(models.Model):
	Input       = models.ForeignKey(Input)
	ParentEvent = models.ForeignKey(ParentEvent)
	WhatRatio   = models.CharField(max_length=15, default='Everyone present: Audience, speakers/panelists, organizers, etc.')
	Men         = models.IntegerField(default=0)
	Other       = models.IntegerField(default=0)
	Women       = models.IntegerField(default=0)
	pub_date    = models.DateField()
	ShortDescription = models.TextField(default='No description')
	created_by       = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.Event

# If users want to add more stats to an event/session		
class StatName(models.Model):
	event       = models.ForeignKey(Input)
	ParentEvent = models.ForeignKey(ParentEvent)
	name        = models.CharField(max_length=30)
	created_on  = models.DateField(auto_now_add = 1)
	created_by  = models.ForeignKey(User)

	def __unicode__(self):
		return '%s' %self.name
		
	def get_absolute_url(self):
		return '/stat/%s/' % self.key()

# Stats regarding contributors
class UserStat(models.Model):
	Contributor  = models.ForeignKey(User)
	Gender       = models.CharField(max_length=10)
	Stats        = models.IntegerField(default=0)
	Ratios       = models.IntegerField(default=0)
	Events       = models.IntegerField(default=0)
	Multi_Events = models.IntegerField(default=0)

# Since the stats are flexible, this is the stat added
class Stat(models.Model):
    StatName = models.ForeignKey(StatName)
    stat     = models.CharField(max_length=10)
    num      = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return '%s' %self.stat
