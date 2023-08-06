"""
Wrapper to display Constellate charts in Jupyter
"""

try:
    from IPython.core.display import display, HTML
    from IPython.display import IFrame
except ImportError as e:
    raise ImportError("Import Error: A working installation of Jupyter notebooks is required to use this feature.")


from urllib.parse import urlencode
from urllib.parse import quote, quote_plus

site_root = "https://constellate.org"
chart_path = site_root + "/charts/%s/?%s"


def _query(qdict):
    return urlencode(qdict)


def _render(chart, qdict, terms=None, width="800", height="600"):
    if qdict.get("keyword"):
        qdict["keyword"] = qdict["keyword"]
    if (terms is not None) and (terms != []):
        qdict["unigrams"] = ",".join([t.lower() for t in terms])
    q = _query(qdict)
    url = chart_path % (chart, q)
    return display(HTML(
        '<iframe src="%s" height="%s" width="%s" frameborder="0"/>' % (url, height, width)
    ))


def documents_over_time(query):
    return _render("documents-over-time", query)

def categories_over_time(query):
    q = urlencode(query)
    return _render("categories-over-time", query)

def keyphrases(query):
    return _render("keyphrases", query)

def word_cloud(query):
    return _render("word-cloud", query)

def term_frequency(query, terms):
    return _render("term-frequency", query, terms=terms)
