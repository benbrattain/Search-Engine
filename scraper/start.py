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
	# crawl.main()
	#pagerank starts index.py first.
	
	#This segment will be uncommented when running on burrow.
	#file = 'pageranks.p'
	#with open(file) as f:
	#	pageranks = pickle.load(f)

	#This segment will be uncommented when running locally
	pageranks = pagerank.main()


	tfidfs = tfidf.main(word_list)
	merge_scores(tfidfs, pageranks)
	merged_docs.sort(key= lambda x : x.rank, reverse = True)

	#to output to cgi
	results = []
	for doc in merged_docs :
		results.append(doc.url)
	print results
	return results

	# for doc in merged_docs :
	# 	print "Name : " + doc.name + " Title: " + doc.title + " Url: " + doc.url + " Score: " + str(doc.rank) 
if __name__ == '__main__':
	wordlist = ["news", "politics", "appointment"]
	main(wordlist)