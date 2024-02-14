from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='static')

app.config['SECRET_KEY'] = 'supersecretkey!'

# Forms
class SearchForm(FlaskForm):
    query = StringField("Search for patient by first name.", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Load data
    df = pd.read_csv('./data/patient_tb.csv')
    # Remove duplicates
    cleaned_data = df.drop_duplicates(
        subset=['MostRecentTestDate', 'TestName'], 
        keep='first')
    
    # Form to query patients
    form = SearchForm()
    
    # POST
    if form.validate_on_submit():
        query = request.form.get('query')
        query = query.capitalize()
        results = cleaned_data.loc[cleaned_data['PatientFirstName'] == query]
        return render_template('search.html', 
                               results=results.to_html(classes='table is-striped'),
                               name=query)

    # GET
    return render_template('search.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,
            debug=True)