from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from .util import simple_html_visitor


class TimeDirective(SphinxDirective):
    """The ActivityDirective directive is used to generate an activity block."""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        time = Time()
        time += nodes.Text(self.arguments[0], self.arguments[0])
        return [time]


class Time(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-time')


def setup(app):
    """Setup the Time extensions."""
    app.add_directive('time', TimeDirective)
    app.add_node(Time, html=simple_html_visitor('div'))
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
