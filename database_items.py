from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import CatalogItem, Base, Category, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Users
user1 = User(id="feerzinha@gmail.com", name="Fernanda")

session.add(user1)
session.commit()

user2 = User(id="fernanda.moya@udacity.com", name="Fernanda")

session.add(user2)
session.commit()


# Catalog Category
category1 = Category(name="Tenis")

session.add(category1)
session.commit()

category2 = Category(name="Yoga")

session.add(category2)
session.commit()

category3 = Category(name="Spinning")

session.add(category3)
session.commit()

category4 = Category(name="Jiu-jitsu")

session.add(category4)
session.commit()

category5 = Category(name="Karate")

session.add(category5)
session.commit()

category6 = Category(name="Swimming")

session.add(category6)
session.commit()


# Catalog Items

catalogItem1 = CatalogItem(name="Ball Wilson", description="Good ball for practice tenis",
                     owner=user1, category=category1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Mattress", description="Soft and delicious for yoga.",
                     owner=user2, category=category2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Cycling Shoes", description="Shoes for spinning",
                     owner=user1, category=category3)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(name="Kimono KVRA", description="Best kimono ever, durability, beautiful.",
                     owner=user1, category=category4)

session.add(catalogItem4)
session.commit()


catalogItem5 = CatalogItem(name="KVRA Hash", description="Hash for jiu jitsu champions.",
                     owner=user2, category=category4)

session.add(catalogItem5)
session.commit()

print("added catalog items!")