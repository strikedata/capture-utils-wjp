import os
import sys

class Config:
    """Configuration settings for the Capture One Keyword Exporter."""
    
    # Path to the Capture One catalog file
    CATALOG_PATH = os.getenv('CAPTURE_ONE_CATALOG_PATH', '/path/to/catalog.cat')
    
    # Output CSV file path
    OUTPUT_CSV_PATH = os.getenv('OUTPUT_CSV_PATH', 'keywords_export.csv')
    
    # Delimiter for the CSV file
    CSV_DELIMITER = ','
    
    # Enable or disable debug logging
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() in ('true', '1', 't')
    
    # Number of keywords to export
    try:
        MAX_KEYWORDS = int(os.getenv('MAX_KEYWORDS', '1000'))
    except ValueError:
        MAX_KEYWORDS = 1000
    
    @staticmethod
    def validate():
        """Validate configuration settings."""
        if not os.path.isfile(Config.CATALOG_PATH):
            raise ValueError(f"Catalog path '{Config.CATALOG_PATH}' is not a valid file.")
        
        if not Config.OUTPUT_CSV_PATH.endswith('.csv'):
            raise ValueError("Output path must have a .csv extension.")
        
        if Config.MAX_KEYWORDS <= 0:
            raise ValueError("MAX_KEYWORDS must be a positive integer.")

# Validation can be called explicitly when needed
# Config.validate()
