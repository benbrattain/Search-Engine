import os, pickle, crawl, index, pagerank, tfidf
from pagerank import PageDoc
from tfidf import Doc 
#os.system('filename.py')

merged_docs = []

class MergedRank:
	def __init__ (self, doc, pagedoc) :
		self.name = doc.name
		self.title = doc.title
		self.url = doc.url
		self.rank = doc.tf_idf * pagedoc.pagerank
		merged_docs.append(self)

#should be sorted by name anyways by this point so the for loops shouldn't take much time.
def merge_scores(tfidfs, pageranks) :
	for doc in tfidfs :
		for page in pageranks :
			if doc.name == page.name:
				MergedRank(doc, page)
				break

def main(word_list) :
	crawl.main(word_list)
	#pagerank starts index.py first.
	pagerank = pagerank.main()
	tfidf = tfidf.main()
	merge_scores(tfidf, pagerank)
	merged_docs.sort(key= lambda x : x.rank, reverse = True)

	#to output to cgi
	results = []
	for doc in merged_docs :
		results.append(doc.url)

	# for doc in merged_docs :
	# 	print "Name : " + doc.name + " Title: " + doc.title + " Url: " + doc.url + " Score: " + str(doc.rank) 
if __name__ == '__main__':
	word_list = ["sports"]
	main(word_list)