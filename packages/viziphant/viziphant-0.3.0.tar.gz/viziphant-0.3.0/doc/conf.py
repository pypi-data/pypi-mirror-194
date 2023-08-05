# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import date

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('.'))

# -- Setup environment variables for elephant --------------------------------
# set the following environment variables to ensure execution of plots when
# building docs. This is of importance in connection with elephant modules
# using OpenCL (pyopencl) or CUDA (pycuda).

os.environ["ELEPHANT_USE_OPENCL"] = "0"
os.environ["ELEPHANT_USE_CUDA"] = "0"

# -- Project information -----------------------------------------------------

project = 'Viziphant'
authors = 'Elephant team'
copyright = u"2017-{this_year}, {authors}".format(this_year=date.today().year,
                                                  authors=authors)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'matplotlib.sphinxext.plot_directive',
    'sphinxcontrib.bibtex',
    'numpydoc',
    'sphinx_tabs.tabs',
    'sphinx.builders.linkcheck',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
root_dir = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(root_dir, 'viziphant', 'VERSION')) as version_file:
    # The full version, including alpha/beta/rc tags.
    release = version_file.read().strip()

# The short X.Y version.
version = '.'.join(release.split('.')[:-1])


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Required to automatically create a summary page for each function listed in
# the autosummary fields of each module.
autosummary_generate = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'
html_theme_options = {
    'font_family': 'Arial',
    'page_width': '1200px',  # default is 940
    'sidebar_width': '280px',  # default is 220
    'logo': 'viziphant_logo_sidebar.png',  # add logo to sidebar
    'fixed_sidebar': 'true'
}

# The name of math_renderer extension for HTML output.
html_math_renderer = 'mathjax'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_static_path = ['images/viziphant_logo_sidebar.png']

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'images/viziphant_favicon.ico'

# Suppresses  wrong numpy doc warnings
# see here https://github.com/phn/pytpm/issues/3#issuecomment-12133978
numpydoc_show_class_members = False

# If false, no index is generated.
html_use_index = True

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'viziphantdoc'

# configuration for intersphinx: refer to Elephant
intersphinx_mapping = {'viziphant': ('https://viziphant.readthedocs.io/en/latest/', None)}

# path to bibtex_bibfiles
bibtex_bibfiles = ['bib/viziphant.bib']

# To configure your referencing style:
bibtex_reference_style = 'author_year_round'

# To configure the bibliography style:
bibtex_default_style = 'author_year'

# replace square brackets in citation with round brackets
from dataclasses import dataclass, field
import sphinxcontrib.bibtex.plugin

from sphinxcontrib.bibtex.style.referencing import BracketStyle
from sphinxcontrib.bibtex.style.referencing.author_year \
    import AuthorYearReferenceStyle


def bracket_style() -> BracketStyle:
    return BracketStyle(
        left='(',
        right=')',
    )


@dataclass
class RoundBracketReferenceStyle(AuthorYearReferenceStyle):
    bracket_parenthetical: BracketStyle = field(default_factory=bracket_style)
    bracket_textual: BracketStyle = field(default_factory=bracket_style)
    bracket_author: BracketStyle = field(default_factory=bracket_style)
    bracket_label: BracketStyle = field(default_factory=bracket_style)
    bracket_year: BracketStyle = field(default_factory=bracket_style)


sphinxcontrib.bibtex.plugin.register_plugin(
    'sphinxcontrib.bibtex.style.referencing',
    'author_year_round', RoundBracketReferenceStyle)

# Custom style for bibliography labels

from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.labels import BaseLabelStyle
from pybtex.plugin import register_plugin


# a simple label style which uses the bibtex keys for labels
class AuthorYearStyle(BaseLabelStyle):

    def format_labels(self, sorted_entries):
        for entry in sorted_entries:
            # create string for label
            yield entry.persons["author"][0].last_names[0] + ", " +\
                entry.fields["year"][-4:]


class AuthorYear(UnsrtStyle):

    default_label_style = AuthorYearStyle


register_plugin('pybtex.style.formatting', 'author_year', AuthorYear)
