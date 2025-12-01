"""
Script to generate 'mkdocs.yml'.
"""

import os


def generate_nav(directory, base_path=''):
    """
    Recurse to every leaf-pathname under directory, and, if it correspond to
    a markdown-file, then add it to the list of markdown-pathnames.
    """
    nav = []
    for item in sorted(os.listdir(directory)):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            if item == 'javascripts':
                continue
            # Item is a directory.
            # - Call generate_env() recursively to descend into it.
            # - Append its markdown-files to the list.
            nav.append({item: generate_nav(item_path, base_path + item + '/')})
        elif item.endswith('.md'):
            # Item is a markdown-file.
            # - Append it to the list.
            nav.append({item[:-3]: base_path + item})
    return nav


def main():
    nav = generate_nav('docs')

    mkdocs_yml = f"""
extra_javascript:
  - https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.js
  - https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/auto-render.min.js
  - javascripts/katex.js
extra_css:
  - https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.extra
  - pymdownx.superfences
  - pymdownx.betterem
  - pymdownx.tilde
repo_name: GitHub
repo_url: https://github.com/tevaughan/notes
site_name: Thomas E. Vaughan's Journal and Notes
site_url: https://tevaughan.github.io/notes/
theme:
  name: material

nav:
"""
    for item in nav:
        mkdocs_yml += f'  - {list(item.keys())[0]}: {list(item.values())[0]}\n'

    mkdocs_yml += """
plugins:
  - search
"""

    with open('mkdocs.yml', 'w') as f:
        f.write(mkdocs_yml)


if __name__ == '__main__':
    main()
