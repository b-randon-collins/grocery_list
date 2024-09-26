from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    list_items = db.relationship('ListItems', backref='item', cascade="all, delete")
    purchases = db.relationship('Purchase', backref='item', cascade="all, delete")

    def __repr__(self):
        return f"<Item {self.name}>"

class List(db.Model, SerializerMixin):
    __tablename__ = 'lists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    list_items = db.relationship('ListItems', backref='list', cascade="all, delete")

    def __repr__(self):
        return f"<List {self.title}>"

class ListItems(db.Model, SerializerMixin):
    __tablename__ = 'list_items'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False) 
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    def __repr__(self):
        return f"<ListItems: List {self.list_id}, Item {self.item_id}, Quantity {self.quantity}>"

class Store(db.Model, SerializerMixin):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    purchases = db.relationship('Purchase', backref='store', cascade="all, delete")

    def __repr__(self):
        return f"<Store {self.name}>"

class Purchase(db.Model, SerializerMixin):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    def __repr__(self):
        return f"<Purchase: Store {self.store_id}, Item {self.item_id}, Price {self.price}, Date {self.purchase_date}>"
