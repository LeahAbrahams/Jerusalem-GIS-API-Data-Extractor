# Jerusalem Municipal GIS Data Extractor

A robust Python command-line utility designed to interface with the Jerusalem Municipality's official GIS API. This tool allows users to dynamically search for specific spatial data layers, bypass server-side request blocks, and perform automated data cleaning and processing on the retrieved datasets.

## Key Features

* Dynamic Layer Search: Allows users to query the GIS server interactively using layer IDs or partial keyword searches (e.g., "parking", "education").
* Request Block Prevention: Simulates browser headers (Chrome User-Agent) to bypass restrictive access blocks and ensure a reliable API connection.
* Automated Data Processing: Utilizes the `pandas` library to clean, filter, and structure the retrieved geospatial data instantly.
* Robust Error Handling: Features customized exception handling to manage connection timeouts and server-side response issues gracefully without crashing.

## Tech Stack

* Language: Python 3.x
* Core Libraries: requests (for API querying), pandas (for data manipulation and processing)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/jerusalem-gis-extractor.git](https://github.com/your-username/jerusalem-gis-extractor.git)
   cd jerusalem-gis-extractor
   ```
   
2. Install required dependencies:
   ```bash
   pip install pandas requests
   ```
   
3. Run the script:
   ```bash
   python gis_project.py
   ```
   
## Future Roadmap

* Implement a graphical user interface (GUI) or an interactive web dashboard.
* Add advanced spatial data manipulation options based on specific business needs.
