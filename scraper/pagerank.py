# page rank should be in pagerank.py. Should have def pagerank(graph):
# 	return prank.
# graph: {key str: iterator(neighbors str))
# prank - key str: float pagerank

from index import *
import index
import pickle
sys.setrecursionlimit(10000)

# class Document(object):
#     def __init__(self, document, url, name):
#         self.document = document
#         self.words = self.parse_words()
#         self.filtered_words = self.filter_words(self.words)
#         self.stemmed_words = self.stem_words(self.filtered_words)
#         self.length = len(self.stemmed_words)
#         self.counted_words = collections.Counter(self.stemmed_words)
#         self.url = url
#         self.name = name
#         self.title
#         self.links = collections.Counter(self.parse_links())
#         self.num_links = sum(self.links.values())
#         self.pagerank = 1 #default score to start. will use this in pagerank.py later
#         self.compute_words()
#         self.write_doc()
#         documents.append(self)


doc_names = {}
global documents


def pagerank(graph) :
	rank = 0
	for doc in graph.links.keys() :
		#number of times link is in page
		freq = graph.links[doc]
		#some links that aren't cleaned perfectly sometimes get through and are in the list unfortunately. they don't have a doc and as such are skipped.
		if doc in doc_names.keys() :
			page = doc_names[doc]
		else :
			continue
		rank += freq * (float(page.pagerank) / float(page.num_links))
	rank = .15 + (.85 * rank)
	graph.pagerank = rank
	return rank

#Smaller object with less data stored as I'll no longer need long lists for each doc after Pagerank is computed. Had issues with recursion depth
class PageDoc():
	def __init__ (self, doc):
		self.name = doc.name
		self.title = doc.title
		self.url = doc.url
		self.pagerank = doc.pagerank

def main() :
	documents = index.main()
	documents_array = []
	#for sorting at the end.
	for url, doc in documents.iteritems():
		documents_array.append(doc)
	for i in range(50):
		for url, doc in documents.iteritems() :
			pagerank(doc)

	documents_array.sort(key=lambda x: x.name)
	#remove any possible duplicates
	pageranks = list()
	names = list()
	for doc in documents_array :
		if doc.name not in names :
			temp = PageDoc(doc)
			pageranks.append(temp)
			names.append(doc.name)
	
	file = 'pagerank.p'
	with open(file, 'w') as f:
		pickle.dump(pageranks,f)

	return pageranks

# if __name__ == '__main__':
# 	main()




