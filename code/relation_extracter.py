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
		familypattern = re.compile("<Man ([A-Z][a-z]+)>.* begat .*<Man ([A-Z][a-z]+)>.* of <Woman ([A-Z][a-z]+)>")

		foundFamilyPattern = re.findall(familypattern, sent)
		for match in foundFamilyPattern:
			father = match[0]
			child = match[1]
			mother =match[2]
			self.write("%s is the father of %s"%(father,child))
			self.write("%s is the mother of %s"%(mother,child))

	def recursivePattern(self,sent,tagNames):
		recpattern = re.compile(".* <Man>[A-Z][a-z].* the son of <Man>[A-Z][a-z] (which|Which was the son of <Man>[A-Z][a-z])*.*")
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
	rawtext = """3:23 And Jesus himself began to be about thirty years of age, being
(as was supposed) the son of Joseph, which was the son of Heli, 3:24
Which was the son of Matthat, which was the son of Levi, which was the
son of Melchi, which was the son of Janna, which was the son of
Joseph, 3:25 Which was the son of Mattathias, which was the son of
Amos, which was the son of Naum, which was the son of Esli, which was
the son of Nagge, 3:26 Which was the son of Maath, which was the son
of Mattathias, which was the son of Semei, which was the son of
Joseph, which was the son of Juda, 3:27 Which was the son of Joanna,
which was the son of Rhesa, which was the son of Zorobabel, which was
the son of Salathiel, which was the son of Neri, 3:28 Which was the
son of Melchi, which was the son of Addi, which was the son of Cosam,
which was the son of Elmodam, which was the son of Er, 3:29 Which was
the son of Jose, which was the son of Eliezer, which was the son of
Jorim, which was the son of Matthat, which was the son of Levi, 3:30
Which was the son of Simeon, which was the son of Juda, which was the
son of Joseph, which was the son of Jonan, which was the son of
Eliakim, 3:31 Which was the son of Melea, which was the son of Menan,
which was the son of Mattatha, which was the son of Nathan, which was
the son of David, 3:32 Which was the son of Jesse, which was the son
of Obed, which was the son of Booz, which was the son of Salmon, which
was the son of Naasson, 3:33 Which was the son of Aminadab, which was
the son of Aram, which was the son of Esrom, which was the son of
Phares, which was the son of Juda, 3:34 Which was the son of Jacob,
which was the son of Isaac, which was the son of Abraham, which was
the son of Thara, which was the son of Nachor, 3:35 Which was the son
of Saruch, which was the son of Ragau, which was the son of Phalec,
which was the son of Heber, which was the son of Sala, 3:36 Which was
the son of Cainan, which was the son of Arphaxad, which was the son of
Sem, which was the son of Noe, which was the son of Lamech, 3:37 Which
was the son of Mathusala, which was the son of Enoch, which was the
son of Jared, which was the son of Maleleel, which was the son of
Cainan, 3:38 Which was the son of Enos, which was the son of Seth,
which was the son of Adam, which was the son of God."""
# 	rawtext = open("trainer.txt").read() 
 	#rawtext= "40:001:002 Abraham begat Isaac; and Isaac begat Jacob; and Jacob begat Judas and Park of Ruth;"
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
	catches= [ x for x in b.catches if x not in seen and not seen_add(x)]
	with open ("results2.txt","w") as r:
		for c in catches:
			print c
			r.write("%s\n"%c)
		
	
	