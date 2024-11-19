### Geocoding Script ###
This project is a simple geocoding tool using Python and Nominatim (OpenStreetMap). The script processes an input file with addresses and outputs files with latitude and longitude coordinates in both Excel and CSV formats.

## Project Structure

- **`data/`**: This folder holds your input file containing addresses. Place your `.xlsx` file here.
- **`output/`**: This folder will store the output files with geocoded data (latitude and longitude) in both Excel and CSV formats. It starts off empty.
- **`script.py`**: This is the main script that processes the data and retrieves geolocation coordinates using Nominatim.
- **`requirements.txt`**: This file lists the dependencies needed to run the script. Install them using `pip install -r requirements.txt`.
- **`README.md`**: The documentation for the project (you’re reading it right now!).

## Usage

Clone this repository:

    git clone https://github.com/JulienRht/geocoding-script.git
    cd geocoding-script

Install dependencies:

    pip install -r requirements.txt

Place your input file in the data/ folder. Example file: data/input_data.xlsx.

Run the script:

    python script.py
