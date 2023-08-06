from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from .util import simple_html_visitor


class WhereNextDirective(SphinxDirective):
    """The WhereNextDirective directive is used to generate an "Where Next" block."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        where_next = WhereNext()
        where_next_title = WhereNextTitle()
        where_next += where_next_title
        where_next_title += nodes.Text('Where next?', 'Where next?')
        self.state.nested_parse(self.content, self.content_offset, where_next)
        return [where_next]


class WhereNext(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-where-next')


class WhereNextTitle(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-where-next-title')


class WhereNextContent(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-where-next-content')


def setup(app):
    """Setup the Where Next extensions."""
    app.add_directive('where-next', WhereNextDirective)
    app.add_node(WhereNext, html=simple_html_visitor('div'))
    app.add_node(WhereNextTitle, html=simple_html_visitor('p'))
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
