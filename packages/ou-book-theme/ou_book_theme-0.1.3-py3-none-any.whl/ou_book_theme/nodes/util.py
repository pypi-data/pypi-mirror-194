def simple_html_visitor(tag: str):
    def visit(self, node) -> None:
        self.body.append(self.starttag(node, tag))

    def depart(self, node) -> None:
        self.body.append(f'</{tag}>')

    return (visit, depart)
