"""This file creates the necessary classes for the catalog database."""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#DATABASE_PATH = os.path.join(BASE_DIR, 'catalog.db')

class User(Base):
    """This class is used for store users informations and will be used to record creations and deletions on the future."""

    __tablename__ = 'user'

    id = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'name': self.name,
            'id': self.id,
        }


class Category(Base):
    """This table is for store the available categories."""

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'name': self.name,
            'id': self.id,
        }


class CatalogItem(Base):
    """This table is for store the available items."""
    
    __tablename__ = 'catalog_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(5050))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, backref='items')
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id,
        }


engine = create_engine('sqlite:///'+ '/home/grader/nd_project/catalog-site/catalog.db')

Base.metadata.create_all(engine)
