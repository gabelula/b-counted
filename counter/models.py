from django.db import models
from django.contrib.auth.models import User

# Stores all addresses
class EventAddress(models.Model):
  street     = models.CharField(max_length=10)
  city       = models.CharField(max_length=10)
  state      = models.CharField(max_length=10)
  zip_code   = models.CharField(max_length=5)
  country    = models.CharField(max_length=15)
  latitude   = models.FloatField()
  longitude  = models.FloatField()
  created_by = models.ForeignKey(User)

  def __unicode__(self):
    return self.EventAddress

  def __unicode__(self):
    return '%s' % self.Contributor

# Stores multisession event names (conferences)
class ParentEvent(models.Model):
  address    = models.ForeignKey(EventAddress)
  name       = models.CharField(max_length=30)
  num_events = models.IntegerField()
  event_URL  = models.URLField() 
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
class Event(models.Model): # it used to be called Input
  multi      = models.BooleanField()
  parent     = models.ForeignKey(ParentEvent)
  event      = models.CharField(max_length=30)
  event_URL  = models.URLField()
  address    = models.ForeignKey(EventAddress)
  pub_date   = models.DateField()
  up_date    = models.DateField()
  created_by = models.ForeignKey(User)
  eventDay   = models.DateField()

  def __unicode__(self):
    return self.Event

  def get_absolute_url(self):
    return '/event/%s/' % self.key()

# Gender distribution is stored here.
class Ratio(models.Model):
  input             = models.ForeignKey(Input)
  parent_event      = models.ForeignKey(ParentEvent)
  what_ratio        = models.CharField(max_length=15, default='Everyone present: Audience, speakers/panelists, organizers, etc.')
  men               = models.IntegerField(default=0)
  other             = models.IntegerField(default=0)
  women             = models.IntegerField(default=0)
  pub_date          = models.DateField()
  short_description = models.TextField(default='No description')
  created_by        = models.ForeignKey(User)

  def __unicode__(self):
    return self.Event

# If users want to add more stats to an event/session  
class StatName(models.Model):
  event        = models.ForeignKey(Input)
  parent_event = models.ForeignKey(ParentEvent)
  name         = models.CharField(max_length=30)
  created_on   = models.DateField(auto_now_add = 1)
  created_by   = models.ForeignKey(User)

  def __unicode__(self):
    return '%s' %self.name

  def get_absolute_url(self):
    return '/stat/%s/' % self.key()

# Stats regarding contributors
class UserStat(models.Model):
  contributor  = models.ForeignKey(User, unique=True)
  gender       = models.CharField(max_length=10)
  stats        = models.IntegerField(default=0)
  ratios       = models.IntegerField(default=0)
  events       = models.IntegerField(default=0)
  multi_events = models.IntegerField(default=0)

  def is_contributor():
    pass

# Since the stats are flexible, this is the stat added
class Stat(models.Model):
  stat_name = models.ForeignKey(StatName)
  stat     = models.CharField(max_length=10)
  num      = models.IntegerField(default = 0)

  def __unicode__(self):
    return '%s' %self.stat
