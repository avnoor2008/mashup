import os
import sys
import smtplib
import subprocess
import zipfile
import uuid
import logging
from email.message import EmailMessage
from flask import Flask, request, render_template_string
from dotenv import load_dotenv

# --- SETUP & CONFIGURATION ---
load_dotenv()
app = Flask(__name__)

# Configure Logging (Debugging logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Credentials
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASS")
ROLL_NUMBER_SCRIPT = os.getenv("ROLL_NUMBER_SCRIPT", "102483084.py") # Default to your script

# --- FRONTEND ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mashup Generator</title>
    <style>
        :root { --primary: #6366f1; --bg: #f8fafc; --text: #1e293b; }
        body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: white; padding: 2.5rem; border-radius: 1rem; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); width: 100%; max-width: 450px; }
        h2 { text-align: center; color: var(--primary); margin-bottom: 1.5rem; font-weight: 700; }
        .form-group { margin-bottom: 1.2rem; }
        label { display: block; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem; }
        input { width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 0.5rem; font-size: 1rem; transition: border 0.2s; box-sizing: border-box;}
        input:focus { border-color: var(--primary); outline: none; }
        button { width: 100%; padding: 0.85rem; background: var(--primary); color: white; border: none; border-radius: 0.5rem; font-size: 1rem; font-weight: 600; cursor: pointer; transition: transform 0.1s; }
        button:hover { background: #4f46e5; transform: translateY(-1px); }
        .note { font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }
        
        /* Loading Overlay */
        #loader { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255, 255, 255, 0.9); z-index: 50; flex-direction: column; justify-content: center; align-items: center; }
        .spinner { width: 50px; height: 50px; border: 5px solid #e2e8f0; border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>

    <div class="card">
        <h2>🎵 Mashup Studio</h2>
        <form action="/mashup" method="POST" onsubmit="showLoader()">
            <div class="form-group">
                <label>🎤 Singer Name</label>
                <input type="text" name="singer" required placeholder="e.g. The Weeknd">
            </div>
            
            <div class="form-group">
                <label>🎬 Number of Videos</label>
                <input type="number" name="count" required min="11" value="20">
                <div class="note">Must be greater than 10</div>
            </div>
            
            <div class="form-group">
                <label>⏱️ Clip Duration (Seconds)</label>
                <input type="number" name="duration" required min="21" value="30">
                <div class="note">Must be greater than 20</div>
            </div>
            
            <div class="form-group">
                <label>📧 Email Address</label>
                <input type="email" name="email" required placeholder="you@example.com">
            </div>
            
            <button type="submit">✨ Generate Mashup</button>
        </form>
    </div>

    <div id="loader">
        <div class="spinner"></div>
        <h3 style="color: #6366f1; margin-top: 1rem;">Generating your masterpiece...</h3>
        <p style="color: #64748b;">This may take 1-2 minutes. Please do not close this tab.</p>
    </div>

    <script>
        function showLoader() { document.getElementById('loader').style.display = 'flex'; }
    </script>
</body>
</html>
"""

def send_email_with_attachment(recipient_email, zip_path):
    """Sends the zip file via SMTP Securely."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        logging.error("Email credentials missing!")
        return False

    msg = EmailMessage()
    msg['Subject'] = "Your Custom Mashup is Ready! 🎧"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(
        "Hello,\n\n"
        "Your requested mashup has been successfully generated!\n"
        "Please find the zip file attached.\n\n"
        "Best regards,\n"
        "Mashup Web Service"
    )

    try:
        with open(zip_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(zip_path)
        
        msg.add_attachment(file_data, maintype='application', subtype='zip', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        
        logging.info(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/mashup', methods=['POST'])
def mashup():
    # 1. Generate Unique ID for this specific request (Safety against overwrites)
    request_id = str(uuid.uuid4())[:8]
    
    # 2. Get Data
    singer = request.form.get('singer').strip()
    try:
        count = int(request.form.get('count'))
        duration = int(request.form.get('duration'))
    except ValueError:
         return "<h2>Error: Invalid numeric inputs.</h2>"
    
    email = request.form.get('email').strip()

    # 3. Define unique filenames
    output_mp3 = f"mashup_{request_id}.mp3"
    output_zip = f"mashup_{request_id}.zip"

    # 4. Construct Command (Using list format is safer than shell=True)
    # python <script> <Singer> <Count> <Duration> <Output>
    command = [sys.executable, ROLL_NUMBER_SCRIPT, singer, str(count), str(duration), output_mp3]

    logging.info(f"[{request_id}] Starting mashup for {singer}...")
    
    try:
        # 5. Run the background script
        process = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        # 6. Verify MP3 Creation
        if not os.path.exists(output_mp3):
            logging.error(f"Script failed: {process.stderr}")
            return f"<h2>Generation Failed</h2><p>Script output:</p><pre>{process.stderr}</pre>"

        # 7. Create ZIP File (Assignment Requirement)
        logging.info(f"[{request_id}] Zipping file...")
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(output_mp3)

        # 8. Send Email
        logging.info(f"[{request_id}] Sending email to {email}...")
        success = send_email_with_attachment(email, output_zip)

        # 9. Response
        if success:
            return f"""
            <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                <h1 style="color: #6366f1;">Success! 🎉</h1>
                <p style="font-size: 1.2rem;">The mashup <b>{singer}</b> has been sent to <b>{email}</b>.</p>
                <a href='/' style="color: #6366f1; text-decoration: none; font-weight: bold;">Create Another</a>
            </div>
            """
        else:
            return "<h2>Error</h2><p>Mashup created, but email failed. Check server logs.</p>"

    except subprocess.CalledProcessError as e:
        return f"<h2>Script Error</h2><pre>{e.stderr}</pre>"
    except Exception as e:
        return f"<h2>Server Error</h2><p>{str(e)}</p>"
    
    finally:
        # 10. CLEANUP
        # Delete the temp files to keep the server clean
        try:
            if os.path.exists(output_mp3): os.remove(output_mp3)
            if os.path.exists(output_zip): os.remove(output_zip)
            logging.info(f"[{request_id}] Cleaned up temp files.")
        except Exception as e:
            logging.warning(f"Cleanup failed: {e}")

if __name__ == '__main__':
    # Pre-flight check
    if not os.path.exists(ROLL_NUMBER_SCRIPT):
        print(f"⚠️  WARNING: Could not find script '{ROLL_NUMBER_SCRIPT}'. Make sure it's in the same folder!")
    
    app.run(debug=True, port=5000)