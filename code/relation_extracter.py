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
		words = sent.split()
		tagNames = []
		for word in words:
			if word in self.malenames[word[0]]:
				sent = sent.replace(word,"<Man>%s"%word)
				tagNames.append(word)
			elif word in self.femalenames[word[0]]:
				sent = sent.replace(word,"<Woman>%s"%word)
				tagNames.append(word)
		return sent,tagNames
	
	def begatPattern(self,sent,tagNames):
		print sent
# 		Father pattern catches David the king type
		fatherpattern = re.compile(".*<Man>[A-Z][a-z]+.* begat <Man>[A-Z][a-z].*")
		motherpattern = re.compile(".*<Woman>[A-Z][a-z]+ begat <Man>[A-Z][a-z].*")
		if fatherpattern.match(sent):
			father = tagNames[0]
			child = tagNames[1]
			self.write("%s is the father of %s"%(father,child))
						
		elif motherpattern.match(sent):
			mother = tagNames[0]
			child = tagNames[1]
			self.write("%s is the mother of %s"%(mother,child))
			
	def begatOfPattern(self,sent,tagNames):
		familypattern = re.compile(".* <Man>[A-Z][a-z]+ begat <Man>[A-Z][a-z]+ of <Woman>[A-Z][a-z].*")
		if familypattern.match(sent):
			father = tagNames[0]
			child = tagNames[1]
			mother = tagNames[2]
			self.write("%s is the father of %s"%(father,child))
			self.write("%s is the mother of %s"%(mother,child))
			return True
	
	def begatManyPattern(self,sent,tagNames):
		manypattern = re.compile(".* <Man>[A-Z][a-z]+ begat <Man>[A-Z][a-z]+ and <Man>[A-Z][a-z]+.*")
		if manypattern.match(sent):
			self.write("%s is the father of %s"%(tagNames[0],tagNames[1]))
			self.write("%s is the father of %s"%(tagNames[0],tagNames[2]))
				
	def write(self,text):
# 		print text
		self.catches.append(text)	

def cleanClause(clause):
	words = clause.split()
	for word in words:
		word = word.strip()
		word = word.strip('\t')
	sentence = " ".join(words)
	return sentence

if __name__=="__main__":
	b = extractBible()
	b.readMaleNames()
	b.readFemaleNames()
# 	rawtext = "Abraham begat Issac"
	rawtext = open("trainer.txt").read() 
# 	rawtext= "40:001:002 Abraham begat Isaac; and Isaac begat Jacob; and Jacob begat Judas and his brethren;"
	sentences = rawtext.replace(",",".").replace(";",".")
	clauses= sentences.split(".")
	for sent in clauses:
		sent = cleanClause(sent)
		sent,tagNames = b.namePattern(sent)
		b.begatOfPattern(sent,tagNames)
		b.begatManyPattern(sent,tagNames)
		b.begatPattern(sent,tagNames)
	seen = set()
	seen_add = seen.add
	catches= [ x for x in b.catches if x not in seen and not seen_add(x)]
	with open ("results2.txt","w") as r:
		for c in catches:
			print c
			r.write("%s\n"%c)
		
	
	