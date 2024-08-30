from flask import Flask, request, render_template, jsonify
import pandas as pd
import datetime

app = Flask(__name__)

# Load dataset
df = pd.read_csv('route_schedule.csv')

# Dictionaries to store shift info and allocations
shift_info = {}
route_allocation = {}
allocated_details = {}  # To store allocated details

# Predefined crew IDs and associated driver-conductor pairs
crew_pairs = {
    "C1A2B3": {"driver": "driver1", "conductor": "conductor1"},
    "C2D4E5": {"driver": "driver2", "conductor": "conductor2"},
    "C3F6G7": {"driver": "driver3", "conductor": "conductor3"},
    "C4H8I9": {"driver": "driver4", "conductor": "conductor4"},
    "C1A2B3": {"driver": "driver5", "conductor": "conductor5"}, # Example of a mixed pair
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/allocate', methods=['POST'])
def allocate():
    crew_id = request.form.get('crew_id')
    print(crew_id)

    # Validate the crew_id
    if crew_id not in crew_pairs:
        return jsonify({'status': 'error', 'message': 'Invalid Crew ID'})

    # Get the driver and conductor associated with the crew_id
    driver_name = crew_pairs[crew_id]['driver']
    conductor_name = crew_pairs[crew_id]['conductor']

    # Check if driver and conductor are available
    def check_shift(name):
        if name.lower() in shift_info:
            shift_end = shift_info[name.lower()]['end_time']
            if datetime.datetime.now() > shift_end:
                return True
            else:
                return f"{name}'s shift ends by {shift_end.strftime('%H:%M')}"
        return True

    driver_check = check_shift(driver_name)
    conductor_check = check_shift(conductor_name)

    if isinstance(driver_check, str):
        return jsonify({'status': 'error', 'message': driver_check})
    if isinstance(conductor_check, str):
        return jsonify({'status': 'error', 'message': conductor_check})

    # Allocate a shift for familiar routes only
    familiar_routes = set(df['Route Number'].unique())

    for _, row in df.iterrows():
        route_number = row['Route Number']
        if route_number in familiar_routes and route_number not in route_allocation:
            # Allocate shift for the crew
            shift_info[driver_name.lower()] = {
                'shift': row['Shift Hours'],
                'end_time': datetime.datetime.now() + datetime.timedelta(hours=12)
            }
            shift_info[conductor_name.lower()] = {
                'shift': row['Shift Hours'],
                'end_time': datetime.datetime.now() + datetime.timedelta(hours=12)
            }

            route_allocation[route_number] = {'driver': driver_name, 'conductor': conductor_name}

            # Save allocated details
            allocated_details[route_number] = {
                'crew_id': crew_id,
                'driver': driver_name,
                'conductor': conductor_name,
                'route_stops': row['Route Stops'],
                'route_timings': row['Route Timings']
            }

            return jsonify({
                'status': 'success',
                'route_number': route_number,
                'route_stops': row['Route Stops'],
                'route_timings': row['Route Timings']
            })

    return jsonify({'status': 'error', 'message': 'No available routes for this crew ID.'})

@app.route('/show_schedule', methods=['GET'])
def show_schedule():
    return jsonify(allocated_details)

if __name__ == '__main__':
    app.run(debug=True)
