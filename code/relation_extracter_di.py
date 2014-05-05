
from __future__ import division
import nltk
import collections
import re

class extractBible:
	def __init__(self):
		self.malenames=collections.defaultdict(list)
		self.femalenames=collections.defaultdict(list)
		self.catches = []
	
	def readMaleNames(self):
		with open('menNames.txt') as m:
			for l in m:
				self.malenames[l[0]].append(l.strip())
	
	def readFemaleNames(self):
		with open('womenNames.txt') as m:
			for l in m:
				self.femalenames[l[0]].append(l.strip())
	
	def namePattern(self,sent):
		sent = sent.replace(",","")
		words = sent.split()
		tagNames = []
		for index,word in enumerate(words):
			if word in self.malenames[word[0]]:
				words[index] = "<Man %s>"%word
				tagNames.append(word)
			elif word in self.femalenames[word[0]]:
				words[index] = "<Woman %s>"%word
				tagNames.append(word)
		sent = " ".join(words)
		return sent,tagNames
	
	def begatPattern(self,sent):
# 		Father pattern catches David the king type
		fatherpattern = re.compile("<Man ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)>")
		motherpattern = re.compile("<Woman ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)>")

		foundFatherPattern = re.findall(fatherpattern, sent)
		for match in foundFatherPattern:
			father = match[0]
			child = match[1]
			self.write("%s is the father of %s"%(father,child))
	
		foundMotherPattern = re.findall(motherpattern, sent)	
		for match in foundMotherPattern:
			mother = match[0]
			child = match[1]	
			self.write("%s is the mother of %s"%(mother,child))			
			
	def begatOfPattern(self,sent):
		familypattern = re.compile("<Man ([A-Z][a-z]+)>.* begat.*<Man ([A-Z][a-z]+)>.* of <Woman ([A-Z][a-z]+)>")

		foundFamilyPattern = re.findall(familypattern, sent)
		for match in foundFamilyPattern:
			father = match[0]
			child = match[1]
			mother =match[2]
			self.write("%s is the father of %s"%(father,child))
			self.write("%s is the mother of %s"%(mother,child))

	def recursivePattern(self,sent,tagNames):

		recpattern = re.compile(".* <Man ([A-Z][a-z]+)>.* the son of <Man ([A-Z][a-z]+)>.* (which|Which was the son of <Man ([A-Z][a-z]+)>.*)*.*")
		if recpattern.match(sent):
			j=1
			for i in xrange(len(tagNames)-1):
				father = tagNames[j]
				child = tagNames[i]
				self.write("%s is the father of %s"%(father,child))
				j=j+1
		
	def begatManyPattern(self,sent):
		manypattern = re.compile("<Man ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)>.* and <Man ([A-Z][a-z]+)>")

		foundManyPattern = re.findall(manypattern, sent)
		for match in foundManyPattern:
			self.write("%s is the father of %s"%(match[0],match[1]))
			self.write("%s is the father of %s"%(match[0],match[2]))
				
	def write(self,text):
# 		print text
		self.catches.append(text)	

def cleanClause(sent):
	nopattern = re.compile("[1-9][0-9]*:[1-9][0-9]")
	words = sent.split()
	for index,word in enumerate(words):
		word = word.strip()
		word = word.strip('\t')
		if nopattern.match(word):
			words[index] = ""
	sentence = " ".join(words)
	return sentence

if __name__=="__main__":

	b = extractBible()
	b.readMaleNames()
	b.readFemaleNames()
 	rawtext = open("trainer.txt").read() 
 	#rawtext= "40:001:011 And Josias begat Jechonias and his brethren about the time they were carried away to Babylon; 40:001:012 And after they were brought to Babylon Jechonias begat Salathiel"
	sentences = rawtext.replace(";",".")
	clauses= sentences.split(".")
	for sent in clauses:
		sent = cleanClause(sent)
		sent,tagNames = b.namePattern(sent)
		b.begatOfPattern(sent)
		b.begatManyPattern(sent)
		b.begatPattern(sent)
		b.recursivePattern(sent, tagNames)
	seen = set()
	seen_add = seen.add
	catches = [ x for x in b.catches if x not in seen and not seen_add(x)]
	#with open ("results.txt","w") as r:
	#	for c in catches:
	#		#print c
	#		r.write("%s\n"%c)
	corrects = []
	numCorrect = 0
	with open("correct.txt", 'r') as correctFile:
		for c in correctFile:
			corrects.append(c.strip("\n"))

	print "*****[Relations Missed]****"
	for correct in corrects:
		if correct not in catches:
			print correct

	print "***[Incorrect Relations]***"
	for catch in catches:
		if catch not in corrects:
			print catch
		else:
			numCorrect+=1

	numInKey = len(corrects)
	numInResponse = len(catches)

	precision = numCorrect/numInResponse
	recall = numCorrect/numInKey 
	fmeasure = 2/(1/recall + 1/precision)
	print "***[Evaluation Summary]***"
	print "Precision\t" + str(precision)
	print "Recall\t\t" + str(recall)
	print "fmeasure\t" + str(fmeasure)

	
	
	