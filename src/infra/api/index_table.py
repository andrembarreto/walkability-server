import os
import dotenv

dotenv.load_dotenv()

def get_source() -> str:
    """
    Returns the path to the JSON file containing the table data.
    """
    return os.getenv('TABLE_DATA_PATH', 'src/domain/index/table_data.json')