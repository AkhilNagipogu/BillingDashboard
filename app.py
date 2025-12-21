from flask import Flask, render_template, request
import json
import qrcode
from PIL import Image, ImageDraw
import os
from datetime import datetime

# --------------------
# App setup
# --------------------
app = Flask(__name__)

DATA_FILE = 'data.json'
BILL_FOLDER = 'static/bills'
QR_FOLDER = 'static/qr'

# Checks for the existence of these fricking folders!!!!
os.makedirs(BILL_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# --------------------
# Helper functions (What is that you ask, Even i dont know, it is what it is)
# --------------------

def load_data():
    """Read data.json and return it as Python dict"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    """Save given data into data.json"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --------------------
# Routes
# --------------------

# Billing page 
@app.route('/')
def billing_page():
    return render_template('billing.html', data=load_data())

# Admin page, well more or less like a coustomization page
@app.route('/admin')
def admin_page():
    return render_template('admin.html', data=load_data())


@app.route('/save-admin', methods=['POST'])
def save_admin():
    data = request.json
    save_data(data)
    return {"status": "saved"}


@app.route('/generate-bill', methods=['POST'])
def generate_bill():
    bill = request.json
    data = load_data()

    total = bill['total']
    upi_id = data['upi_id']
    store = data['store_name']

    # --------------------
    # Generate UPI QR
    # --------------------
    # Generate UPI QR (SEPARATE IMAGE)

    upi_link = f"upi://pay?pa={upi_id}&pn={store}&am={total}&cu=INR"
    qr = qrcode.make(upi_link)

    qr_filename = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    qr.save(qr_path)


    # --------------------
    # Create bill image
    # --------------------
    img = Image.new('RGB', (600, 700), 'white')
    draw = ImageDraw.Draw(img)

    y = 20
    draw.text((20, y), store, fill='black')
    y += 40

    for item in bill['items']:
        line = f"{item['name']} x {item['qty']} = {item['price'] * item['qty']}"
        draw.text((20, y), line, fill='black')
        y += 30

    y += 20
    draw.text((20, y), f"Total: {total}", fill='black')

    # Paste QR
    qr = qr.resize((200, 200))
    img.paste(qr, (350, 450))

    # Save image
    filename = f"bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(BILL_FOLDER, filename)
    img.save(path)

    return {
    "qr": qr_path
}


# --------------------
# Run app
# --------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)