import nltk



if __name__=="__main__":
	rawtext = open("tester.txt").read() 
	sentences = nltk.sent_tokenize("Mr. and Mrs. Dursley with their father Harry Potter") # NLTK default sentence segmenter 
	sentences = [nltk.word_tokenize(sent) for sent in sentences] # NLTK word tokenizer 
	sentences = [nltk.pos_tag(sent) for sent in sentences] # NLTK POS tagger
	grammar = """ 
 		NP:	{<NNP>+} 
 		REL: {<NN>} 
		"""

# 	grammar = """
# 		//  pattern set for noun and verb groups
# 
# pattern set chunks;
# 
# //  patterns for noun groups
# 
# ng := 		det-pos? <JJ>* <NN> |
# 		proper-noun |
# 		[constit cat=pro];
# 
# det-pos	    :=	[constit cat=det] |
# 		[constit cat=det]? [constit cat=n number=singular] "'s";
# 
# proper-noun :=	[ENAMEX] ;
# 
# when ng        add [ngroup];
# 
# //  patterns for active verb groups
# 
# vg :=		[constit cat=tv] |
# 		[constit cat=w] vg-inf |
# 		tv-vbe vg-ving;
# 
# vg-inf :=	[constit cat=v] |
# 		"be" vg-ving;
# 
# vg-ven :=	[constit cat=ven] |
# 		"been" vg-ving;
# 
# vg-ving :=	[constit cat=ving];
# 
# tv-vbe :=	"is" | "are" | "was" | "were";
# 
# when vg		add [constit cat=vgroup];
# 
# //  patterns for passive verb groups
# 
# vg-pass :=	tv-vbe [constit cat=ven] |
# 		[constit cat=w] "be" [constit cat=ven];
# 
# when vg-pass	add [constit cat=vgroup-pass];
# 
# //  pattern for infinitival verb groups
# 
# to-vg :=	vg-inf;	
# 	"""
# 	cp = nltk.parse_cfg(grammar)
# 	parser = nltk.ChartParser(cp)
# 	result=parser.nbest_parse(sentences[0])

	cp = nltk.RegexpParser(grammar)
	chunked = cp.parse(sentences[0])
	for n in chunked:
		if isinstance(n,nltk.tree.Tree):
			if n.node == 'REL':
				print n