import sys, os
try:
  import sphinxtogithub
  optional_extensions = ['sphinxtogithub']
except ImportError:
  optional_extensions = []

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary'] + optional_extensions
master_doc = 'index'
project = u'gevent-utils'
copyright = u'2011, Travis Cline'
version = '0.0.1'
release = '0.0.1'

exclude_patterns = []
add_module_names = True
pygments_style = 'sphinx'

html_show_sourcelink = False
html_show_sphinx = False
htmlhelp_basename = 'gevent-utilsdoc'
latex_documents = [
  ('index', 'gevent-utils.tex', u'gevent-utils Documentation',
   u'Travis Cline', 'manual'),
]
man_pages = [
    ('index', 'gevent-utils', u'gevent-utils Documentation',
     [u'Travis Cline'], 1)
]
