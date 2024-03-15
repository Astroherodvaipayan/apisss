from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/postgres'
db = SQLAlchemy(app)

class Schema1(db.Model):
    __tablename__ = 'banks1'
    __table_args__ = {'schema':'schema1'}     
    ID = db.Column(db.Integer, primary_key=True)
    Age = db.Column(db.Integer)
    month = db.Column(db.String(50))
    SSN = db.Column(db.String(50))
    annual_income = db.Column(db.Float)
    Num_credit_card = db.Column(db.Integer)
    Num_of_loan = db.Column(db.Integer)
    Credit_History_age = db.Column(db.Integer)
    Credit_Score = db.Column(db.Integer)
    Outstanding_Debt = db.Column(db.Float)
    # New column to store model predictions
    Model_Prediction = db.Column(db.Integer)

@app.route('/query', methods=['GET'])
def query_schema1():
    # Query the database using SQLAlchemy to get only the required columns
    results = db.session.query(Schema1.ID, Schema1.Age, Schema1.month, Schema1.SSN, Schema1.annual_income, Schema1.Num_credit_card, Schema1.Num_of_loan, Schema1.Credit_History_age, Schema1.Credit_Score, Schema1.Outstanding_Debt).all()
    
    # Convert results to pandas DataFrame
    df = pd.DataFrame(results, columns=['ID', 'Age', 'month', 'SSN', 'annual_income', 'Num_credit_card', 'Num_of_loan', 'Credit_History_age', 'Credit_Score', 'Outstanding_Debt'])
    
    # Separate features and target
    X = df.drop(columns=['ID', 'month', 'SSN'])
    y = df['SSN']  # Example target column, change it to your actual target
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    
    # Store the accuracy score back into the database
    for index, row in df.iterrows():
        entry = Schema1.query.filter_by(ID=row['ID']).first()
        entry.Model_Prediction = y_pred[index]  # Storing predictions in the new column
    
    db.session.commit()  # Commit changes
    
    # Return the accuracy score
    return jsonify({'accuracy': accuracy})

if __name__ == '__main__':
    app.run(debug=True)
