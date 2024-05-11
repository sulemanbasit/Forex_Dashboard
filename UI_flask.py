from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route("/")
def home():
        # Read the CSV file
    data = pd.read_csv("test.csv")

    # Group data by 'Type' column
    grouped_data = data.groupby('Type')

    # Convert the grouped data into a dictionary
    data_dict = {group: group_data.to_dict('records') for group, group_data in grouped_data}
    
    return render_template("index.html", data_dict=data_dict)

if __name__ == "__main__":
    app.run(debug=True)