from flask import Flask, render_template, request, jsonify
import os

# --- Application Setup ---
app = Flask(__name__)

# --- WQI Calculation Constants ---
PARAMETERS = {
    'ph': {'standard': 8.5, 'ideal': 7.0, 'weight': 4},
    'tds': {'standard': 500, 'ideal': 0, 'weight': 1},
    'do': {'standard': 5, 'ideal': 14.6, 'weight': 5},
    'turbidity': {'standard': 5, 'ideal': 0, 'weight': 3},
    'nitrate': {'standard': 45, 'ideal': 0, 'weight': 2}
}

# --- Core WQI Function ---
def calculate_wqi(data):
    total_w = 0
    total_qw = 0

    for param, config in PARAMETERS.items():
        if param in data and data[param] is not None:
            try:
                observed = float(data[param])
                standard = config['standard']
                ideal = config['ideal']
                weight = config['weight']

                if (standard - ideal) == 0:
                    qi = 0
                else:
                    qi = 100 * (observed - ideal) / (standard - ideal)

                if param == 'do':
                    if observed >= standard:
                        qi = 100 * (1 - observed / ideal)
                    else:
                        qi = 100 + 100 * (standard - observed) / standard

                qi = max(0, qi)

                total_qw += qi * weight
                total_w += weight
            except:
                continue

    if total_w == 0:
        return 0

    return round(total_qw / total_w, 2)

# --- Status Function ---
def get_status(wqi):
    if wqi < 25:
        return "Excellent", "success"
    elif wqi < 50:
        return "Good", "info"
    elif wqi < 75:
        return "Poor", "warning"
    elif wqi < 100:
        return "Very Poor", "orange"
    else:
        return "Unfit for Consumption", "danger"

# --- Routes ---
@app.route('/')
def home():
    google_maps_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    return render_template(
        "index.html",
        google_maps_key=google_maps_key
    )

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    score = calculate_wqi(data)
    status, color = get_status(score)
    return jsonify({
        "wqi": score,
        "status": status,
        "color": color
    })

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
