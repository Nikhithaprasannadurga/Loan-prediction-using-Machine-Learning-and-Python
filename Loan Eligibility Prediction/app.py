from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Example loan eligibility criteria function
def check_loan_eligibility(data):
    """
    Check loan eligibility based on simple criteria.
    """
    if data['creditScore'] < 600:
        return "Not Eligible"
    if data['income'] < 2000:
        return "Not Eligible"
    if data['loanAmount'] > data['income'] * 10:
        return "Not Eligible"
    return "Eligible"

@app.route('/')
def index():
    """
    Serve the main HTML page.
    """
    return render_template('index.html')

@app.route('/check_eligibility', methods=['POST'])
def check_eligibility():
    """
    API endpoint to check loan eligibility.
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate required fields
        required_fields = [
            'gender', 'married', 'dependents', 'education',
            'income', 'loanAmount', 'creditScore', 'employment'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Convert fields to appropriate types
        data['dependents'] = int(data['dependents'])
        data['income'] = float(data['income'])
        data['loanAmount'] = float(data['loanAmount'])
        data['creditScore'] = int(data['creditScore'])

        # Call eligibility function
        result = check_loan_eligibility(data)

        # Return result
        return jsonify({'result': result})
    except ValueError as ve:
        return jsonify({'error': f'Invalid input type: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

