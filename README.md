Project Title: BMI Calculator with History and Trend Analysis Using Flask and MySQL

Project Description:
This project is a BMI (Body Mass Index) Calculator and Tracker that allows users to calculate their BMI and store it in a MySQL database for historical tracking and analysis. The web application, developed using Python’s Flask framework, provides a user-friendly interface for inputting weight, height, and user name. It calculates BMI, categorizes it, and saves the details to a MySQL database. Users can also view their BMI trends and history, represented in a line chart with interactive statistics.

Key Components:
Backend (Python with Flask):

The backend is developed using Flask to handle user input, perform BMI calculations, and communicate with a MySQL database.
Data is saved and retrieved from MySQL, enabling users to view past records.
It calculates BMI categories (Underweight, Normal, Overweight, Obese) and suggests an ideal weight range based on height.

Database (MySQL):

The MySQL database stores records of each BMI calculation along with the user name, date, weight, height, and BMI value.
This structured storage enables easy retrieval for historical analysis and trend visualization.

Frontend (HTML, CSS, Plotly):

HTML: The primary interfaces include a BMI calculation form, user selection dropdown, and display pages for results and history.
CSS: A simple style for form layouts, data tables, and navigation.
Plotly: Provides an interactive graph of BMI trends over time, visualizing BMI progression.

Features:

BMI Calculation: Calculates BMI based on user input, categorizes it, and displays it with suggestions.
Historical Records: Users can view their past BMI records, date-wise.
Trend Analysis: Line chart of BMI trends over time with statistics like the latest, average, minimum, and maximum BMI values.
User Selection: Dropdown to select and view BMI history for different users.

Usage:

Launch the application, enter the weight, height, and name to calculate and save BMI.
View past records by selecting a user from the dropdown.
Access a trend analysis with BMI history, view statistics, and track fitness progress.
This project is an excellent application of Flask with MySQL, providing practical functionality for tracking and visualizing BMI over time in a visually engaging way.
