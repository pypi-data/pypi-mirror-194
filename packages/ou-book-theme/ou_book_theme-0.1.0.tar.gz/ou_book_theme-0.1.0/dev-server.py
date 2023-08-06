#!/usr/bin/env python
from livereload import Server, shell

build_docs = shell('hatch run dev:jupyter-book build --all docs')
shell('npm install')()
shell('npm run build')()
build_docs()

server = Server()
server.watch('docs/**/*.md', build_docs)
server.watch('docs/**/*.yml', build_docs)
server.watch('ou_book_theme/assets/**/*.*', shell('npm run build'))
server.watch('ou_book_theme/theme/**/*.*', build_docs)
server.watch('ou_book_theme/**/*.py', build_docs)
server.serve(root='docs/_build/html', port=8000)
