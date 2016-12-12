import sys, re, collections, math, pickle
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
		temp_docs = []
		if doc not in words[1].documents.iterkeys() :
			temp_docs.append(doc)

	for doc in temp_docs :
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
		#in case there is a discrepancy for some reason, don't go out of index range.
		for i in range(min(len(doc), len(frequency))) :
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
			if self.name in word.documents.keys() :
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

#Smaller object with less data stored as I'll no longer need long lists for each doc after InvIndex is computed. Had issues with recursion depth
class Doc():
	def __init__ (self, doc):
		self.name = doc.name
		self.title = doc.title
		self.url = doc.url
		self.tf_idf = doc.tf_idf

def main():
	word_list = stem_words(["news", "Syra", "Trump", "President", "Sports"]) #be sure to start later
	global total_documents

        
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

	# #get doc details from docs.dat for later use.
	file = 'docs.dat'
	with open(file) as doc :
		get_docs_details(doc)

	#make all of the documents
	for doc in words[0].documents.iterkeys() :
		Document(doc)
	documents.sort(key=lambda x: x.name)

	tf_idf_list = []
	names = []
	for doc in documents:
		if doc.name not in names :
			names.append(doc.name)
			temp = Doc(doc)
			tf_idf_list.append(temp)

	name = 'tfidf.p'
	with open(name, 'w') as file: 
		pickle.dump(documents,file)

	return documents

# if __name__ == '__main__':	
# 	main()