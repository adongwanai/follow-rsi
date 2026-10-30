"""Build the owner-supplied long-form article without changing its Markdown."""
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown

from scripts.common import read_yaml


def build_articles(root):
    root = Path(root)
    slug = 'why-ai-self-improvement'
    source = root / 'articles' / f'{slug}.md'
    if not source.exists():
        return
    title, body = source.read_text(encoding='utf-8').split('\n', 1)
    parser = markdown.Markdown(extensions=['extra', 'toc'], extension_configs={
        'toc': {'permalink': False, 'toc_depth': '2-2'}})
    content = parser.convert(body.strip()).replace('../site/articles/assets/', 'assets/')
    config = read_yaml(root / 'site.config.yaml')
    content = content.replace(f'href="{slug}-audit.md"',
        f'href="{config["repository_url"]}/blob/main/articles/{slug}-audit.md"')
    env = Environment(loader=FileSystemLoader(root / 'scripts/templates'),
                      autoescape=select_autoescape(['html']), keep_trailing_newline=True)
    html = env.get_template('article.html').render(
        title=title.removeprefix('# '), body=content, toc=parser.toc,
        canonical=config['base_url'].rstrip('/') + f'/articles/{slug}.html',
        repository=config['repository_url'], slug=slug)
    target = root / 'site/articles' / f'{slug}.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')
