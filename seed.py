from sqlalchemy.orm import Session
from models import Author, Book, Member  


def seed(db: Session):
    
    author1 = Author(name="Abdoul Nasser")
    author2 = Author(name="Abdoul Aziz")

    
    member1 = Member(name="Abdoul Nasser", email="alice@example.com")
    member2 = Member(name="Abdoul Aziz", email="bob@example.com")

    
    book1 = Book(title="Les Misérables", year=1862, author=author1)
    book2 = Book(title="Pride and Prejudice", year=1813, author=author2)

    
    db.add_all([author1, author2, member1, member2, book1, book2])

    
    db.commit()


