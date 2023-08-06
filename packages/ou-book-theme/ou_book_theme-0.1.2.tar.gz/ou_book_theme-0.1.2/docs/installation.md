# Installation

To use the OU Book Theme, first install it into your project:

```
pip install ou-book-theme
```

Then enable the theme in your {file}`_config.yml`:

```yaml
sphinx:
  extra_extensions:
    - ou_book_theme
  config:
    html_theme: ou_book_theme
```

Next, create a {file}`_static` directory and add two empty files {file}`favicon.svg` and {file}`logo.svg`. These will automatically be overwritten by
the theme, but need to be in place for the build process to know that the files exist.

Then set the two files in the `logo` and `html.favicon` keys in the {file}`_config.yml`:

```yaml
logo: _static/logo.svg

...

html:
  favicon: _static/favicon.svg
```

You are now ready to build your book with the OU Book Theme.
