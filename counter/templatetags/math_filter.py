
from django.template import *
from django.template import Node
from django.template import Library
from django.conf import settings

register = Library()

def mult(value, arg):
	"Multiplies the arg and the value"
	return int(value) * int(arg)
	mult.is_safe = False 
def sub(value, arg):
	"Subtracts the arg from the value"
	return int(value) - int(arg)
sub.is_safe = False 
def div(value, arg):
	"Divides the value by the arg"
	return int(value) / int(arg)
div.is_safe = False 


def add_three(token1,token2, token3):
	return str(token1+token2+token3)

def percentage_design(token1,token2, token3):
	if token1 != '0':
		sum = float(token1) + float(token2) + float(token3)
		per = float(token1)
		percent = int((per/sum)*350)
	else:
		percent = 0
	
	
	return str(percent)
	
def percentage(token1,token2, token3):
	if token1 != '0':
		sum = float(token1) + float(token2) + float(token3)
		per = float(token1)
		percent = (per/sum)*100
		percent = round(percent,2)
		
	else:
		percent = 0
	
	
	return str(percent)

def encode(token1):
	token = token.encode('iso-8859-1')
	return token
	
	


def ave(token):
	women = 0
	men = 0
	other =0
	count = 0
	for t in token:
		women += t.Women
		men += t.Men
		other += t.Other
		count += 1
	women = float(women)/ float(count)
	men = float(men)/float(count)
	other= float(other)/float(count)
	return str(women)+' women, '+str(men)+' men, '+str(other)+' other.'
	
	
register.simple_tag(add_three)
register.simple_tag(percentage)
register.simple_tag(percentage_design)
register.simple_tag(ave)
register.simple_tag(encode)



register.filter(mult)
register.filter(sub)
register.filter(div)



