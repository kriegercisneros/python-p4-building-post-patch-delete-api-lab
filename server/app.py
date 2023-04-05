#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    #patch to update the name of the bakery in db and returns as json, request will be sent in a form 
    #which doesn't need to include values for all the bakeries attributes
    bakery = Bakery.query.filter_by(id=id).first()

    if request.method=='GET':

        bakery_serialized = bakery.to_dict()

        response = make_response(
            jsonify(bakery_serialized),
            200
        )
        return response
    elif request.method=='PATCH':
        #updates the name of the bakery
        ##please take time to understand what these lines of code are doing
        for attr in request.form:
            #uses the set attribute function to set the attribute of the bakery obj to the value provided in the request form data.  
            #attr is the name of the attribute being set and request.form.get(attr) is the value being set for the attribute
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        backery_dict = bakery.to_dict()

        response = make_response(
            jsonify(backery_dict), 200
        )
        return response

@app.route('/baked_goods', methods=['GET','POST'])
def baked_goods():
    #this post block creates a new baked good in the db and returns its data as JSON.  the request till send data in a form
    if request.method =='GET':
        baked_goods = BakedGood.query.all()
        baked_goods_serialized = []
        for bg in baked_goods:
            baked_goods_serialized.append(bg.to_dict())
            
    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        )

    db.session.add(new_baked_good)
    db.session.commit()

    baked_good_dict = new_baked_good.to_dict()

    response = make_response(
        jsonify(baked_good_dict), 201
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_by_id():
    baked_good = BakedGood.query.filter_by(id=id).first()
    if request.method == 'GET':
        baked_good_dict = baked_good.to_dict()

        response=make_response(
            jsonify(baked_good_dict), 200
        )
        return response
    
    elif request.method == 'DELETE':
        #delete baked good from the db and returns a json message confirming the record was deleted
        db.session.delete(baked_good)
        db.session.commit()

        response_dict = {'message': 'record successfully deleted'}

        response=make_response(
            jsonify(response_dict), 200
        )
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
