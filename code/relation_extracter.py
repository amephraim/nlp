import nltk



if __name__=="__main__":
	rawtext = open("tester.txt").read() 
	sentences = nltk.sent_tokenize(rawtext) # NLTK default sentence segmenter 
	sentences = [nltk.word_tokenize(sent) for sent in sentences] # NLTK word tokenizer 
	sentences = [nltk.pos_tag(sent) for sent in sentences] # NLTK POS tagger
	print "ok"