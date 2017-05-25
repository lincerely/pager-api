#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from tinydb import TinyDB, Query
import shortuuid

app = Flask(__name__)
db = TinyDB('messages.json')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}), 404)

@app.route('/pager/<string:uid>', methods=['GET'])
def get_text(uid):
    message = Query()
    msg = db.get(message.id == uid)
    if msg is None:
        abort(404)
    return jsonify(msg)

@app.route('/pager/new', methods=['GET','PUT','POST'])
def create_user():
    msg = {
        "id":shortuuid.uuid(),
        "text":request.args.get('text','')
    }
    db.insert(msg)
    return jsonify(msg),201

@app.route('/pager/<string:uid>', methods=['PUT','POST','GET'])
def update_text(uid):
    message = Query()
    db.update({'text':request.args.get('text','')},message.id == uid)
    return get_text(uid)

if __name__ == '__main__':
    app.run(debug=True)
