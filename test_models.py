from models import *

author1 = Author(id=1, name="Abdoul Nasser")
book = Book(title="Les Misérables", year=1862, author=author1)
author_data = {
    "name":"Abdoul nasser"
}

def test_list_all(mocker):
    session = mocker.MagicMock()
    session.query.return_value.all.return_value = [book] 


    got = Book.list_all(session)

    assert got == [book] 
    session.query.return_value.all.assert_called_once()

def test_create(mocker):
    session = mocker.MagicMock()

    Author.create(session, author_data)
    session.add.assert_called_once()
    session.commit.assert_called_once

def test_as_dict():
    excepted = {
        "id" : 1,
        "name":"Abdoul Nasser"
    }

    assert excepted == Author(id=1,name="Abdoul Nasser").as_dict()

def test_get_books_by_author(mocker):
    session=mocker.MagicMock()
    session.query.return_value.filter.return_value.all.return_value = [book]

    assert Book.get_books_by_author(session,1) == [book]

    session.query.return_value.filter.assert_called_once()


 
