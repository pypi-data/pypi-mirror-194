from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from .util import simple_html_visitor


class ActivityDirective(SphinxDirective):
    """The ActivityDirective directive is used to generate an activity block."""

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        activity = Activity()
        activity_title = ActivityTitle()
        activity += activity_title
        activity_title += nodes.Text(self.arguments[0], self.arguments[0])
        self.state.nested_parse(self.content, self.content_offset, activity)
        return [activity]


class Activity(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-activity')


class ActivityTitle(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-activity-title')


class ActivityAnswerDirective(SphinxDirective):
    """The ActivityAnswerDirective directive is used to generate an activity block."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        activity_answer = ActivityAnswer()
        self.state.nested_parse(self.content, self.content_offset, activity_answer)
        return [activity_answer]


class ActivityAnswer(nodes.Element):

    def __init__(self, rawsource='', *children, **attributes):
        super().__init__(rawsource=rawsource, *children, **attributes)
        self.set_class('ou-activity-answer')


def setup(app):
    """Setup the Activity extensions."""
    app.add_directive('activity', ActivityDirective)
    app.add_node(Activity, html=simple_html_visitor('div'))
    app.add_node(ActivityTitle, html=simple_html_visitor('p'))
    app.add_directive('activity-answer', ActivityAnswerDirective)
    app.add_node(ActivityAnswer, html=simple_html_visitor('div'))
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
