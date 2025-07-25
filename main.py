from database import  engine, SessionLocal
from models  import Base
from seed import seed

print("Création des tables...")

if __name__ == "__main__":

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed(db)
    db.close()


# Base.metadata.create_all(bind=engine)
print("Fait.")
