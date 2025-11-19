import mysql.connector
from datetime import datetime
from typing import Tuple, List, Optional, Dict


class DatabaseManager:
    
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "smartpark"
    
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            return None
    
    def park_vehicle(self, spot_id: int, driver_name: str, plate_number: str) -> Tuple[bool, str]:
        conn = None
        cursor = None
        
        try:
            conn = self.get_connection()
            if not conn:
                return False, "Database connection failed"
            
            cursor = conn.cursor()
            time_in = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute(
                "SELECT is_occupied FROM parking_spots WHERE id = %s",
                (spot_id,)
            )
            result = cursor.fetchone()
            
            if result and result[0]:
                return False, f"Spot {spot_id} is already occupied!"
            
            if result:
                cursor.execute(
                    """UPDATE parking_spots 
                       SET driver_name = %s, plate_number = %s, 
                           time_in = %s, is_occupied = 1, time_out = NULL
                       WHERE id = %s""",
                    (driver_name, plate_number, time_in, spot_id)
                )
            else:
                cursor.execute(
                    """INSERT INTO parking_spots 
                       (id, driver_name, plate_number, time_in, is_occupied) 
                       VALUES (%s, %s, %s, %s, 1)""",
                    (spot_id, driver_name, plate_number, time_in)
                )
            
            conn.commit()
            return True, "Vehicle parked successfully"
            
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            return False, f"Database error: {err}"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error: {e}"
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def unpark_vehicle(self, plate_number: str) -> Tuple[bool, str, Optional[Dict]]:
        conn = None
        cursor = None
        
        try:
            conn = self.get_connection()
            if not conn:
                return False, "Database connection failed", None
            
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT id, driver_name, time_in 
                   FROM parking_spots 
                   WHERE plate_number = %s AND is_occupied = 1""",
                (plate_number,)
            )
            
            result = cursor.fetchone()
            
            if not result:
                return False, "Vehicle not found or already unparked", None
            
            spot_id, driver_name, time_in = result
            time_out = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute(
                """UPDATE parking_spots 
                   SET time_out = %s, is_occupied = 0 
                   WHERE id = %s""",
                (time_out, spot_id)
            )
            
            cursor.execute(
                """INSERT INTO parking_history 
                   (spot_id, driver_name, plate_number, time_in, time_out) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (spot_id, driver_name, plate_number, time_in, time_out)
            )
            
            conn.commit()
            
            data = {
                "spot": spot_id,
                "driver": driver_name,
                "plate": plate_number,
                "time_in": time_in,
                "time_out": time_out
            }
            
            return True, "Vehicle unparked successfully", data
            
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            return False, f"Database error: {err}", None
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error: {e}", None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_parking_spots(self) -> List[Tuple[int, bool]]:
        conn = None
        cursor = None
        spots = []
        
        try:
            conn = self.get_connection()
            if not conn:
                return spots
            
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, is_occupied FROM parking_spots ORDER BY id ASC"
            )
            
            rows = cursor.fetchall()
            
            for row in rows:
                spot_id = int(row[0])
                is_occupied = bool(row[1]) if row[1] is not None else False
                spots.append((spot_id, is_occupied))
            
            return spots
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return spots
            
        except Exception as e:
            print(f"Error: {e}")
            return spots
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_parking_history(self, limit: int = 50) -> List[Dict]:
        """Fetch parking history records"""
        conn = None
        cursor = None
        history = []
        
        try:
            conn = self.get_connection()
            if not conn:
                return history
            
            cursor = conn.cursor()
            cursor.execute(
                """SELECT history_id, spot_id, driver_name, plate_number, 
                          time_in, time_out 
                   FROM parking_history 
                   ORDER BY time_out DESC 
                   LIMIT %s""",
                (limit,)
            )
            
            rows = cursor.fetchall()
            
            for row in rows:
                history.append({
                    'id': row[0],
                    'spot_id': row[1],
                    'driver_name': row[2],
                    'plate_number': row[3],
                    'time_in': row[4],
                    'time_out': row[5]
                })
            
            return history
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return history
            
        except Exception as e:
            print(f"Error: {e}")
            return history
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
