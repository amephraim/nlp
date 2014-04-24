
from nltk.corpus import PlaintextCorpusReader

load_file(fname):
	corpus_root='project_jet_files'
	wordlists = PlaintextCorpusReader(corpus_root,'.*')

