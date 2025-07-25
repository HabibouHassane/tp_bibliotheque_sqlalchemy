from models import *
import datetime


def list_books_with_authors(session):  #afficher tous les livres avec leur auteur
    books = session.query(Book).join(Book.author).all()
    for book in books:
        print(f"{book.title} ({book.year}) - Auteur : {book.author.name}")



def loan_book(session, book_id, member_id): # créer un prêt
        data = {
            "book_id": book_id,
            "book_id": member_id,
            "loan_date": "loan_date": datetime.datetime.now()
        }
        loan = Loan.create(session, data)
        return loan

def show_loans_for_member(session, member_id): #lister les prêts d'un membre
    return Loan.get_loans_by_member(session, member_id)


def return_book(session, loan_id):
    loan = session.get(Loan, loan_id)
    if not loan:
        print(f"Emprunt avec ID {loan_id} introuvable.")
        return

    if loan.return_date is not None:
        print(f"L'emprunt {loan_id} a déjà été retourné le {loan.return_date}.")
        return

    loan.return_date = datetime.datetime.now().date()
    session.commit()
    print(f"L'emprunt {loan_id} a bien été marqué comme retourné.")

def delete_member(session, member_id):
    loans = show_loans_for_member(session, member_id)

    has_active_loans = any(loan.return_date is None for loan in loans)
    if has_active_loans:
        print("Impossible de supprimer le membre : prêts actifs existants.")
        return

    session.query(Member).filter(Member.id == member_id).delete()
    session.commit()
    print(f"Membre {member_id} supprimé avec succès.")
  