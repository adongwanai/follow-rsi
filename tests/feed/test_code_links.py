import requests

from scripts.feed.fetch_github import verify_code_links
from scripts.feed.guard import enforce_evidence, unknown_evidence


class Session:
    def __init__(self, files):
        self.files = files
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append(url)
        return self

    def raise_for_status(self):
        if isinstance(self.files, Exception):
            raise self.files

    def json(self):
        return {'tree': [{'type': 'blob', 'path': path} for path in self.files]}


def test_code_link_with_non_readme_file_is_yes_and_keeps_url():
    url = 'https://github.com/example/research'
    session = Session(['README.md', 'src/agent.py'])
    checked = verify_code_links([url], session)
    evidence = enforce_evidence('No code link in abstract.', unknown_evidence(), checked['evidence'])
    assert evidence['code_released'] == {'value': 'yes', 'quote': url}
    assert checked['checks'][0]['non_readme_file'] == 'src/agent.py'
    assert len(session.calls) == 1


def test_readme_only_or_unreachable_repo_is_partial():
    url = 'https://github.com/example/research'
    for files in (['README.md', 'docs/README.rst'], requests.HTTPError('404')):
        result = verify_code_links([url], Session(files))
        assert result['evidence'] == {'value': 'partial', 'quote': url}
        assert result['checks'][0]['status'] != 'verified'


def test_non_repository_links_cannot_be_verified():
    session = Session([])
    for url in ('https://example.org/project', 'https://github.com/example/research/issues/1',
                'https://github.com.evil.test/example/research'):
        assert verify_code_links([url], session)['evidence']['value'] == 'partial'
    assert not session.calls
    assert verify_code_links([], session)['evidence'] == {'value': 'unknown', 'quote': None}
