# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

import sphinx_bootstrap_theme
from pygments.lexer import RegexLexer
from pygments import token
from sphinx.highlighting import lexers
from pygments.style import Style
from re import escape

keywords = [
    'runtime', 'load', 'store', 'deref', 'deref!', 'const', 'print', 'pop',
    'prj', 'prj!', 'indir', 'rot', 'dup', 'goto', 'goto-if', 'goto-if-not',
    'label', 'blockaddr', 'call', 'list', 'tuple', 'return', 'line', 'defun',
    'switch', 'document', 'filename', 'free', 'name', 'args', 'firstlineno'
]
operators = ['{', '}', '|', '=>', '_', '[', ']']


class WurusaiStyle(Style):
    background_color = "#FFFFAA"
    styles = {
        token.Text: "#AA3939",
        token.String: "#479030",
        token.Keyword: "#A600A6",
        token.Operator: "#246C60",
        token.Number: "#779D34",
        token.Comment: "#AA6F39",
        token.Punctuation: '#DE369D',
        token.Literal: "#4671D5"
    }


def pygments_monkeypatch_style(mod_name, cls):
    import sys
    import pygments.styles
    cls_name = cls.__name__
    mod = type(__import__("os"))(mod_name)
    setattr(mod, cls_name, cls)
    setattr(pygments.styles, mod_name, mod)
    sys.modules["pygments.styles." + mod_name] = mod
    from pygments.styles import STYLE_MAP
    STYLE_MAP[mod_name] = mod_name + "::" + cls_name


pygments_monkeypatch_style("wurusai", WurusaiStyle)
pygments_style = "wurusai"


class SijLexer(RegexLexer):
    name = 'sijuiacion'

    tokens = {
        'root': [
            *[(escape(k), token.Keyword) for k in keywords],
            *[(escape(o), token.Operator) for o in operators],
            (r"#([^\\#]+|\\.)*?#", token.Literal), (r"\d+", token.Number),
            (r"[-$\.a-zA-Z_\u4e00-\u9fa5][\-\!-$\.a-zA-Z0-9_\u4e00-\u9fa5]*",
             token.Name), (r'''"([^\\"]+|\\.)*?"''', token.String),
            (r'\s+', token.Whitespace)
        ]
    }


class RBNFLexer(RegexLexer):
    name = 'rbnf'

    tokens = {
        'root': [
            *[(escape(o), token.Punctuation)
              for o in ['->', '|', ';', ':', '=', '?']],
            (r"#([^\\#]+|\\.)*?#", token.Comment),
            (r"[-$\.a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]*",
             token.Keyword), (r'''"([^\\"]+|\\.)*?"''', token.Operator),
            (r"""'([^\\']+|\\.)*?'""", token.Operator),
            (r'\<.*\>', token.Operator), (r'\s+', token.Whitespace)
        ]
    }


lexers[SijLexer.name] = SijLexer(startinline=True)
lexers[RBNFLexer.name] = RBNFLexer(startinline=True)

extensions = ['sphinx.ext.mathjax', "recommonmark"]
master_doc = 'index'
project = 'Sijuiacion Language'
copyright = '2020, thautwarm'
author = 'thautwarm'

# The full version, including alpha/beta/rc tags
release = '0.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = "Sij Documentation"

html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    'navbar_site_name': "Documentation",
    'navbar_title': f"{project}",

    # Tab name for entire site. (Default: "Site")

    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.

    'navbar_links': [("GitHub", "github")],

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': True,

    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': "Subsections",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': -1,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    'globaltoc_includehidden': "true",

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    'navbar_class': "navbar navbar-inverse",

    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    'navbar_fixed_top': "true",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': "footer",

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "cosmo" or "sandstone".
    #
    # The set of valid themes depend on the version of Bootstrap
    # that's used (the next config option).
    #
    # Currently, the supported themes are:
    # - Bootstrap 2: https://bootswatch.com/2
    # - Bootstrap 3: https://bootswatch.com/3
    'bootswatch_theme': "united",

    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    'bootstrap_version': "3",
}
htmlhelp_basename = 'sij_'

# html_favicon = './favicon.ico'

latex_documents = [
    (master_doc, f'{project}.tex', f'{project}', 'thautwarm', 'manual'),
]

html_sidebars = {
    '**': [
    ]
}