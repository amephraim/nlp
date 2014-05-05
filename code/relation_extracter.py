from __future__ import division
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
		familypattern = re.compile("<Man ([A-Z][a-z]+)>.* begat .*<Man ([A-Z][a-z]+)>.* of <Woman ([A-Z][a-z]+)>")

		foundFamilyPattern = re.findall(familypattern, sent)
		for match in foundFamilyPattern:
			father = match[0]
			child = match[1]
			mother =match[2]
			self.write("%s is the father of %s"%(father,child))
			self.write("%s is the mother of %s"%(mother,child))

	def recursivePattern(self,sent,tagNames):
		print sent
# 		recpattern = re.compile(".* <Man ([A-Z][a-z]+)>.* the son of <Man ([A-Z][a-z]+)>.* (which|Which was the son of <Man ([A-Z][a-z]+)>.*)*.*")
		recpattern = re.compile(".* <Man ([A-Z][a-z]+)>.* the son of <Man ([A-Z][a-z]+)>.*( which|Which was the son of <Man ([A-Z][a-z]+)>)+")
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
			print "begatManyPattern: " 
			print match 
			self.write("%s is the father of %s"%(match[0],match[1]))
			self.write("%s is the father of %s"%(match[0],match[2]))
	
	def aposPattern(self,sent):
		pass
	
	
	def write(self,text):
# 		print text
		self.catches.append(text)	

	def espousePattern(self,sent):
		espousepattern = re.compile("<Woman ([A-Z][a-z]+)> was espoused to <Man ([A-Z][a-z]+)>")
		espousewife = re.findall(espousepattern,sent)
		for match in espousewife:
			self.write("%s is the wife of %s"%(match[0],match[1]))
		husbandpattern = re.compile("<Man ([A-Z][a-z]+)> the husband of <Woman ([A-Z][a-z]+)>")
		husbandwife = re.findall(husbandpattern,sent)
		for match in husbandwife:
			self.write("%s is the wife of %s"%(match[1],match[0]))
	
	def sonofPattern(self,sent):
		sonpattern = re.compile("<Man ([A-Z][a-z]+)> the? son of <Man ([A-Z][a-z]+)>")
		foundson = re.findall(sonpattern,sent)
		for match in foundson:
			self.write("%s is the father of %s"%(match[1],match[0]))
	
	def daughterofPattern(self,sent):
		daughterpattern = re.compile("<Woman ([A-Z][a-z]+)> the? daughter of <Man ([A-Z][a-z]+)>")
		founddaughter = re.findall(daughterpattern,sent)
		for match in founddaughter:
			self.write("%s is the father of %s"%(match[1],match[0]))
		
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
	sentences = rawtext.replace(";",".")
	clauses= sentences.split(".")
	for sent in clauses:
		sent = cleanClause(sent)
		sent,tagNames = b.namePattern(sent)
		b.begatOfPattern(sent)
		b.begatManyPattern(sent)
		b.begatPattern(sent)
		b.recursivePattern(sent, tagNames)
		b.espousePattern(sent)
		b.sonofPattern(sent)
		b.daughterofPattern(sent)
	seen = set()
	seen_add = seen.add
	catches= [ x for x in b.catches if x not in seen and not seen_add(x)]
# 	#with open ("results2.txt","w") as r:
# 	for c in catches:
# 		print c
# 			#r.write("%s\n"%c)
# 		
	corrects = set()
	numCorrect = 0
	with open("correct.txt", 'r') as correctFile:
		for c in correctFile:
			corrects.add(c.strip("\n"))

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
	