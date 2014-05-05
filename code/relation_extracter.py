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
		for word in words:
			if word in self.malenames[word[0]]:
				sent = sent.replace(word,"<Man %s>"%word)
			elif word in self.femalenames[word[0]]:
				sent = sent.replace(word,"<Woman %s>"%word)
		return sent
	
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
		familypattern = re.compile("<Man ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)>.* of <Woman ([A-Z][a-z]+)>")

		foundFamilyPattern = re.findall(familypattern, sent)
		for match in foundFamilyPattern:
			father = match[0]
			child = match[1]
			mother =match[2]
			self.write("%s is the father of %s"%(father,child))
			self.write("%s is the mother of %s"%(mother,child))
	
	def begatManyPattern(self,sent):
		manypattern = re.compile("<Man ([A-Z][a-z]+)>.* begat <Man ([A-Z][a-z]+)>.* and <Man ([A-Z][a-z]+)>")

		foundManyPattern = re.findall(manypattern, sent)
		for match in foundManyPattern:
			self.write("%s is the father of %s"%(match[0],match[1]))
			self.write("%s is the father of %s"%(match[0],match[2]))
				
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
	#rawtext = "Abraham begat Issac"
	rawtext = open("trainer.txt").read() 
 	#rawtext= "40:001:002 Abraham begat Isaac; and Isaac begat Jacob; and Jacob begat Judas and Park of Ruth;"
	sentences = rawtext.replace(";",".")
	clauses= sentences.split(".")
	for sent in clauses:
		sent = cleanClause(sent)
		sent = b.namePattern(sent)
		b.begatOfPattern(sent)
		b.begatManyPattern(sent)
		b.begatPattern(sent)
	seen = set()
	seen_add = seen.add
	catches= [ x for x in b.catches if x not in seen and not seen_add(x)]
	with open ("results2.txt","w") as r:
		for c in catches:
			print c
			r.write("%s\n"%c)
		
	
	