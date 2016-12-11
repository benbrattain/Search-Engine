# page rank should be in pagerank.py. Should have def pagerank(graph):
# 	return prank.
# graph: {key str: iterator(neighbors str))
# prank - key str: float pagerank

import index

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

#get documents from invindex.py.
def get_documents() :
	f = open('documents.p', 'r')
	documents = pickle.load(f)
	f.close()
	return documents

#initial pickling of all documents
def pickle_docs(documents) :
	for doc in documents :
		doc_names[doc.url] = doc.name
		name = self.name + '.p'
		f = open(name, 'w')
		pickle.dump(doc, f)
		f.close()


def pagerank(graph) :
	rank = 0
	for doc in graph.links.keys() :
		#number of times link is in page
		freq = graph[doc]
		name = doc_names[doc]
		file_name = name + '.p'
		f = open(file_name, 'r')
		page = pickle.load(f)
		f.close()
		rank += freq * (page.pagerank / page.num_links)
	rank = .15 + (.85 * rank)
	return rank

def update_pagerank(graph) :
	rank = pagerank(graph)
	name = graph.name + '.p'
	f = open(name, 'w')
	pickle.dump(graph, f)
	f.close()

if __name__ == '__main__':

	documents = get_documents()
	pickle_docs(documents)
	for i in range(100): #arbitrary num of times, can be adjusted.
		for doc in documents:
			update_pagerank(doc)

	ranked_documents = []
	for doc in documents :
		name = doc.name + '.p'
		f = open(name, 'r')
		page = pickle.load(f)
		f.close()
		ranked_documents.append(page)

	name = 'pagerank.p'
	f = open(name, 'w')
	pickle.dump(f, ranked_documents)




