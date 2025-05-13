from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

# MySQL Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",  # Update with your MySQL host
        user="root",       # Update with your MySQL username
        password="1234",  # Update with your MySQL password
        database="bmi_db"  # Name of your database
    )

# BMI Category Calculation
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Suggested weight range for normal BMI
def get_suggested_weight(height_m):
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    return round(min_weight, 1), round(max_weight, 1)

# Home Page: BMI Calculator Form and User History Dropdown
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch all distinct user names
    cursor.execute("SELECT DISTINCT name FROM bmi_data")
    users = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', users=users)

# Route to calculate BMI and save the result
@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height']) / 100  # Convert cm to meters

        # BMI Calculation
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
        category = get_bmi_category(bmi)

        # Suggested weight range for normal BMI
        suggested_min, suggested_max = get_suggested_weight(height)

        # Date of calculation
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Save to MySQL Database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bmi_data (name, date, weight, height, bmi) VALUES (%s, %s, %s, %s, %s)",
                       (name, date, weight, height * 100, bmi))
        conn.commit()
        conn.close()

        return render_template('result.html', name=name, bmi=bmi, category=category, suggested_min=suggested_min, suggested_max=suggested_max)

# User's BMI History and Trend Analysis
@app.route('/history/<name>')
def history(name):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch all stored data for the user
    cursor.execute("SELECT date, weight, height, bmi FROM bmi_data WHERE name = %s ORDER BY date", (name,))
    rows = cursor.fetchall()
    
    conn.close()

    # Prepare data for graph and history table
    if rows:
        df = pd.DataFrame(rows, columns=['date', 'weight', 'height', 'bmi'])
        
        # Create a BMI trend line graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['bmi'], mode='lines+markers', name='BMI Trend'))
        fig.update_layout(title='BMI Trend Over Time', xaxis_title='Date', yaxis_title='BMI')
        graph = fig.to_html(full_html=False)
        
        # Generate statistics for the user
        latest_bmi = df['bmi'].iloc[-1]
        avg_bmi = df['bmi'].mean()
        max_bmi = df['bmi'].max()
        min_bmi = df['bmi'].min()

        stats = {
            "latest_bmi": latest_bmi,
            "avg_bmi": round(avg_bmi, 2),
            "max_bmi": round(max_bmi, 2),
            "min_bmi": round(min_bmi, 2)
        }
    else:
        graph = None
        stats = None

    return render_template('history.html', name=name, graph=graph, data=rows, stats=stats)

# Route to view history by selecting a user
@app.route('/view-history', methods=['POST'])
def view_history():
    selected_user = request.form['user']
    return redirect(url_for('history', name=selected_user))

if __name__ == '__main__':
    app.run(debug=True)
