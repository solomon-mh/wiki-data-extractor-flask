from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)  # Nullable to handle single names
    birth_city = db.Column(db.String(100))
    early_life = db.Column(db.String(250))

    def __repr__(self):
        return f'<Person {self.first_name} {self.last_name or ""}>'

