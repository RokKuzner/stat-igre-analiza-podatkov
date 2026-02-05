import pandas as pd
import sqlite3
import re
import os

# confg
INPUT_FILE = 'data/raw/9_EvropskeStatIgre_naloga2_podatki.xlsx'
DB_FILE = 'data/database/stat_igre_data.db'

def process_stacked_data(df):
    cleaned_rows = []
    columns = None
    
    section_starts = df[df[1].astype(str).str.contains("Leto", na=False)].index.tolist()
    
    for i, start_idx in enumerate(section_starts):
        # "Leto 2018" --> 2018
        leto_str = str(df.iloc[start_idx, 1])
        year_match = re.search(r'\d+', leto_str)
        year = int(year_match.group()) if year_match else None
        
        header_row_idx = start_idx + 1
        current_header = df.iloc[header_row_idx].tolist()
        
        if columns is None:
            columns = ['Leto'] + current_header
        
        # Determine the end of the section
        if i < len(section_starts) - 1:
            end_idx = section_starts[i+1]
        else:
            end_idx = len(df)
            
        # Extract data rows
        data_start_idx = header_row_idx + 1
        section_data = df.iloc[data_start_idx:end_idx].copy()
        
        # Filter valid rows
        section_data = section_data[pd.to_numeric(section_data[0], errors='coerce').notna()]
        
        section_data.insert(0, 'Leto', year)
        
        cleaned_rows.append(section_data)
        
    if cleaned_rows:
        final_df = pd.concat(cleaned_rows, ignore_index=True)
        final_df.columns = columns
        return final_df
    else:
        return pd.DataFrame()

def process_sifrant(df):
    header_rows = df[df[0].astype(str).str.contains("Šifra", na=False)].index
    
    if not header_rows.empty:
        header_idx = header_rows[0]
        final_df = df.iloc[header_idx+1:].copy()
        final_df.columns = df.iloc[header_idx]
        
        # Filter valid rows
        final_df = final_df[pd.to_numeric(final_df.iloc[:, 0], errors='coerce').notna()]
        return final_df
    else:
        return df

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: File '{INPUT_FILE}' not found.")
        return

    print("Reading Excel file...")
    
    # 1. Process stacked data sheets
    print("Procesiranje PODATKI_GOSPODINJSTVA...")
    df_gosp_raw = pd.read_excel(INPUT_FILE, sheet_name='PODATKI_GOSPODINJSTVA', header=None)
    df_gosp = process_stacked_data(df_gosp_raw)
    
    print("Procesiranje PODATKI_OSEBE...")
    df_osebe_raw = pd.read_excel(INPUT_FILE, sheet_name='PODATKI_OSEBE', header=None)
    df_osebe = process_stacked_data(df_osebe_raw)
    
    # 2. Process dictionary/code sheets
    print("Procesiranje PROSTORSKI ŠIFRANT...")
    df_sifrant_raw = pd.read_excel(INPUT_FILE, sheet_name='PROSTORSKI ŠIFRANT', header=None)
    df_sifrant = process_sifrant(df_sifrant_raw)
    
    # 3. Process metadata (read normally with header)
    print("Procesiranje Metadata...")
    df_meta_gosp = pd.read_excel(INPUT_FILE, sheet_name='METAPODATKI_GOSPODINJSTVA')
    df_meta_osebe = pd.read_excel(INPUT_FILE, sheet_name='METAPODATKI_OSEBE')

    # 4. Save to SQLite
    print(f"Shranjeno v {DB_FILE}...")
    conn = sqlite3.connect(DB_FILE)
    
    df_gosp.to_sql('PODATKI_GOSPODINJSTVA', conn, if_exists='replace', index=False)
    df_osebe.to_sql('PODATKI_OSEBE', conn, if_exists='replace', index=False)
    df_sifrant.to_sql('PROSTORSKI_SIFRANT', conn, if_exists='replace', index=False)
    df_meta_gosp.to_sql('METAPODATKI_GOSPODINJSTVA', conn, if_exists='replace', index=False)
    df_meta_osebe.to_sql('METAPODATKI_OSEBE', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Koncano! Baza podakov uspesno ustvarjena.")

if __name__ == "__main__":
    main()