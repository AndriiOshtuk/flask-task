import datetime

import config
from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from models import db, WishList, Gift


app = Flask(__name__)
app.debug = config.DEBUG
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)


@app.route("/about/")
def about():
    """
    This function checks the running API status.

    Return the "Alive!" string if the API is well running.
    """
    db.create_all()
    return jsonify(status="Alive!")


ma = Marshmallow(app)


class GiftSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gift
        include_fk = True


class WishlistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WishList

    id = ma.auto_field()
    name = ma.auto_field()
    due_date = ma.auto_field()

    gifts = ma.Nested(GiftSchema, many=True)


wishlist_schema = WishlistSchema()
wishlists_schema = WishlistSchema(many=True)
gift_schema = GiftSchema()
gift_schemas = GiftSchema(many=True)


@app.route("/wishlist/")
def wishlist_list():
    """ Returns list of wishlists and related gifts as JSON """
    all_wishlists = WishList.query.all()
    return jsonify(wishlists_schema.dump(all_wishlists))


@app.route("/wishlist/", methods=["POST"])
def create_wishlist():
    """ Create wishlist """
    name = request.json.get("name", "")
    due_date = request.json.get("due_date", "")

    datetime_object = datetime.datetime.strptime(due_date, "%Y-%m-%d")

    wishlist = WishList(name=name, due_date=datetime_object)

    db.session.add(wishlist)
    db.session.commit()

    return wishlist_schema.jsonify(wishlist)


@app.route("/wishlist/<id>")
def wishlist_detail(id):
    """ Returns single wishlists and related gifts as JSON """
    wishlist = WishList.query.get(id)
    return wishlist_schema.jsonify(wishlist)


@app.route("/gift/<id>")
def gift_detail(id):
    """ Returns single gift as JSON """
    gift = Gift.query.get(id)
    return gift_schema.jsonify(gift)


@app.route("/gift/", methods=["POST"])
def create_gift():
    """ Create gift """
    name = request.json.get("name", "")
    description = request.json.get("description", "")
    price = request.json.get("price", 0.0)
    url = request.json.get("url", "")
    wishlist_id = request.json.get("wishlist_id", "")

    gift = Gift(
        name=name,
        description=description,
        price=price,
        url=url,
        wishlist_id=wishlist_id,
    )

    db.session.add(gift)
    db.session.commit()

    return gift_schema.jsonify(gift)


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
