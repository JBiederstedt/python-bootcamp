import os
from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# determine absolute path to the database file
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'cafes.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))

# HTML template for listing cafes
index_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cafe List</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body class="container">
    <h1 class="mt-4 mb-4">Cafe List</h1>
    <a href="{{ url_for('add_cafe') }}" class="btn btn-primary mb-3">Add New Cafe</a>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Name</th>
                <th>Image</th>
                <th>Location</th>
                <th>Seats</th>
                <th>Price</th>
                <th>Wifi</th>
                <th>Sockets</th>
                <th>Toilet</th>
                <th>Calls</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for cafe in cafes %}
            <tr>
                <td>{{ cafe.name }}</td>
                <td><img src="{{ cafe.img_url }}" alt="{{ cafe.name }}" width="100"></td>
                <td><a href="{{ cafe.map_url }}" target="_blank">{{ cafe.location }}</a></td>
                <td>{{ cafe.seats or 'N/A' }}</td>
                <td>{{ cafe.coffee_price or 'N/A' }}</td>
                <td>{{ '✅' if cafe.has_wifi else '❌' }}</td>
                <td>{{ '✅' if cafe.has_sockets else '❌' }}</td>
                <td>{{ '✅' if cafe.has_toilet else '❌' }}</td>
                <td>{{ '✅' if cafe.can_take_calls else '❌' }}</td>
                <td>
                    <a href="{{ url_for('delete_cafe', cafe_id=cafe.id) }}" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure you want to delete this cafe?');">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>"""

# HTML template for adding a new cafe
add_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add New Cafe</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body class="container">
    <h1 class="mt-4 mb-4">Add New Cafe</h1>
    <form method="POST">
        <div class="form-group">
            <label>Name</label>
            <input class="form-control" type="text" name="name" required>
        </div>
        <div class="form-group">
            <label>Map URL</label>
            <input class="form-control" type="url" name="map_url" required>
        </div>
        <div class="form-group">
            <label>Image URL</label>
            <input class="form-control" type="url" name="img_url" required>
        </div>
        <div class="form-group">
            <label>Location</label>
            <input class="form-control" type="text" name="location" required>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="has_sockets" id="has_sockets">
            <label class="form-check-label" for="has_sockets">Has Sockets</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="has_toilet" id="has_toilet">
            <label class="form-check-label" for="has_toilet">Has Toilet</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="has_wifi" id="has_wifi">
            <label class="form-check-label" for="has_wifi">Has Wifi</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="can_take_calls" id="can_take_calls">
            <label class="form-check-label" for="can_take_calls">Can Take Calls</label>
        </div>
        <div class="form-group">
            <label>Seats</label>
            <input class="form-control" type="text" name="seats">
        </div>
        <div class="form-group">
            <label>Coffee Price</label>
            <input class="form-control" type="text" name="coffee_price">
        </div>
        <button type="submit" class="btn btn-success">Add Cafe</button>
        <a href="{{ url_for('home') }}" class="btn btn-secondary">Cancel</a>
    </form>
</body>
</html>"""

@app.route('/')
def home():
    cafes = Cafe.query.all()
    return render_template_string(index_template, cafes=cafes)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form['name'],
            map_url=request.form['map_url'],
            img_url=request.form['img_url'],
            location=request.form['location'],
            has_sockets=bool(request.form.get('has_sockets')),
            has_toilet=bool(request.form.get('has_toilet')),
            has_wifi=bool(request.form.get('has_wifi')),
            can_take_calls=bool(request.form.get('can_take_calls')),
            seats=request.form.get('seats'),
            coffee_price=request.form.get('coffee_price')
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template_string(add_template)

@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
