# I built this assignment based off of the framework of hw4. Instead of scanning the inverted index,
# I instead took parts of index.py and retrieve.py in order to build a new program that could scrape the pages by itself.
# My methodology was pretty simple, I scanned the index.dat file and created a new Document object for each page.
# I also kept track of each new document while doing this.
# With the document object, I went ahead and filtered out and stemmed all the words just like in assignment 4.
# After that, I computed the TF score on the spot and then put the document into a large document array.
# After all of the documents were processed, I went ahead and calculated the idf_score tf_idf_score at the same time for each document.
# Finally, I sorted all of the documents by the tf_idf_scores and printed the highest 25, completing the assignment.

# If I was dealing with a much larger document base, I could have come up with some sort of method to prune out lower tf_idf_scores as they came along.
# That way I would use a smaller array and have a shorter sorting time. However, given the fact that it was only a few hundered documents, this wasn't necessary.



import sys, re, collections, math
from nltk.corpus import stopwords
from nltk.stem import *
from bs4 import BeautifulSoup
from unidecode import unidecode


hit_list = []

#stems words

def stem_words(words):
	output = []
	stemmer = SnowballStemmer("english")

	for word in words:
		temp = stemmer.stem(word)
		output.append(temp)
        
	return output


if __name__ == '__main__':
    try:
        del sys.argv[0] # Delete the file name from the args
        word_list = stem_words(sys.argv)
    except IndexError:
        raise ValueError ("Please specify a file in the command arg, like: 'python index.py directory/ index.dat'")

    try:
        
        file = 'invindex.dat'
        total_documents = 0
        with open(file) as doc:
            for line in doc:
                print line         

    except IOError as e:
        raise IOError("Please enter a correct file. Python says: '" + str(e)+"'")