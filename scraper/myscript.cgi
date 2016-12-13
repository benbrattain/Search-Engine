#!/user/bin/python
import cgi
from start import *

# Base of the html content
CONTENT = """
<html>
<title>Search Engine</title>
<body>
    <h1>News Search Engine</h1>
    <form method=POST action="myscript.cgi">
        <P><B>Your last query is "%s"; enter your new query</B>
        <P><input type=text name=query>
        <P><input type=submit>
    </form>
    <h2>Results</h2>
    %s
</body></html>
"""

def format_results(results):
  # join hyperlink tags with newlines
  return '\n'.join(
    '<a id="result%d" href ="%s">result%d</a><br>' % (idx, url, idx)
    for idx, url in enumerate(results)
    )

def main() :
  print "Content-Type: text/html\n\n"
  #parse form data
  form = cgi.FieldStorage()
  word_list = None
  #get the query, if any, from the form
  if 'query' in form:
    query_str = cgi.escape(form['query'].value)
    word_list = query_str.split()
  else :
    query_str = '"empty query"'

    #format URL strings in results into hyperlinks
    results = None

    if word_list :
      results = start.main(word_list)

    #TODO process query and get hit results.
    #results should be a list of url strings

    if results is None or len(results) == 0:
      result_str = '<h3>Empty result: No Hit</h3>'
    else :
      result_str = format_results(results)

    # format your final hmtl page
    print CONTENT % (query_str, result_str)