import html
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    """Serve the Data Validation Form page."""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    """
    Server-side validation and sanitization.
    - Sanitize all inputs using html.escape() to prevent XSS / script injection
    - Validate each field with server-side rules
    - Return validated + sanitized results as JSON
    """
    data = request.get_json()

    raw_name = data.get('name', '').strip()
    raw_email = data.get('email', '').strip()
    raw_mobile = data.get('mobile', '').strip()
    raw_age = data.get('age', '').strip()
    raw_comment = data.get('comment', '').strip()

    errors = []

    # ── Sanitize (output encoding to prevent script injection) ──
    sanitized_name = html.escape(raw_name)
    sanitized_email = html.escape(raw_email)
    sanitized_mobile = html.escape(raw_mobile)
    sanitized_comment = html.escape(raw_comment) if raw_comment else 'No client error, as the data entered is valid.'

    # ── Validate ──
    if not sanitized_name or len(sanitized_name) < 2:
        errors.append('Full Name must be at least 2 characters.')

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, raw_email):
        errors.append('Enter a valid email (e.g., user@mail.com).')

    if not re.match(r'^\d{10}$', raw_mobile):
        errors.append('Mobile must be 10 digits starting with 6-9.')

    validated_age = None
    try:
        validated_age = int(raw_age)
        if validated_age < 18 or validated_age > 60:
            errors.append('Age must be a number between 18 and 60.')
    except ValueError:
        errors.append('Age must be a valid number.')

    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400

    # ── Success response ──
    return jsonify({
        'success': True,
        'student': 'IZHAR KHAN (Roll: 231422)',
        'sanitized_name': sanitized_name,
        'sanitized_email': sanitized_email,
        'sanitized_mobile': sanitized_mobile,
        'validated_age': validated_age,
        'sanitized_comment': sanitized_comment,
        'status': 'Payload cleaned, sanitized, and ready for database insertion.'
    }), 200


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("Flask server starting at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
