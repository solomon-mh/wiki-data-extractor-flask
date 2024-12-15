from flask import Flask, render_template, request, redirect, url_for
from models.models import db, Person
from werkzeug.exceptions import HTTPException
from utils.utils import extract_early_life, extract_birth_city_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure the tables are created before running the app
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_names', methods=['POST'])
def submit_names():
    names = request.form['names'].split(',')
    for name in names:
        name = name.strip()
        if Person.query.filter_by(first_name=name.split()[0], last_name=name.split()[1]).first():
            # Skip if person already exists
            continue
        
        data = fetch_wikipedia_data(name)
        if data:
            person = Person(
                first_name=data['first_name'],
                last_name=data['last_name'],
                birth_city=data['birth_city'],
                early_life=data['early_life']
            )
            db.session.add(person)
    db.session.commit()
    return redirect(url_for('all_people'))

@app.route('/person/<int:id>')
def person_details(id):
    person = Person.query.get(id)
    if person is None:
        # If person not found, return a 404 error page
        return render_template('404.html'), 404
    return render_template('details.html', person=person)

@app.route('/all_people')
def all_people():
    people = Person.query.order_by(Person.id.desc()).all()  # Get all people in reverse order
    return render_template('all_people.html', people=people)

def fetch_wikipedia_data(name):
    """
    Fetches data using BeautifulSoup and Wikipedia API to extract birth city and early life details.
    """
    try:
        # Extract birth city using BeautifulSoup
        birth_city = extract_birth_city_info(name)
        print(birth_city)

        # Extract early life using wikipedia-api
        early_life = extract_early_life(name)

        first_name, last_name = name.split(' ', 1)

        return {
            'first_name': first_name,
            'last_name': last_name,
            'birth_city': birth_city,
            'early_life': early_life
        }
    except Exception as e:
        print(f"Error fetching data for {name}: {e}")
        return None

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
