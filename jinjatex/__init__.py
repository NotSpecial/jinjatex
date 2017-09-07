# -*- coding: utf-8 -*-

r"""Create the xelatex files.

The jinja environment and filters are based on a [flask snippet]
(http://flask.pocoo.org/snippets/55/) by Clemens Kaposi.

Some adjustments were made:
* Environment made independent from flask
* New filter to convert '\n' to '\\'

The render_tex function takes care of filename and directory things.
It plugs everything into the template and can return either the .tex file or
start latex and return the .pdf (also removes all non .pdf files)
"""
import subprocess
from os import path
import re
from tempfile import TemporaryDirectory
from jinja2 import Environment


MAX_RUNS = 10  # Avoid infinite oscillations


class Error(Exception):
    """Jinjatex error."""


class Jinjatex(object):
    """Wrapper for a Jinja environment.

    Providing functions to easility render and compile templates.
    """

    def __init__(self, tex_engine='pdflatex', **kwargs):
        self.tex_engine = tex_engine

        parameters = {
            'block_start_string': '((*',
            'block_end_string': '*))',
            'variable_start_string': '(((',
            'variable_end_string': ')))',
            'comment_start_string': '((=',
            'comment_end_string': '=))',
        }
        parameters.update(kwargs)

        self.env = Environment(**parameters)
        self.env.filters['t'] = _escape_tex

    def render_template(self, name, *args, **kwargs):
        """Render template."""
        return self.env.get_template(name).render(*args, **kwargs)

    def render(self, source, *args, **kwargs):
        """Render template from string."""
        return self.env.from_string(source).render(*args, **kwargs)

    def compile_template(self, name, *args, tex_engine=None, **kwargs):
        """First render template, then compile it and return pdf content."""
        rendered = self.render_template(name, *args, **kwargs)
        engine = tex_engine or self.tex_engine
        return render_tex(rendered, engine)

    def compile(self, source, *args, tex_engine=None, **kwargs):
        """First render from string, then compile it and return pdf content."""
        rendered = self.render(source, *args, **kwargs)
        engine = tex_engine or self.tex_engine
        return render_tex(rendered, engine)


def _escape_tex(value):
    """Filter to make strings tex safe."""
    if not isinstance(value, str):
        return value
    subs = (
        (re.compile(r'\\'), r'\\textbackslash'),
        (re.compile(r'([{}_#%&$])'), r'\\\1'),
        (re.compile(r'~'), r'\~{}'),
        (re.compile(r'\^'), r'\^{}'),
        (re.compile(r'"'), r"''"),
        (re.compile(r'\.\.\.+'), r'\\ldots'),
    )
    for pattern, replacement in subs:
        value = pattern.sub(replacement, value)

    # Replace newlines
    value = value.replace('\n', r'\\')

    return value


def render_tex(source, tex_engine='pdflatex'):
    """Render the template and return the filename.

    Returns:
        str: filename (including path) to output
    """
    with TemporaryDirectory() as tempdir:
        # Safe .tex file
        # Technically passing as string should work,
        # but it seems there is an upper limit on the length
        texfile = path.join(tempdir, 'temp.tex')

        # Helper to read log file
        def read_log():
            with open(path.join(tempdir, 'temp.log'), 'rb') as file:
                return file.read().decode('utf-8')

        with open(texfile, 'wb') as file:
            file.write(source.encode('utf-8'))

        # Compile
        commands = [tex_engine,
                    "-output-directory", tempdir,
                    "-interaction=batchmode", texfile]

        try:
            for _ in range(MAX_RUNS):
                subprocess.check_output(commands)
                # Look for the keyword 'run' in the log, indicating we need
                # to compile again to resolve references etc.
                if 'run' not in read_log():
                    break

        except FileNotFoundError:
            # The command was not recognized
            raise Error("The command '%s' failed. Is everything installed?"
                        % commands[0])
        except subprocess.CalledProcessError as error:
            # Try to return tex log in error message
            try:
                raise Error("Something went wrong during compilation!\n"
                            "Here is the log content:\n\n %s" % read_log())
            except FileNotFoundError:
                # No log! Show output of command instead
                raise Error(error.output.decode('utf-8'))

        # Return content of pdf so all files can be removed
        with open(path.join(tempdir, 'temp.pdf'), 'rb') as file:
            return file.read()
