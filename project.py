# Import of resources
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# ClientID retrieved from client_secrets.json
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Animal Catalog Application"

# database stored in categoriesDB.db file
engine = create_engine('sqlite:///categoriesDB.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# gconnect function handling Oauth 2.0 athentication
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
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Successfully disconnected.")
        return redirect('/catalog')
    else:
        # For whatever reason, the given token was invalid.
        flash("Failed to revoke token for given user.")
        return redirect('/catalog')


# View rendering the main homepage
@app.route('/')
@app.route('/catalog/')
def homePage():
    category = session.query(Categories).all()
    items = session.query(Items).all()
    count = session.query(Items).count()
    # LogIn and Logout button hidden/shown based on authentication
    statusIn = 'visible'
    statusOut = 'none'
    if 'username' in login_session:
        statusIn = 'none'
        statusOut = 'visible'
    return render_template(
        'homePage.html', category=category, items=items, statusIn=statusIn,
        statusOut=statusOut, count=count)


# View rendering categories page
@app.route('/catalog/<string:category_name>/items')
def categoryList(category_name):
    category = session.query(Categories).all()
    category_one = session.query(Categories).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category_id=category_one.id).all()
    count = session.query(Items).filter_by(category_id=category_one.id).count()
    # LogIn and Logout button hidden/shown based on authentication
    statusIn = 'visible'
    statusOut = 'none'
    if 'username' in login_session:
        statusIn = 'none'
        statusOut = 'visible'
    return render_template('categories.html', category=category, items=items,
                           category_name=category_name,
                           statusIn=statusIn, statusOut=statusOut, count=count)


# View rendering detail of an item
@app.route('/catalog/<string:category_name>/<int:item_id>/show')
def itemDetail(category_name, item_id):
    category = session.query(Categories).filter_by(name=category_name).one()
    item = session.query(Items).filter_by(id=item_id).one()
    return render_template('detail.html', item=item, category_name=category_name)


# delete functionality
@app.route('/catalog/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('homePage'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# edit functionality
@app.route('/catalog/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        flash("Item has been edited!")
        return redirect(url_for('homePage'))
    else:
        category = session.query(Categories).all()
        return render_template('editItem.html', item=editedItem,
                               categories=category)


# add new item functionality
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        category_id=request.form['category'])
        session.add(newItem)
        session.commit()
        flash("New item has been created!")
        return redirect(url_for('homePage'))
    else:
        category = session.query(Categories).all()
        return render_template('newItem.html', categories=category)


# JSON endpoint
@app.route('/catalog.JSON')
def retrieveJSON():
    items = session.query(Items).all()
    categories = session.query(Categories).all()

    cArr = []
    for c in categories:
        iArr = []
        for i in items:
            if i.category_id == c.id:
                iArr.append({
                    "category_id": i.category_id,
                    "name": i.name,
                    "id": i.id,
                    "description": i.description,
                })

        cArr.append({
            "category_name": c.name,
            "category_id": c.id,
            "items": iArr
        })
    return jsonify({"Category": cArr})


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
