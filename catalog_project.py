from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, User, CatalogItem, Category

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False}, echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

# Base = declarative_base()
#
# #engine = create_engine('sqlite:///catalog.db')
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()


#TODO: Build a better json - unique
@app.route('/category/<int:category_id>/items/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return jsonify(CatalogItem=[i.serialize for i in items])


@app.route('/catalog/JSON')
def catalogJSON():
    # TODO: Build a better json - unique
    #Concat all infos and return
    catalog = session.query(Category).all()
    return jsonify(catalog=[r.serialize for r in catalog])


# Show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    category = session.query(Category).all()
    # return "This page will show all my categories"
    return render_template('catalogCategories.html', categories=category)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
    # return "This page will be for making a new category"


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            return redirect(url_for('showCategories'))
    else:
        return render_template(
            'editCategory.html', category=editedCategory)

    # return 'This page will be for editing category %s' % category_id

# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
    # return 'This page will be for deleting category %s' % category_id


# Show a category items
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showItems(category_id):
    categories = session.query(Category).all()

    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('catalogItems.html', items=items, category=category, categories=categories)
    # return 'This page is the category menu %s' % category_id

# Create a new catalog item
@app.route(
    '/category/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form[
                           'description'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newCatalogItem.html', category_id=category_id)
    # return 'This page is for making a new catalog item for category %s'
    # %category_id


# Edit a catalog item
@app.route('/category/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCatalogItem(category_id, item_id):
    categories = session.query(Category).all()

    editedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['category']:
            edited_category_id = request.form['category']
            edited_category =  session.query(Category).filter_by(id=edited_category_id).one()

            editedItem.category = edited_category
        #TODO: Manter o owner
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template(
            'editCatalogItem.html', category_id=category_id, item=editedItem, category_items=categories)

    # return 'This page is for editing catalog item %s' % catalog_item_id


# Delete a catalog item
@app.route('/category/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteCatalogItem(category_id, item_id):
    itemToDelete = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteCatalogItem.html', item=itemToDelete)
    # return "This page is for deleting catalog item %s" % item_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)