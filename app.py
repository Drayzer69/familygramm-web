from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///familygramm.db'
db = SQLAlchemy(app)
CORS(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)
    author = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': p.id, 
        'text': p.text, 
        'likes': p.likes,
        'author': p.author
    } for p in posts])

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    post = Post(text=data['text'], author=data['author'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Пост добавлен!'})

@app.route('/')
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

