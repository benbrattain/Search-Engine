# page rank should be in pagerank.py. Should have def pagerank(graph):
# 	return prank.
# graph: {key str: iterator(neighbors str))
# prank - key str: float pagerank

from index import *
import index
import pickle

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


def pagerank(graph) :
	rank = 0
	for doc in graph.links.keys() :
		#number of times link is in page
		freq = graph[doc]
		name = doc_names[doc]
		page = documents
		rank += freq * (page.pagerank / page.num_links)
	rank = .15 + (.85 * rank)
	graph.pagerank = rank
	return rank


if __name__ == '__main__':

	
	documents = index.main()
	print documents
	docs = []

	ranked_documents = []
	for doc in documents :
		name = doc.name + '.p'
		f = open(name, 'r')
		page = pickle.load(f)
		f.close()
		ranked_documents.append(page)




