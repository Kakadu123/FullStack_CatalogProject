from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

app = Flask(__name__)

engine = create_engine('sqlite:///categoriesDB.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def homePage():
    category = session.query(Categories).all()
    items = session.query(Items).all()
    return render_template(
        'homePage.html', category=category, items=items)


@app.route('/catalog/<category_name>/items')
def categoryList(category_name):
    category = session.query(Categories).all()
    category_one = session.query(Categories).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category_id=category_one.id).all()
    return render_template(
        'categories.html', category=category, items=items, category_name=category_name)


@app.route('/catalog/<category_name>/<item_name>/show')
def itemDetail(category_name, item_name):
    category = session.query(Categories).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(name=item_name).one()
    return render_template(
        'detail.html', item_desc=items.description, item_name=item_name, category_name=category_name)


@app.route('/catalog/<string:category_name>/delete',methods=['GET', 'POST'])
def deleteItem(category_name):
    itemToDelete = session.query(Items).filter_by(name=category_name).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('homePage'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


@app.route('/catalog/<string:category_name>/edit', methods=['GET', 'POST'])
def editItem(category_name):
    editedItem = session.query(Items).filter_by(name=category_name).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('homePage'))
    else:
        return render_template('editItem.html', item=editedItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
