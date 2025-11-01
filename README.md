# Food Wastage Management System

A comprehensive food wastage management platform that connects food providers with receivers to reduce food waste and help communities.

## Project Overview

This system helps manage food donations by connecting restaurants, caterers, and other food providers with NGOs, shelters, and individuals who can use the surplus food. The platform tracks food listings, claims, and facilitates the distribution process.

## Features

- **Food Provider Management**: Register and manage food providers
- **Receiver Management**: Track organizations and individuals receiving food
- **Food Listings**: Post and browse available food items
- **Claims System**: Handle food donation claims and tracking
- **Database Management**: SQLite database for efficient data storage
- **Data Export**: CSV files for data portability and analysis

## Technology Stack

- **Backend**: Python with Flask
- **Database**: SQLite
- **Data Processing**: CSV file handling

## Project Structure

```
Food_wastage_management/
├── app.py                      # Main Flask application
├── database_setup.py           # Database initialization and schema
├── food_wastage.db            # SQLite database file
├── queries.sql                # SQL queries for database operations
├── requirements.txt           # Python dependencies
├── claims_data.csv            # Claims data export
├── food_listings_data.csv     # Food listings data export
├── providers_data.csv         # Providers data export
└── receivers_data.csv         # Receivers data export
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vallabh409/Food_wastage_management.git
   cd Food_wastage_management
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python database_setup.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your web browser and navigate to `http://localhost:5000`

## Database Setup

The database is automatically created when you run `database_setup.py`. The system uses SQLite with the following main tables:

- Providers
- Receivers
- Food Listings
- Claims

## Usage

1. **Register as a Provider**: Food providers can register and post available food items
2. **Register as a Receiver**: Organizations can register to receive food donations
3. **Browse Listings**: View available food items
4. **Make Claims**: Receivers can claim food items they need
5. **Track Donations**: Monitor the status of food donations

## Data Files

The CSV files contain exported data and can be used for:
- Data backup
- Analytics and reporting
- Integration with other systems

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

## Acknowledgments

This project aims to reduce food wastage and help communities by connecting food providers with those in need.
