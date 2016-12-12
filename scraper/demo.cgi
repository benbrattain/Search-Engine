#!/usr/bin/python
import cgi


# Base of the html content
CONTENT = """
<html>
<title>Interactive Page</title>
<body>
    <h1>Simple Search Engine</h1>
    <form method=POST action="demo.cgi">
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
        '<a id="result%d" href="%s">result%d</a><br>' % (idx, url, idx)
        for idx, url in enumerate(results)
    )


def main():
    print "Content-Type: text/html\n\n"
    # parse form data
    form = cgi.FieldStorage()

    # get the query, if any, from the form
    if 'query' in form:
        query_str = cgi.escape(form['query'].value)
    else:
        query_str = '"empty query"'

    # TODO: process your query and get hit results
    # Result should be a list of url strings

    # format URL strings in results into hyperlinks
    results = None
    if results is None or len(results) == 0:
        result_str = '<h3>Empty result: No Hit</h3>'
    else:
        result_str = format_results(results)

    # format your final html page
    print CONTENT % (query_str, result_str)


if __name__ == '__main__': main()
