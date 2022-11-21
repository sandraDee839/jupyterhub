#
import os

# -- General configuration ------------------------------------------------

# Sphinx extension modules
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'autodoc_traits',
    'sphinx_copybutton',
    'sphinx-jsonschema',
    'myst_parser',
]

myst_heading_anchors = 2
myst_enable_extensions = [
    'colon_fence',
    'deflist',
]
# The master toctree document.
root_doc = master_doc = 'index'

# General information about the project.
project = 'JupyterHub'
copyright = '2016, Project Jupyter team'
author = 'Project Jupyter team'

# Autopopulate version
import jupyterhub

# The short X.Y version.
version = '%i.%i' % jupyterhub.version_info[:2]
# The full version, including alpha/beta/rc tags.
release = jupyterhub.__version__

language = "en"
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

# Set the default role so we can use `foo` instead of ``foo``
default_role = 'literal'

from contextlib import redirect_stdout
from io import StringIO

from docutils import nodes
from sphinx.directives.other import SphinxDirective

# -- Config -------------------------------------------------------------
from jupyterhub.app import JupyterHub

# create a temp instance of JupyterHub just to get the output of the generate-config
# and help --all commands.
jupyterhub_app = JupyterHub()


class ConfigDirective(SphinxDirective):
    """Generate the configuration file output for use in the documentation."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        # The generated configuration file for this version
        generated_config = jupyterhub_app.generate_config_file()
        # post-process output
        home_dir = os.environ['HOME']
        generated_config = generated_config.replace(home_dir, '$HOME', 1)
        par = nodes.literal_block(text=generated_config)
        return [par]


class HelpAllDirective(SphinxDirective):
    """Print the output of jupyterhub help --all for use in the documentation."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        # The output of the help command for this version
        buffer = StringIO()
        with redirect_stdout(buffer):
            jupyterhub_app.print_help('--help-all')
        all_help = buffer.getvalue()
        # post-process output
        home_dir = os.environ['HOME']
        all_help = all_help.replace(home_dir, '$HOME', 1)
        par = nodes.literal_block(text=all_help)
        return [par]


def setup(app):
    app.add_css_file('custom.css')
    app.add_directive('jupyterhub-generate-config', ConfigDirective)
    app.add_directive('jupyterhub-help-all', HelpAllDirective)


source_suffix = ['.rst', '.md']

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML
html_theme = 'pydata_sphinx_theme'

html_logo = '_static/images/logo/logo.png'
html_favicon = '_static/images/logo/favicon.ico'

# Paths that contain custom static files (such as style sheets)
html_static_path = ['_static']

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jupyterhub/jupyterhub",
            "icon": "fab fa-github-square",
        },
        {
            "name": "Discourse",
            "url": "https://discourse.jupyter.org/c/jupyterhub/10",
            "icon": "fab fa-discourse",
        },
    ],
    "use_edit_page_button": True,
    "navbar_align": "left",
}

html_context = {
    "github_user": "jupyterhub",
    "github_repo": "jupyterhub",
    "github_version": "main",
    "doc_path": "docs",
}

# -- Intersphinx ----------------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'tornado': ('https://www.tornadoweb.org/en/stable/', None),
}

# -- Read The Docs --------------------------------------------------------

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    # readthedocs.org uses their theme by default, so no need to specify it
    # build both metrics and rest-api, since RTD doesn't run make
    from os.path import dirname
    from subprocess import check_call as sh

    docs = dirname(dirname(__file__))
    sh(['make', 'metrics', 'scopes'], cwd=docs)

# -- Spell checking -------------------------------------------------------

try:
    import sphinxcontrib.spelling  # noqa
except ImportError:
    pass
else:
    extensions.append("sphinxcontrib.spelling")

spelling_word_list_filename = 'spelling_wordlist.txt'
