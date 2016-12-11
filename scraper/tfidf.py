import sys, re, collections, math
from nltk.corpus import stopwords
from nltk.stem import *
from bs4 import BeautifulSoup
from unidecode import unidecode

words = []
documents = []
document_details = {}

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
		temp_docs = []
		for doc, freq in word.documents.iteritems() :
			if doc not in words[0].documents.iterkeys() :
				temp_docs.append(doc)
		for doc in temp_docs :
			word.documents.pop(doc, None)

	#remove documents not in cleaned other words from word 1
	for doc, freq in words[0].documents.iteritems() :
		if doc not in words[1].documents.iterkeys() :
			words[0].documents.pop(doc, None)

def get_docs_details(doc) :
	for line in doc :
		temp = line.split(" url: ")
		url = temp[1]
		temp = temp[0].split(" title: ")
		title = temp[1]
		temp = temp[0].split(" length: ")
		name = temp[0]
		size = int(temp[1])
		document = [size, title, url]
		document_details[name] = document

class Word() :
	def __init__(self,array) :
		self.word = array[0]
		self.document_string = array[1]
		self.documents = self.extract_documents()
		self.num_of_docs = len(self.documents)


	def extract_documents(self):
		documents = {}
		doc = re.findall('\w*\.html', self.document_string)
		freq = re.findall('\s\d\s',self.document_string)
		frequency = map(int, freq)
		for i in range(len(doc)) :
			documents[doc[i]] = frequency[i]

		return documents

class Document() :
	def __init__(self, name) :
		self.name = name
		self.size = None
		self.title = None
		self.url = None
		self.get_details()
		self.tf = self.compute_tf()
		self.idf = self.compute_idf()
		self.tf_idf = self.tf * self.idf
		documents.append(self)

	def get_details(self) :
		document = document_details[self.name]
		self.size = document[0]
		self.title = document[1]
		self.url = document[2]

	# occurances of words in doc / length of doc
	def compute_tf(self):
		tf = 0.0
		for word in words :
			tf += word.documents[self.name]
		return tf / self.size

	# total documents / number of documents terms appear in. Purposefully include docs outside of hitlist to get more variance for common words.
	# enables rare words to hold more weight in this computation.
	def compute_idf(self) :
		n = len(words)
		num_of_docs = 0
		for word in words :
			num_of_docs += word.num_of_docs
		if num_of_docs is 0:
			num_of_docs += 1
		return math.log(float(total_documents)/float(num_of_docs))



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
            	total_documents += 1
                temp = line.split(" documents: ")
                if temp[0] in word_list:
                	word = Word(temp)
                	words.append(word)
        make_hit_list()

        #get doc details from docs.dat for later use.
        file = 'docs.dat'
        with open(file) as doc :
        	get_docs_details(doc)
        
        #make all of the documents
        for doc in words[0].documents.iterkeys() :
        	Document(doc)


        documents.sort(key=lambda x: x.tf_idf, reverse=True)
        for doc in documents:
        	print doc.name

    except IOError as e:
        raise IOError("Please enter a correct file. Python says: '" + str(e)+"'")