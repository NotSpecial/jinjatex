"""Super small example."""

from textwrap import dedent
from jinjatex import Jinjatex

template_string = dedent(r"""
    % Example Template
    \documentclass{article}

    \begin{document}
    Hi ((( name )))!

    The document will be compiled multiple times, until
    all references etc. are resolved, like this one: \ref{somelabel}

    \section{Somesection}
    \label{somelabel}

    Some more content.

    \end{document}
    """)

tex = Jinjatex()

# Return rendered template only
print(tex.render(template_string, name="Alex"))
# Compile .tex and return content of .pdf
with open('result.pdf', 'wb') as file:
    file.write(tex.compile(template_string, name="Alex"))
