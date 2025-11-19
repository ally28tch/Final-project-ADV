from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from config import get_db_connection
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = "smartpark_secret_key"

# HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')

# PARK VEHICLE (Combined GET and POST)
@app.route('/park', methods=['GET', 'POST'])
def park():
    if request.method == 'POST':
        conn = None
        cursor = None
        try:
            spot = request.form.get('spot_id')
            driver = request.form.get('driver_name')
            plate = request.form.get('plate_number')
            time_in = datetime.now().strftime('%Y-%m-%d %I:%M %p')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO parking_spots (id, driver_name, plate_number, time_in, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                (spot, driver, plate, time_in, True)
            )
            conn.commit()

            return render_template('park.html',
                                   success=True,
                                   driver=driver,
                                   plate=plate,
                                   spot=spot,
                                   time_in=time_in)
        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
            if conn:
                conn.rollback()
            return render_template('park.html')
        except Exception as e:
            flash(f"Unexpected error: {e}")
            if conn:
                conn.rollback()
            return render_template('park.html')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('park.html')

# UNPARK VEHICLE
@app.route('/unpark', methods=['GET', 'POST'])
def unpark():
    if request.method == 'POST':
        plate = request.form.get('platenumber', '').strip().upper()
        time_out = datetime.now().strftime('%Y-%m-%d %I:%M %p')

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, driver_name, time_in FROM parking_spots WHERE plate_number = %s AND is_occupied = TRUE",
                (plate,)
            )
            spot_data = cursor.fetchone()
            if not spot_data:
                flash("Vehicle not found or already unparked.")
                return redirect(url_for('unpark'))

            spot_id, driver, time_in = spot_data

            cursor.execute(
                "UPDATE parking_spots SET time_out = %s, is_occupied = FALSE WHERE id = %s",
                (time_out, spot_id)
            )

            cursor.execute(
                "INSERT INTO parking_history (spot_id, driver_name, plate_number, time_in, time_out) VALUES (%s, %s, %s, %s, %s)",
                (spot_id, driver, plate, time_in, time_out)
            )

            conn.commit()

            flash("Vehicle unparked successfully!")
            return jsonify({
                "success": True,
                "data": {
                    "driver_name": driver,
                    "plate_number": plate,
                    "spot": spot_id,
                    "time_in": time_in,
                    "time_out": time_out
                }
            })
        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
            if conn:
                conn.rollback()
        except Exception as e:
            flash(f"Unexpected error: {e}")
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return render_template('unpark.html')
    return render_template('unpark.html')

# MAP BUTTON
@app.route('/map')
def map_view():
    conn = None
    cursor = None
    spots = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, is_occupied FROM parking_spots ORDER BY id ASC")
        rows = cursor.fetchall()
        for r in rows:
            spot_id = int(r[0]) if isinstance(r[0], int) else r[0]
            occupied = bool(r[1]) if r[1] is not None else False
            spots.append((spot_id, occupied))
    except Exception as e:
        flash(f"Error loading map: {e}")
        spots = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('map.html', spots=spots)

# CHECK AVAILABILITY BUTTON
@app.route('/check_availability')
def check_availability():
    conn = None
    cursor = None
    spots = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, is_occupied FROM parking_spots ORDER BY id ASC")
        rows = cursor.fetchall()
        for r in rows:
            spot_id = int(r[0]) if isinstance(r[0], int) else r[0]
            occupied = bool(r[1]) if r[1] is not None else False
            spots.append((spot_id, occupied))
    except Exception as e:
        flash(f"Error checking availability: {e}")
        spots = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    spot_dicts = [{"id": spot_id, "taken": occupied} for spot_id, occupied in spots]

    return render_template('availability.html', spots=spot_dicts)

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)