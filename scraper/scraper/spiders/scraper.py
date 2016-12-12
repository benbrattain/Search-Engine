from collections import deque
import scrapy
import os

#===========
# Exceptions
#===========
class AlgoNotProvidedException(Exception):
    pass
class AlgoNotSupportedException(Exception):
    pass
class NumPageNotProvidedException(Exception):
    pass
class DestFolderNotProvidedException(Exception):
    pass
class UrlNotProvidedException(Exception):
    pass

#===========
# Containers
#===========
class Container(deque):
    ''' This is a class that serves as interface to the Spider '''
    def add_element(self, ele):
        ''' Add an element to the contain, always to the right '''
        return self.append(ele)

    def get_element(self):
        ''' This is an abstract method '''
        # One can also implement this using built-in module "abc",
        #   which stands for Abstract Base Class and produces a
        #   more meaningful error
        raise NotImplementedError

class Queue(Container):
    ''' Queue data structure implemented by deque '''
    def get_element(self):
        ''' Pop an element from the left '''
        return self.popleft()

class Stack(Container):
    ''' Stack data structure implemented by deque '''
    def get_element(self):
        ''' Pop an element from the right '''
        return self.pop()

#=======
# Spider
#=======
class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = []
    allowed_domains = []
    next_page = None
    flag = False
    num_pages_visited = 0
    visited = []

    def __init__(self, algo=None, num=None, directory=None, urls=None,
            *args, **kwargs):
        ''' Cutomized constructor that takes command line arguements '''
        super(ExampleSpider, self).__init__(*args, **kwargs)

        # check manditory inputs
        if num is None:
            raise NumPageNotProvidedException
        self.num_page_to_fetch = int(num)

        if directory is None:
            raise DestFolderNotProvidedException
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        if '/' not in directory:
            directory += '/'    
        self.dest_folder = directory

        if urls is None:
            raise UrlNotProvidedException

        self.start_urls = urls.split(',')

        # check algorithm choice, and construct container accordingly
        if algo is None:
            raise AlgoNotProvidedException
        elif algo == 'dfs':
            self.container = Stack()
        elif algo == 'bfs':
            self.container = Queue()
        else:
            raise AlgoNotSupportedException

        for u in self.start_urls:
            self.container.add_element(u)
        return

    def parse(self, response):
        # The following are accessible from self
        # - self.num_page_to_fetch = maximum number of pages to fetch
        # - self.dest_folder = path to folder where files should be stored
        # - self.container = Container object where urls are stored and extracted
        
        max_pages = self.num_page_to_fetch
        dest_folder = self.dest_folder
        self.visited.append(response.url)

        if response.url[len(response.url) - 1] == '/':
            self.visited.append(response.url[:-1])
        else:
            self.visited.append(response.url + '/')
            
        #self.num_pages_visited += 1

        # extract links from page
        #links = response.xpath('@href').extract()
        links = response.css('a::attr(href)').extract()

        if isinstance(self.container, Stack):
            links = links[::-1]

        for link in links:
            if response.urljoin(link) not in self.visited:
                self.container.add_element(response.urljoin(link))


        file_name = dest_folder + str(self.num_pages_visited) + '.html'
        html_writer = open(file_name, 'w')
        html_writer.write(response.body)
        html_writer.close()

        index_file = dest_folder + 'index.dat'
        writer = open(index_file, 'a+')
        writer.write(str(self.num_pages_visited) + '.html ' + response.url + '\n')
        writer.close()
        self.log('Saved file: ' + file_name)


        if (self.num_pages_visited < max_pages) and self.container:
            next_page = self.container.get_element()
                
            while self.container and next_page in self.visited:
                next_page = self.container.get_element()


            if next_page and (next_page not in self.visited):
                self.visited.append(next_page)
                self.num_pages_visited += 1
                request = scrapy.Request(next_page, callback = self.parse, dont_filter = True)
                yield request
        