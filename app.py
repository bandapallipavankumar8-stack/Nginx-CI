import csv
import os
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# File path where data spreadsheet will be saved permanently
DATA_FILE = '/usr/share/nginx/html/poultry_data.csv'

def save_to_csv(data_dict):
    file_exists = os.path.isfile(DATA_FILE)
    
    # Open CSV file in append mode
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data_dict.keys())
        
        # Write headers if the file is brand new
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(data_dict)

@app.route('/save-data', methods=['POST'])
def save_data():
    try:
        # Extract form field parameters sent by user
        form_data = {
            "Date": request.form.get("log_date"),
            "Shed_ID": request.form.get("shed_id"),
            "Total_Birds": request.form.get("total_birds"),
            "Mortality": request.form.get("mortality"),
            "Eggs_Collected": request.form.get("eggs_collected"),
            "Damaged_Eggs": request.form.get("damaged_eggs"),
            "Feed_Consumed_KG": request.form.get("feed_consumed"),
            "Remarks": request.form.get("remarks", "").replace("\n", " ")
        }
        
        # Save to local CSV file data block
        save_to_csv(form_data)
        
        # Return success screen notification
        return """
        <html>
            <body style="font-family:Arial; text-align:center; padding-top:50px; background-color:#f4f7f6;">
                <div style="background:white; display:inline-block; padding:30px; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color:#27ae60;">✅ Data Saved Successfully!</h2>
                    <p>Today's metrics have been logged into the poultry database sheet.</p>
                    <a href="/" style="background:#27ae60; color:white; padding:10px 20px; text-decoration:none; border-radius:4px;">Back to Form</a>
                </div>
            </body>
        </html>
        """
    except Exception as e:
        return f"An error occurred while saving records: {str(e)}", 500

if __name__ == '__main__':
    # Run application locally on port 5000
    app.run(host='0.0.0.0', port=5000)
