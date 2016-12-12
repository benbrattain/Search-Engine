import sys, re, collections, pickle
from nltk.corpus import stopwords
from nltk.stem import *
from bs4 import BeautifulSoup
from unidecode import unidecode
reload(sys)
sys.setdefaultencoding('utf-8')

#enables me to process all the words for the invindex
words = []
#for pagerank
documents = list()
global doc_hash
doc_hash = {}


def write_invindex(words):
    string = ""
    with open('invindex.dat','a') as doc:
        for word in words :
            string += word.name + " documents: "
            for key, freq in word.documents.iteritems():
                string += key + " - " + str(freq) + " "
            string += "\n"
        doc.write(string)

class Word(object):
    def __init__(self, name, document, frequency):
        self.name = name
        self.documents = {document : frequency}


    def add_doc(self, document, frequency):
        self.documents[document] = frequency

class Document(object):
    def __init__(self, document, url, name):
        self.document = document
        self.words = self.parse_words()
        self.filtered_words = self.filter_words(self.words)
        self.stemmed_words = self.stem_words(self.filtered_words)
        self.length = len(self.stemmed_words)
        self.counted_words = collections.Counter(self.stemmed_words)
        self.url = url
        self.name = name
        self.title
        self.links = collections.Counter(self.parse_links())
        self.num_links = sum(self.links.values())
        self.pagerank = 1 #default score to start. will use this in pagerank.py later
        self.compute_words()
        self.write_doc()
        documents.append(self)

    #for pagerank later
    def parse_links(self) :
        links = []
        with open(self.document) as doc:
            html = doc.read()
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.findAll(href = True):
                links.append(link.get('href'))
        return links

            

    #removes links that won't be in my index so I don't have to deal with them for Pagerank. Already computed num of links on the page.
    def clean_links(self) :
        for doc in documents:
            if doc.url not in self.links :
                del self.links[doc.url]

      
    def parse_words(self):
        words = None
        with open(self.document) as doc:
            html = doc.read()
            soup = BeautifulSoup(html, 'html.parser')
            self.set_title(soup)
            words = soup.findAll(text=True)
        
        #I figured everything previous on my own, but used https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages
        #to figure out how to clean up the rest for scripts etc. Only for this function visible.
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(unidecode(element))):
                return False
            return True

        #filters out scripts, newlines etc.
        text = filter(visible, words)
        text = filter(lambda a: a != '\n', text)
        words = []

        #tokenizing indirectly.
        for string in text :
            temp = string.replace(".","").split()
            for element in temp :
                element = unidecode(element)
                words.append(element)
        
        return words

    #removes stopwords
    def filter_words(self,words):
        filtered_words = [word for word in words if word not in stopwords.words('english')]
        return filtered_words

    #stems words
    def stem_words(self, words):
        output = []
        stemmer = SnowballStemmer("english")

        for word in words:
            temp = stemmer.stem(word)
            output.append(temp)
        
        return output

    def set_title(self,soup):
        self.title = soup.title.string

    #turns words in doc into word objects or appends them to current object
    def compute_words(self):
        wordExists = False
        for word, freq in self.counted_words.items() :
            for item in words :
                if item.name == word :
                    item.add_doc(self.name, freq)
                    wordExists = True
            if not wordExists:
                document = self.name
                temp = Word(word,document, freq)
                words.append(temp)

    #writes info to docs.dat
    def write_doc(self) :
        with open('docs.dat','a') as doc:
            string = self.name + " length: " + str(self.length) + " title: " + self.title + " url: " + self.url + "\n"
            doc.write(string)

def main() :
        
    file = 'pages/index.dat'
    with open(file) as doc:
        for line in doc:
            info = line.split()
            currentFile = 'pages/' + info[0]
            document = Document(currentFile, info[1],info[0])
    write_invindex(words)

    #for pagerank later.
    for doc in documents :
        doc.clean_links()
    for doc in documents :
        doc_hash[doc.url] = doc

    return doc_hash        


if __name__ == '__main__':
    main()
    # try:
    #     del sys.argv[0] # Delete the file name from the args
    #     location = sys.argv[0] # Get the first real arg, the name of the file to analyze
    #     index = sys.argv[1] #name of files
    # except IndexError:
    #     raise ValueError ("Please specify a file in the command arg, like: 'python index.py directory/ index.dat'")