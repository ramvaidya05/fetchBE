from flask import Flask, request, jsonify
app = Flask(__name__)
transactions=[] 


@app.route("/add", methods = ["POST"])
def add_points():
    try:
        data = request.json
        # Check if all required fields are present in the request
        if 'payer' not in data or 'points' not in data or 'timestamp' not in data:
            return jsonify({'error': 'Missing fields in request'}), 400

        # Extract data from the request
        payer = data['payer']
        points = data['points']
        timestamp = data['timestamp']

        # Add the transaction to the list
        transactions.append({
            'payer': payer,
            'points': points,
            'timestamp': timestamp
        })

        # Respond with a 200 status code
        return '', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/spend', methods=['POST'])
def spend_points():
    try:
        data = request.json
        points_left = data['points']
        global result
        result = []

        # Create a dictionary to keep track of points for each payer
        payer_points = {}

        # Sort transactions by timestamp (oldest first)
        transactions.sort(key=lambda x: x['timestamp'])

        #Iterate through the transactions and make result list
        for transaction in transactions:
            if transaction["points"] > points_left:
                payer_points[transaction["payer"]] = -1 * points_left
                points_left = 0
                break
            
            points_left = points_left - transaction["points"]
            if transaction["payer"] in payer_points:
                payer_points[transaction["payer"]] = payer_points[transaction["payer"]] - transaction["points"]
            else:
                payer_points[transaction["payer"]] = 0 -  transaction["points"]

            if points_left == 0:
                break

        result.append(payer_points)

        if points_left > 0:
            return 'User does not have enough points', 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/balance', methods=['GET'])
def get_points_balance():
    try:
        balance = {}
        for transaction in transactions:
            payer = transaction['payer']
            points = transaction['points']

            # Calculate balance based on transactions
            if payer in balance:
                balance[payer] += points
            else:
                balance[payer] = points

        keysList = list(balance.keys())
        for key in keysList:
            balance[key] = balance[key] + result[0][key]

        return jsonify(balance), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000)