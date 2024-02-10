from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/postgres'
db = SQLAlchemy(app)

class Schema1(db.Model):
    __tablename__ = 'banks1'
    __table_args__ = {'schema':'schema1'}     
    ID = db.Column(db.Integer, primary_key=True)
    # Add other columns as needed

@app.route('/query', methods=['GET'])
def query_schema1():
    # Query the database using SQLAlchemy
    results = Schema1.query.all()
    
    # Convert SQLAlchemy model objects to dictionary representations
    results_dict = [{'ID': result.ID} for result in results]
    
    # Return the results as JSON using jsonify
    return jsonify(results_dict)

if __name__ == '__main__':
    app.run(debug=True)
