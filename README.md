This project requires a Google Maps API key to function. Follow the steps below to set it up:

### Setup Instructions

1. **Create a `.env` File**  
    In the root directory of the project, create a file named `.env`.

2. **Add Your API Key**  
    Add your Google Maps API key to the `.env` file in the following format:
    ```env
    GMAPS_TOKEN=your_google_maps_api_key
    ```
    Replace `your_google_maps_api_key` with your actual API key.

3. **Configure the Batch Script**  
    Before running the project, edit the `run_extraction_gmaps_place.bat` script to configure it as needed. Below are the key parameters you may need to adjust:

    - **`--keywords`**: Update the list of keywords to match your specific use case.
    - **`--file`**: Specify the input file containing the scan area details.
    - **`--outlet-check`**: Include this flag if you want to perform outlet checks.
    - **`--outlet-file`**: Provide the path to the outlet data file.

    #### Example Script Content:
    ```bat
    @echo off
    call .venv\Scripts\activate.bat
    python main.py ^
      --keywords "Restaurant Food and Drink" "Hotel or Guesthouse" "Massage or Spa" "Resort Private" "Sport Club or Gym" "Hospitals" "School or University" ^
      --file scan_area_HORECA-KOH_RONG_AREA ^
      --outlet-check ^
      --outlet-file data/master/all_kb_outlets.xlsx
    ```

### Notes
- Ensure the `.env` file is not shared publicly to protect your API key.
- Adjust the script parameters to suit your specific project requirements.
- For additional help, refer to the project's documentation or contact the maintainer.