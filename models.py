from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from datetime import date
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    @classmethod
    def list_all(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def create(cls, db: Session, data: dict):
        instance = cls(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        # return instance

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        fields = ", ".join(f"{col.name}={getattr(self, col.name)!r}" for col in self.__table__.columns)
        return f"{self.__class__.__name__}({fields})"


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    # @classmethod
    # def get_by_name(cls, db: Session, name: str):
    #     return db.query(cls).filter(cls.name == name).first()



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

    @classmethod
    def get_books_by_author(cls, db: Session, author_id: int):
        return db.query(cls).filter(cls.author_id == author_id).all()



class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    loans: Mapped[list["Loan"]] = relationship(back_populates="member", cascade="all, delete-orphan")

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()



class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    loan_date: Mapped[date] = mapped_column()
    return_date: Mapped[date | None] = mapped_column(nullable=True)

    book: Mapped["Book"] = relationship(back_populates="loans")
    member: Mapped["Member"] = relationship(back_populates="loans")

    @classmethod
    def get_loans_by_book(cls, db: Session, book_id: int):
        return db.query(cls).filter(cls.book_id == book_id).all()

    @classmethod
    def get_loans_by_member(cls, db: Session, member_id: int):
        return db.query(cls).filter(cls.member_id == member_id).all()

    @classmethod
    def get_active_loans(cls, db: Session):
        return db.query(cls).filter(cls.return_date == None).all()

    
