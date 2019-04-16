from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, User, CatalogItem, Category

# For Auth
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False}, echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

login_output = ""

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state

    loggedIn = hasValidLogin()
    global login_output
    if loggedIn and login_output == "":
        login_output = getProfileHTML()

    return render_template('login.html', STATE=state, loggedin=hasValidLogin(), login_output=login_output)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Tokens client ID does not match apps.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    return getProfileHTML()

def getProfileHTML():
    output = ''
    output += '<div style="display: flex; align-items: center; justify-content: center;">'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 60px; height: 60px; border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    output += '<div style="padding-top:10px;padding-left:10px;padding-right:10px;"><font color="white">'
    output += login_session['username']
    output += '</font>'
    output += '<a href="/gdisconnect" style="margin:10px;display:block;"> <button style="width: 100%; font-size: 13px; border-radius: 10px; padding:3px;">Logout</button> </a>'
    output += '</div></div>'

    print(output)

    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        
    print(response)
    return redirect(url_for('showCategories'))

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
    return render_template('catalogCategories.html', categories=category, loggedin=hasValidLogin())


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

# Show a category items
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showItems(category_id):
    categories = session.query(Category).all()

    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('catalogItems.html', items=items, category=category, categories=categories, loggedin=hasValidLogin())

# Create a new catalog item
@app.route(
    '/category/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
    if not hasValidLogin():
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form[
                           'description'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newCatalogItem.html', category_id=category_id)


# Edit a catalog item
@app.route('/category/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editCatalogItem(category_id, item_id):
    if not hasValidLogin():
        return redirect(url_for('showLogin'))

    categories = session.query(Category).all()

    editedItem = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
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
    if not hasValidLogin():
        return redirect(url_for('showLogin'))

    itemToDelete = session.query(CatalogItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteCatalogItem.html', item=itemToDelete)

def hasValidLogin():
    if 'username' not in login_session:
        return False;
    else:
        return True;


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)