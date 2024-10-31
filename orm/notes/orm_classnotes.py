# DB Connection : 
# create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<datebase_name>)
# engine = create_engine("pastgresql+pyscopg2://postgres:csclass23@local/postgres")

# Define and Create Classes/ Tables 
class Base(DelarativeBase):
    pass
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str: #represents the object as string
        return f"User (id= {self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base) : 
    __tablename__ = "address"
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    email_address : Mapped[str] = mapped_column(String(40))
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address (id={self.id!r}, email_address={self.email_address!r})"

#Create Tables
Base.metadata.create_all(engine)

# Create Objects 
#insert data
with Session(engine) as session:
    spongebob = User(
        name = "spongebob",
        fullname = "Spongebob Squarepants",
        address = [Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name = "sandy",
        fullname = "Sandy Cheeks",
        address = [
            Address(email_address="sand@sqlachemy.org"),
        ],
    )
    patrick = User(name="patrick",fullname="Patrick Star")
    session.add_all([spongebob, sandy,patrick])
    session.commit()

# Simple Queries
session = Session(engine)
print(" ## User Table Content (1) ##")
stmt = select(User).where(User.name.in_(["spongebob","sandy"]))
for user in session.scalars(stmt): # excute stmt and return the results as scalars
    print(user)
print(" ## Address Table Content ##")
addresses = session.query(Address)
for address in addresses:
    print("Email Address: " + address.email_address)

# Join Query 
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)

sandy_address = session.scalars(stmt).one()
print("Sandy's Address: " + sandy_address.email_address)

# update and delete
sandy_address = session.scalars(stmt).one()
print("Sandy's Address: " + sandy_address.email_address)

#updates Sandy's email
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

#adds address for patrick
stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
session.commit()

# Show update addresses
print("\n ## Address Table Contents - After Update ##")
addresses = session.query(Address)
for address in addresses:
    print("Email Address: " + address.email_address)

# Deletes one of Sandy's email addresses (sand_cheeks@...)
sandy = session.get(User, 2) # 2 is the primaary key (id)
sandy.addresses.remove(sandy_address)
session.commit()

#shows updated addresses
print("\n ## Address Table Contents - After Delete ##")
addresses = session.query(Address)
for address in addresses:
    print("Email Address: " + address.email_address)
    
