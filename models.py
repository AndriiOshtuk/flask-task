from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class WishList(db.Model):
    __tablename__ = "wishlist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    due_date = db.Column(db.Date)
    gifts = db.relationship("Gift", backref="wishlist", lazy=True)

    def __repr__(self):
        return "<WishList %d:%r>" % (self.id, self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Gift(db.Model):
    __tablename__ = "gift"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=True)
    url = db.Column(db.Text, unique=False, nullable=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlist.id"), nullable=False)

    def __repr__(self):
        return "<Gift %d:%r>" % (self.id, self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
