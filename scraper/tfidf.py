import sys, re, collections, math
from nltk.corpus import stopwords
from nltk.stem import *
from bs4 import BeautifulSoup
from unidecode import unidecode

words = []

#stems words

def stem_words(words):
	output = []
	stemmer = SnowballStemmer("english")

	for word in words:
		temp = stemmer.stem(word)
		output.append(temp)
        
	return output

#makes sure every document in words is shared across all words
def make_hit_list() :
	#if only one query do nothing
	if len(words) <= 1 :
		return
	#remove documents not in first word from other documents
	for word in words[1:] :
		for doc, freq in word.documents.iteritems() :
			if doc not in words[0].documents.iterkeys() :
				word.documents.pop(doc, None)

	#remove documents not in cleaned other words from word 1
	for doc, freq in words[0].documents.iteritems() :
		if doc not in words[1].documents.iterkeys() :
			words[0].documents.pop(doc, None)

class Word() :
	def __init__(self,array) :
		self.word = array[0]
		self.document_string = array[1]
		self.documents = self.extract_documents()


	def extract_documents(self):
		documents = {}
		doc = re.findall('\w*\.html', self.document_string)
		freq = re.findall('\s\d{1}\s',self.document_string)
		for i in range(len(doc)) :
			documents[doc[i]] = freq[i]

		return documents




if __name__ == '__main__':
    try:
        del sys.argv[0] # Delete the file name from the args
        # word_list = stem_words(sys.argv)
        word_list = stem_words(["not", "feedback"])
    except IndexError:
        raise ValueError ("Please specify a file in the command arg, like: 'python index.py directory/ index.dat'")

    try:
        
        file = 'invindex.dat'
        total_documents = 0
        with open(file) as doc:
            for line in doc:
                temp = line.split(" documents: ")
                if temp[0] in word_list:
                	word = Word(temp)
                	words.append(word)
        make_hit_list()

    except IOError as e:
        raise IOError("Please enter a correct file. Python says: '" + str(e)+"'")