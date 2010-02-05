
import sys, os

project = u'Project Documentation'
copyright = u'2010, Justin Quick <justquick@gmail.com>'
version = '0.1'
release = '0.1'

sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']
templates_path = ['templates']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'
exclude_trees = ['build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = []
htmlhelp_basename = 'DjangoNativeTagsdoc'
