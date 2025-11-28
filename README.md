# Food Wastage Management System

A comprehensive food wastage management platform that connects food providers with receivers to reduce food waste and help communities.

## 🚀 Live Demo

**[View Live Application](https://foodwastagemanagement-dknc3rr9tguqjwzdj34pdp.streamlit.app/)**

Experience the Food Wastage Management System deployed on Streamlit Cloud.

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

- **Backend**: Python with Streamlit
- **Database**: SQLite
- **Data Processing**: CSV file handling, pandas, matplotlib, seaborn

## Project Structure

```
Food_wastage_management/
├── app.py                      # Main Streamlit application
├── database_setup.py           # Database initialization and schema
├── food_wastage.db             # SQLite database file
├── queries.sql                 # SQL queries for database operations
├── requirements.txt            # Python dependencies
├── claims_data.csv             # Claims data export
├── food_listings_data.csv      # Food listings data export
├── providers_data.csv          # Providers data export
└── receivers_data.csv          # Receivers data export
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/vallabh409/Food_wastage_management.git
cd Food_wastage_management
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python database_setup.py
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and navigate to:
```
http://localhost:8501
```

### Database Setup

The database will be automatically created when you run `database_setup.py`. It includes tables for:
- Food Providers
- Food Receivers
- Food Listings
- Claims

## Usage

1. Launch the application using Streamlit
2. Use the sidebar to navigate between different sections
3. Manage providers, receivers, and food listings
4. Track donations and claims through the system
5. Export data to CSV files for analysis

## Data Files

The project includes CSV files for data import/export:
- `providers_data.csv` - Food provider information
- `receivers_data.csv` - Food receiver information
- `food_listings_data.csv` - Available food listings
- `claims_data.csv` - Food donation claims

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Contact

For questions or suggestions, please open an issue on GitHub.

## Acknowledgments

- Thanks to all contributors who have helped with this project
- Built with Streamlit for easy deployment and user interaction
