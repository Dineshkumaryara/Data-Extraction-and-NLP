
## Instructions

### Setup
1. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Data Extraction
1. Ensure `Input.xlsx` is in the `data/` directory.
2. Run the extraction script:
    ```bash
    python scripts/extract_articles.py
    ```
   Extracted articles will be saved in the `data/extracted_articles/` directory.

### Text Analysis
1. Run the text analysis script:
    ```bash
    python scripts/text_analysis.py
    ```
   The results will be saved in the `output/Output Data Structure.xlsx` file.
