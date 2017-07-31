Jinjatex
========

A wrapper of `Jinja2 <https://github.com/pallets/jinja>`_ for easy
rendering of `.tex` files of all sorts.


Installation
------------

.. code-block:: bash

    pip install jinjatex

Usage
-----

The main :code:`Jinjatex` class provides wrappers to compile tex templates
with jinja. Tex is not included, so make sure the binaries are available.

Template Syntax
^^^^^^^^^^^^^^^

.. code-block:: none

    ((= This is a comment. =))
    ((* for value in somelist *))
        ((( value )))
    ((* endfor *))

Python Bindings
^^^^^^^^^^^^^^^

.. code-block:: python

    from jinjatex import Jinjatex

    from textwrap import dedent

    # Example 1: Compile string templates

    template_string = dedent(r"""
        \documentclass{article}
        \begin{document}
        Hi ((( name )))!
        \end{document}
        """)

    tex = Jinjatex()

    # Return rendered template only
    tex.render(template_string)
    # Compile .tex and return content of .pdf, default engine is pdflatex
    with open('result.pdf', 'wb') as file:
        file.write(tex.compile(template_string))


    # Example 2: Jinja options and other tex compilers
    # Assuming a template 'mytemplate.tex' exists in mypackage/tex_templates

    from jinja2 import PackageLoader, StrictUndefined

    tex = Jinjatex(tex_engine='xelatex',
                   loader=PackageLoader('mypackage', 'tex_templates'),
                   trim_blocks=True,
                   undefined=StrictUndefined)

    tex.render_template('mytemplate.tex')
    with open('result.pdf', 'wb') as file:
        file.write(tex.compile_template('mytemplate.tex'))
