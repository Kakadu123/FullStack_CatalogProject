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
        'categories2.html', category=category, items=items, category_name=category_name)


@app.route('/catalog/<category_name>/<item_name>/show')
def itemDetail(category_name, item_name):
    category = session.query(Categories).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(name=item_name).one()
    return render_template(
        'detail.html', item_desc=items.description, item_name=item_name, category_name=category_name)





if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
