# FDA Drug Adverse Event Dashboard

A web application that visualizes adverse event data reported to the U.S. FDA for selected drugs. Users can analyze manufacturers, time trends, and seriousness categories using real-world FDA API data.

---

## 🚀 Features

- **Drug Selection**: Choose from commonly reported drugs using a dropdown
- **Seriousness Filtering**: Filter events by categories like Death, Hospitalization, Disability, etc.
- **Manufacturer Breakdown**: View the distribution of manufacturers responsible for reported cases
- **Trend Visualization**: Plot time-series data to detect spikes or patterns in adverse events
- **Dynamic API Integration**: Live data fetched from [OpenFDA](https://open.fda.gov/apis/) using RESTful endpoints

---

## 🛠️ Tech Stack

- **Frontend**: HTML, JavaScript, Plotly.js
- **Backend**: Python, Flask, Requests
- **APIs Used**:
  - `/drug/event.json` for adverse event data
  - `/drug/drugsfda.json` for supplemental drug metadata

---

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.x
- Flask
- Internet connection (for FDA API access)

### Steps
```bash
# Clone or download this repo
cd freed

# Install dependencies
pip install flask requests
pip install -r requirements.txt

# Run the app
python app.py

# Open browser and visit
http://127.0.0.1:5000

# Next Steps
Testing with Positive and Negative Test scenarios
Verify the count and ranking for each manufacturer
Polish UI m make it more user friendly.
