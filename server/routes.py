from flask import jsonify, request, make_response
from models import db, List, Item, ListItems, Store, Purchase

def register_routes(app):

    @app.route("/")
    def index():
        return "<h1>Grocery List App</h1>"

    @app.route('/lists', methods=['GET'])
    def get_lists():
        lists = List.query.all()
        result = [{
            'id': list_.id,
            'title': list_.title
        } for list_ in lists]
        
        return jsonify(result)

    @app.route('/lists/<int:id>', methods=['GET'])
    def get_list(id):
        list_ = db.session.get(List, id)
        if list_:
            return jsonify(list_.to_dict())
        return make_response(jsonify({"error": "List not found"}), 404)

    @app.route('/lists', methods=['POST'])
    def create_list():
        data = request.get_json()
        new_list = List(title=data['title'])
        db.session.add(new_list)
        db.session.commit()
        return jsonify(new_list.to_dict()), 201

    @app.route('/lists/<int:id>', methods=['DELETE'])
    def delete_list(id):
        list_ = db.session.get(List, id)
        if list_:
            db.session.delete(list_)
            db.session.commit()
            return make_response("", 204)
        return make_response(jsonify({"error": "List not found"}), 404)

    @app.route('/items', methods=['GET'])
    def get_items():
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items])

    @app.route('/list_items', methods=['POST'])
    def create_list_item():
        data = request.get_json()
        try:
            new_list_item = ListItems(
                quantity=data["quantity"],
                list_id=data["list_id"],
                item_id=data["item_id"]
            )
            db.session.add(new_list_item)
            db.session.commit()
            return jsonify(new_list_item.to_dict()), 201
        except Exception as e:
            return make_response(jsonify({"errors": ["validation errors"]}), 400)

    @app.route('/purchases', methods=['GET'])
    def get_purchases():
        purchases = Purchase.query.all()
        return jsonify([purchase.to_dict() for purchase in purchases])
