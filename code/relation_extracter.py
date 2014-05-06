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
		smc=""
		for index,word in enumerate(words):
			if ":" in word:
				smc = ":"	
			word=word.split(":")[0]
			if word in self.malenames[word[0]]:
				words[index] = "<Man %s>%s"%(word,smc)
				tagNames.append(word)
			elif word in self.femalenames[word[0]]:
				words[index] = "<Woman %s>%s"%(word,smc)
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
		twopattern = re.compile("<Man ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)>.* and <Man ([A-Z][a-z]+)>")
		foundtwoPattern = re.findall(twopattern, sent)
		threepattern = re.compile("<Man ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)> <Man ([A-Z][a-z]+)> and <Man ([A-Z][a-z]+)>")
		foundthreePattern = re.findall(threepattern, sent)
		for match in foundtwoPattern:
			self.write("%s is the father of %s"%(match[0],match[1]))
			self.write("%s is the father of %s"%(match[0],match[2]))
		for match in foundthreePattern:
			self.write("%s is the father of %s"%(match[0],match[1]))
			self.write("%s is the father of %s"%(match[0],match[2]))
			self.write("%s is the father of %s"%(match[0],match[3]))	
	
	
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

		wifepattern = re.compile("<Man ([A-Z][a-z]+)>.+ <Woman ([A-Z][a-z]+)> his wife")
		foundWifePattern = re.findall(wifepattern, sent)
		for match in foundWifePattern:
			self.write("%s is the wife of %s"%(match[1], match[0]))

		wifepattern = re.compile("<Man ([A-Z][a-z]+)>.+ wives.* <Woman ([A-Z][a-z]+)> and <Woman ([A-Z][a-z]+)>")
		foundWifePattern = re.findall(wifepattern, sent)
		for match in foundWifePattern:
			self.write("%s is the wife of %s"%(match[1], match[0]))
			self.write("%s is the wife of %s"%(match[2], match[0]))
	
	def sonofPattern(self,sent):
		sonpattern = re.compile("<Man ([A-Z][a-z]+)> the? son of <Man ([A-Z][a-z]+)>")
		foundson = re.findall(sonpattern,sent)
		for match in foundson:
			self.write("%s is the father of %s"%(match[1],match[0]))
	
	def daughterofPattern(self,sent):
		daughterpattern = re.compile("<Woman ([A-Z][a-z]+)> the? daughter of <Man ([A-Z][a-z]+)>")
		founddaughter = re.findall(daughterpattern,sent)
		for match in founddaughter:
			print sent
			self.write("%s is the father of %s"%(match[1],match[0]))
	
	def barePattern(self,sent):
		#Error???
		barePattern1 = re.compile("<Woman ([A-Z][a-z]+)> bare to <Man ([A-Z][a-z]+)> <Man ([A-Z][a-z]+)>")
		foundBare = re.findall(barePattern1,sent)
		for match in foundBare:
			self.write("%s is the mother of %s"%(match[0],match[1]))
	
	def becamefatherPattern(self,sent):
		sp = re.compile(".*<Man ([A-Z][a-z]+)> .* begat a? son? <Man ([A-Z][a-z]+)>")
		spm = re.findall(sp,sent)
		print sent
		for match in spm:
			self.write("%s is the father of %s"%(match[0],match[1]))

	def brotherofPattern(self, sent):
		brotherPattern = re.compile("<Man ([A-Z][a-z]+)>.+ <Man ([A-Z][a-z]+)> his brother")
		foundbrother = re.findall(brotherPattern,sent)
		for match in foundbrother:
			self.write("%s is the brother of %s"%(match[0], match[1]))

	def sisterofPattern(self, sent):
		sisterPattern = re.compile("sister of <Man ([A-Z][a-z]+)> was <Woman ([A-Z][a-z]+)>")
		foundsister = re.findall(sisterPattern,sent)
		for match in foundsister:
			self.write("%s is the sister of %s"%(match[1], match[0]))

	def fatherofPattern(self, sent):
		fatherPattern = re.compile("<Man ([A-Z][a-z]+)> knew .*bare.* name? <Man ([A-Z][a-z]+)>")
		foundfather = re.findall(fatherPattern,sent)
		for match in foundfather:
			self.write("%s is the father of %s"%(match[0], match[1]))

		fatherPattern = re.compile("unto <Man ([A-Z][a-z]+)> was born <Man ([A-Z][a-z]+)>")
		foundfather = re.findall(fatherPattern,sent)
		for match in foundfather:
			self.write("%s is the father of %s"%(match[0], match[1]))

		fatherPattern = re.compile("to <Man ([A-Z][a-z]+)>.* was born.* name? <Man ([A-Z][a-z]+)>")
		foundfather = re.findall(fatherPattern,sent)
		for match in foundfather:
			self.write("%s is the father of %s"%(match[0], match[1]))

	def motherofPattern(self, sent):
		motherPattern = re.compile("<Woman ([A-Z][a-z]+)>.* bare <Man ([A-Z][a-z]+)>")
		foundmother = re.findall(motherPattern,sent)
		for match in foundmother:
			self.write("%s is the mother of %s"%(match[0],match[1]))

		
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

def testing(catches,fname):
	corrects = set()
	numCorrect = 0
	with open(fname, 'r') as correctFile:
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
	
if __name__=="__main__":

	b = extractBible()
	b.readMaleNames()
	b.readFemaleNames()
	

	rawtext = open("trainer.txt").read()
	#sentences = rawtext.replace(";",".")
	sentences = rawtext.replace(":", "")
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
		b.becamefatherPattern(sent)
		b.brotherofPattern(sent)
		b.fatherofPattern(sent)
		b.motherofPattern(sent)
		b.sisterofPattern(sent)
		
	seen = set()
	seen_add = seen.add
	catches= [ x for x in b.catches if x not in seen and not seen_add(x)]
	for c in catches:
		print c
	testing(catches,"correct3.txt")
# 	#with open ("results2.txt","w") as r:
# 	for c in catches:
# 		print c
# 			#r.write("%s\n"%c)
# 		
	
	