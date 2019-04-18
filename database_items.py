"""This file creates some mock items and categories and inserts the data into the database."""

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


# Catalog Items Mock
catalogItem1 = CatalogItem(name="Ball - Wilson", description="Good ball for practice tennis, usually used for the tournament, The duration is around two months. Mostly used on the fast tennis court.",
                     owner=user1, category=category1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Mattress", description="Soft and delicious mattress for yoga. The size is perfect and is super comfy for you to have a good time at a yoga class. Colors available: Green, Yellow, Red, and Black. Easy to roll and store in any place.",
                     owner=user2, category=category2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Cycling Shoes", description="Shoes for spinning, mountain bike, and outside bikes. This is great for your security, feel comfortable to go fast and potentialize your training. This has three special plugs, so it is easily adaptable to the various bike models. All sizes are available.Shoes for spinning, mountain bike, and outside bikes. This is great for your security, feel comfortable to go fast and potentialize your training. This has three special plugs, so it is easily adaptable to the various bike models. All sizes are available.",
                     owner=user1, category=category3)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(name="Kimono KVRA", description="Best kimono ever, durability, beautiful are the main characteristics. Color available: Black and White.",
                     owner=user1, category=category4)

session.add(catalogItem4)
session.commit()


catalogItem5 = CatalogItem(name="KVRA Hash", description="Hash for training jiu-jitsu. Really comfortable and will help keep you dry. Many patterns and sizes are available. All champions use this hash, don't hesitate to buy!",
                     owner=user2, category=category4)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(name="Swimming goggles", description="Swimming goggles for swimming comfortable and have a perfect time under the water. The glass is from a high-quality material that makes your view very clear during all the training.",
                     owner=user2, category=category6)

session.add(catalogItem6)
session.commit()

catalogItem7 = CatalogItem(name="Swimming cap", description="Swimming cap from all sizes. Don't squish your head either break your hair! Really comfy, try it!",
                     owner=user2, category=category6)

session.add(catalogItem7)
session.commit()

catalogItem8 = CatalogItem(name="Swimsuit", description="Swimsuit made with high-quality material. Many patterns, and sizes available. You swim and don't get wet, it is incredible.",
                     owner=user1, category=category6)

session.add(catalogItem8)
session.commit()

print("added catalog items!")