# SmartPark - Parking Management System

A simple desktop application for managing parking spots, built with Python and Tkinter.

## Features

- 🚗 **Park Vehicle** - Register a vehicle in a parking spot
- 🚪 **Unpark Vehicle** - Remove a vehicle from a parking spot  
- 🗺️ **Parking Map** - Visual grid showing all parking spots and their status
- 📊 **Check Availability** - List view of all parking spots with availability status

## Requirements

- Python 3.7 or higher
- MySQL Server
- mysql-connector-python

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup MySQL Database:**
   - Make sure MySQL server is running
   - Import the database schema:
   ```bash
   mysql -u root -p < smartpark.sql
   ```
   
3. **Configure Database Connection:**
   - Edit `db_connection.py` if your MySQL credentials differ from defaults:
     - Host: `localhost`
     - User: `root`
     - Password: (empty)
     - Database: `smartpark`

## Running the Application

Simply run the main Python file:

```bash
python main.py
```

## Usage

1. **Park a Vehicle:**
   - Click "Park Vehicle" button
   - Enter Spot ID (number), Driver Name, and Plate Number
   - Click "Park Vehicle" to confirm

2. **Unpark a Vehicle:**
   - Click "Unpark Vehicle" button
   - Enter the Plate Number
   - Click "Unpark Vehicle" to confirm

3. **View Parking Map:**
   - Click "View Parking Map" to see a visual grid of all parking spots
   - Green = Available, Red = Occupied

4. **Check Availability:**
   - Click "Check Availability" for a detailed list view
   - Shows total spots, available count, and occupied count

## Project Structure

```
Final-project-ADV/
├── main.py              # Main Tkinter application
├── db_connection.py     # Database operations
├── smartpark.sql        # Database schema
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Database Schema

### parking_spots
- `id` - Parking spot ID (Primary Key)
- `driver_name` - Name of the driver
- `plate_number` - Vehicle plate number
- `time_in` - Entry timestamp
- `time_out` - Exit timestamp
- `is_occupied` - Occupancy status (0 or 1)

### parking_history
- `history_id` - Auto-increment ID (Primary Key)
- `spot_id` - Reference to parking spot
- `driver_name` - Name of the driver
- `plate_number` - Vehicle plate number
- `time_in` - Entry timestamp
- `time_out` - Exit timestamp

## Notes

- Make sure MySQL server is running before starting the application
- The application uses port 3306 (MySQL default)
- All timestamps are automatically recorded
- Parking history is maintained for record keeping

## License

This project is for educational purposes.
