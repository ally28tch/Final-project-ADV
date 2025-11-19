# OOP and Python Concepts in SmartPark System

Here is a breakdown of the key Object-Oriented Programming (OOP) and Python concepts utilized in this project.

### Object-Oriented Programming (OOP) Concepts

| Concept | Purpose | Context in Smart Park |
| :--- | :--- | :--- |
| **Classes & Objects** | To bundle data (attributes) and functionality (methods) together, creating blueprints for objects. | `SmartParkApp` class manages the entire UI and application flow. `DatabaseManager` class handles all database interactions. Instances of these classes are the objects that run the application. |
| **Methods** | Functions defined inside a class that operate on an object's data. | `park_vehicle()` in `DatabaseManager` updates the database. `show_dashboard()` in `SmartParkApp` renders the main UI screen. `get_connection()` provides a database connection. |
| **Encapsulation** | Hiding the internal state and complexity of an object, exposing only necessary functionality through methods. | The `DatabaseManager` class encapsulates all database logic (SQL queries, connection handling). The `SmartParkApp` class doesn't know the implementation details; it just calls simple methods like `db.park_vehicle()`. |

### General Python Concepts

| Concept | Purpose | Context in Smart Park |
| :--- | :--- | :--- |
| **Modules** | To organize code into separate files, making it more manageable, reusable, and logical. | `db_connection.py` separates database logic from the UI logic in `main.py`. We also import external modules like `tkinter` for the GUI and `mysql.connector` for DB access. |
| **Data Structures (List)** | To store an ordered collection of items, which can be of mixed types. | Used to hold the list of available parking spots (`available_spots`), the full list of spots from the database (`spots`), and the parking history records (`history`). |
| **Data Structures (Dictionary)** | To store data values in `key:value` pairs, allowing for efficient lookup. | Used in `unpark_vehicle` to return a structured set of data (`driver`, `plate`, `time_in`, etc.) after a vehicle is successfully unparked. Also used for history records. |
| **Error Handling (try...except)** | To gracefully handle runtime errors and prevent the program from crashing unexpectedly. | Used extensively in `DatabaseManager` to catch `mysql.connector.Error` during database operations. This ensures the app can report DB errors to the user without stopping. |
| **Conditional Logic (if/else)** | To execute different blocks of code based on whether a certain condition is true or false. | Used to check if a parking spot is occupied, validate that form fields are not empty, and determine the color of a spot in the parking map (`if occupied`). |
| **Functions** | A reusable block of code that performs a specific task and only runs when it is called. | The `main()` function serves as the entry point to start the application. It creates the `Tkinter` root window and an instance of the `SmartParkApp`, then starts the event loop. |
| **String Formatting (f-Strings)** | To easily embed expressions inside string literals for dynamic output. | Used to create user-friendly messages in `messagebox` pop-ups, such as displaying the details of a newly parked vehicle or showing summary text. |
