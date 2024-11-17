This project is a Flask application that analyzes traffic events in Paris, including data extraction, transformation, and visualization
1)Installation
2)Clone the repository:
git clone https://github.com/AmineAchour/paris_events.git
cd Paris_events
3)Install Dependencies: Install the required Python packages:
pip install -r requirements.txt
4)Database Setup:
4.1)Ensure MySQL is running and accessible.
4.2)Modify database connection details in app.py as needed.
5)Run the flask APP :
python app.py
6)Usage
6.1)Access the app at http://127.0.0.1:5000.
6.2)View data visualizations on the home page.

File Structure
app.py: Main application script.
requirements.txt: List of Python dependencies.
static/: Directory for static files (e.g., images).
templates/: HTML templates for rendering views.
Requirements
Python 3.x
Flask
MySQL
pandas
matplotlib
requests
