import pytest
from api.models import Book, Author
from pytest_tipsi_django.client_fixtures import APIError


BOOK = '/api/001/book/'
AUTHOR = '/api/001/author/'


@pytest.fixture
def cli(anonymous_client):
    yield anonymous_client


def test_01_empty(cli):
    resp = cli.get_json(BOOK)
    assert resp == [], resp

    resp = cli.get_json(AUTHOR)
    assert resp == [], resp


def test_02_create(cli):
    out = cli.post_json(AUTHOR, {'name': 'Stanislav Lem'})
    assert Author.objects.count() == 1

    # {'books': [], 'id': 1, 'name': 'Stanislav Lem'}
    assert out['books'] == [], out
    assert out['name'] == 'Stanislav Lem', out

    lem = Author.objects.first()
    out = cli.post_json(BOOK, {'title': 'Solaris', 'author': lem.id})
    assert Book.objects.count() == 1

    # {'author': {'id': 1, 'name': 'Stanislav Lem'}, 'id': 1, 'title': 'Solaris'}
    assert out['author']['id'] == lem.id, out
    assert out['title'] == 'Solaris'


def test_03_bulk_create(cli):
    out = cli.post_json(f'{AUTHOR}batch/', [{'name': 'Author1'}, {'name': 'Author2'}])
    assert len(out) == 2

    a1 = Author.objects.get(name='Author1')
    out = cli.post_json(f'{BOOK}batch/', [{'title': 'book1_author1', 'author': a1.id},
                                          {'title': 'book2_author1', 'author': a1.id}])


def test_04_invalid(cli):
    cli.post_json(f'{AUTHOR}batch/', [{'name': 'Author1'}, {'name': 'Author2'}])
    a1 = Author.objects.get(name='Author1')
    with pytest.raises(APIError) as e:
        cli.post_json(f'{BOOK}batch/', [{'titlet': 'key', 'author': a1.id}])
    assert e.value.resp.status_code == 400, e.value.resp

    with pytest.raises(APIError) as e:
        cli.post_json(f'{BOOK}batch/', [{'title': 'book1_author1', 'author': -1}])
    assert e.value.resp.status_code == 400, e.value.resp


def test_05_invalid_single(cli):
    cli.post_json(f'{AUTHOR}batch/', [{'name': 'Author1'}, {'name': 'Author2'}])
    a1 = Author.objects.get(name='Author1')
    with pytest.raises(APIError) as e:
        cli.post_json(f'{BOOK}', {'titlet': 'key', 'author': a1.id})
    assert e.value.resp.status_code == 400, e.value.resp
