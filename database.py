import sqlite3

def get_stat_info(table_type:str, year:int, region:int|str, data_point:str, db_path:str='data/database/stat_igre_data.db'):
    """
    Extracts a specific data value from the database.
    
    Args:
        table_type (str): Either 'gospodinjstva' or 'osebe'.
        year (int): The year (e.g., 2018, 2022, 2024).
        region (str/int): The statistical region name (e.g., "Gorenjska") 
                          or the region code (e.g., 9).
        data_point (str): The column name of the data point (e.g., "Neto_preb").
        db_path (str): Path to the SQLite database file.
        
    Returns:
        The requested value, or an error message if not found.
    """
    conn = sqlite3.connect(db_path)
    
    try:
        # map table_type to database table name
        table_mapping = {
            'gospodinjstva': 'PODATKI_GOSPODINJSTVA',
            'osebe': 'PODATKI_OSEBE'
        }
        db_table = table_mapping.get(table_type.lower())
        
        if not db_table:
            return "Error: table_type must be 'gospodinjstva' or 'osebe'."

        # resolve Region Code if a name was provided
        region_id = region
        if isinstance(region, str):
            query = "SELECT [Šifra statistične regije] FROM PROSTORSKI_SIFRANT WHERE [Ime statistične regije] = ?"
            res = conn.execute(query, (region,)).fetchone()
            if res:
                region_id = res[0]
            else:
                return f"Error: Region '{region}' not found in the spatial registry."
        
        # Query the specific value
        query = f"SELECT [{data_point}] FROM {db_table} WHERE Leto = ? AND SR_12 = ?"
        result = conn.execute(query, (year, str(region_id))).fetchone()
        
        if result:
            return result[0]
        else:
            return "No data found for the given criteria."
            
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()

def get_stat_average(table_type: str, years: list[int], region: int|str, data_point: str, db_path: str='data/database/stat_igre_data.db'):
    """
    Calculates the average of a data point over a list of years by reusing get_stat_info.
    
    Args:
        table_type (str): 'gospodinjstva' or 'osebe'.
        years (list[int]): List of years to include (e.g., [2018, 2022]).
        region (str/int): Region name or code.
        data_point (str): Variable name.
        db_path (str): Path to database.
        
    Returns:
        float: The average value, or a message if no data was found.
    """
    values = []
    
    for year in years:
        # Reuse the first function
        result = get_stat_info(table_type, year, region, data_point, db_path)
        
        # Only add to list if the result is a number (ignores error strings)
        if isinstance(result, (int, float)):
            values.append(result)
            
    if not values:
        return "No valid data found for the given years."
    
    # Calculate average
    return sum(values) / len(values)
