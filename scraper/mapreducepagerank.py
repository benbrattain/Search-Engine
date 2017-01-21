# page rank should be in pagerank.py. Should have def pagerank(graph):
# 	return prank.
# graph: {key str: iterator(neighbors str))
# prank - key str: float pagerank

from index import *
import index
import itertools


doc_names = {}
global documents


#standard mapreduce algorithm. used in a tutorial as well.
def mapreduce(i,mapper,reducer):
  middle = []
  for (key,val) in i.items():
    middle.extend(mapper(key,val))
  groups = {}
  for key, group in itertools.groupby(sorted(middle), 
                                      lambda x: x[0]):
    groups[key] = list([y for x, y in group])
  return [reducer(middle_key,groups[middle_key])
          for middle_key in groups] 

def mapper(key, out_list):
	url = key[0]
	prank = key[1]
	return [(link, float(prank)/ float(len(out_list))) for link in out_list]

def reducer(url, list_of_links_or_rank):
	out_links =[]
	prank = 0

	for value in list_of_links_or_rank :
		if isinstance(list_of_links_or_rank,list):
			out_links = value
		else :
			prank += value
	pagerank = .15 + (.85 * prank)

	return ([url, pagerank] , out_links)



def main() :
	documents = index.main()
	documents_hash = {}
	#for mapreduce
	for url, doc in documents.iteritems():
		documents_hash[(url, doc.pagerank)] = doc.outboundlinks.keys()
	
	pageranks = mapreduce(documents_hash,mapper,reducer)
	


	for i in range(len(pageranks)):
		print str(i) + ". " + pageranks[i][0][0] + " " + str(pageranks[i][1])


if __name__ == '__main__':
	main()




