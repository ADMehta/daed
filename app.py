# Import required libraries
from flask import Flask, request, jsonify, render_template
import requests
from collections import Counter
from collections import defaultdict
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# OpenFDA endpoints
OPENFDA_EVENT_URL = "https://api.fda.gov/drug/event.json"
OPENFDA_DRUGS_URL = "https://api.fda.gov/drug/drugsfda.json"

# Route to render the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to fetch adverse event data for a given drug, with optional seriousness filtering
@app.route("/events")
def get_adverse_events():
    drug = request.args.get("drug")
    serious = request.args.get("serious")

    if not drug:
        return jsonify({"error": "Drug name is required"}), 400

    query = f'search=patient.drug.medicinalproduct:"{drug}"'
    if serious:
        query += f'+AND+serious:{serious}'

    try:
        response = requests.get(f"{OPENFDA_EVENT_URL}?{query}&limit=100")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to get manufacturers associated with reports for a drug
@app.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    drug = request.args.get('drug')
    seriousness = request.args.get('seriousness', 'hospitalization')  # default to 'hospitalization'

    if not drug:
        return jsonify({'error': 'Drug name is required'}), 400


    # Use local /events endpoint with seriousness filtering
    url = f"http://127.0.0.1:5000/events?drug={drug}&seriousness={seriousness}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch data: {str(e)}'}), 500

    results = data.get("results", [])
    manufacturer_counts = {}

    # Parse manufacturer name from each matching report
    for r in results:
        matched_mfgs = set()

        # Check all drug entries in each report
        for drug_entry in r.get("patient", {}).get("drug", []):
            if drug_entry.get("medicinalproduct", "").lower() == drug.lower():
                mfgs = drug_entry.get("openfda", {}).get("manufacturer_name", [])
                for mfg in mfgs:
                    matched_mfgs.add(mfg)

        # Count each manufacturer only once per report
        for mfg in matched_mfgs:
            manufacturer_counts[mfg] = manufacturer_counts.get(mfg, 0) + 1

        if not matched_mfgs:
            manufacturer_counts["Unknown"] = manufacturer_counts.get("Unknown", 0) + 1


        else:
            manufacturer_counts["Unknown"] = manufacturer_counts.get("Unknown", 0) + 1

        # Format response as a list of [manufacturer, count]
        manufacturers_output = [[name, count] for name, count in manufacturer_counts.items()]

    return jsonify({'manufacturers': manufacturers_output})


# Route to generate time-based trend data for adverse events
@app.route("/trends")
def get_trends():
    drug = request.args.get("drug")
    if not drug:
        return jsonify({"error": "Drug name is required"}), 400

    # FDA API request to retrieve reports for selected drug
    url = f"https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:\"{drug}\"&limit=100"
    res = requests.get(url)
    data = res.json()

     # Dictionary to aggregate counts by YYYY-MM
    trend = defaultdict(int)

    for r in data.get("results", []):
        # Try multiple date fields
        date_str = r.get("receiptdate") or r.get("receivedate") or r.get("occurdate")
        if not date_str or len(date_str) != 8:
            continue

        try:
            date = datetime.strptime(date_str, "%Y%m%d")
            key = date.strftime("%Y-%m")
        except Exception:
            continue

        # Match drug name case-insensitively
        for d in r.get("patient", {}).get("drug", []):
            if d.get("medicinalproduct", "").lower() == drug.lower():
                trend[key] += 1
                break

    return jsonify({"trend": dict(trend)})

# Run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)




