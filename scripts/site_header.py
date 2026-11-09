"""Render the one shared header used by every public HTML page."""
from jinja2 import Environment, FileSystemLoader, select_autoescape

from scripts.common import ROOT


def render_header(config, active, root_prefix=""):
    env = Environment(loader=FileSystemLoader(ROOT / "site/partials"),
                      autoescape=select_autoescape(["html"]))
    return env.get_template("header.html").render(config=config, active=active, root_prefix=root_prefix)
