from bs4 import BeautifulSoup
import requests
import pandas as pd

def fetchdata_wikipedia(weblink, table_index=0):
    try:
        # Step 1: Fetch the web page
        source = requests.get(weblink)
        soup = BeautifulSoup(source.text, 'html.parser')

        # Step 2: Locate all tables with class 'wikitable'
        tables = soup.find_all('table', class_='wikitable')

        if not tables:
            return "No tables found on this page."

        # Use the specified table index
        if table_index >= len(tables):
            return f"Table index {table_index} is out of range. There are only {len(tables)} tables."

        explor = tables[table_index]

        # Step 3: Extract the table headers
        exp2 = explor.find_all('th')
        titles = [title.text.strip() for title in exp2]

        # Step 4: Initialize an empty list to store all row data
        all_rows = []

        # Step 5: Extract table rows, skipping the header row
        row_data = explor.find_all('tr')[1:]  # Skip the first row (header)

        for row in row_data:
            row_data0 = row.find_all('td')
            row_data2 = [row1.text.strip() for row1 in row_data0]

            # Check if the number of columns in the current row matches the number of headers
            if len(row_data2) == len(titles):
                all_rows.append(row_data2)
            else:
                print(f"Warning: Row skipped due to column mismatch: {row_data2}")

        # Create a DataFrame from the collected data
        df2 = pd.DataFrame(all_rows, columns=titles)

        # Check if there are at least two columns to work with
        if len(titles) >= 2:
            # Repeat the first column's values for the second column
            df_repeated = df2.loc[df2.index.repeat(df2.iloc[:, 1].astype(int))].reset_index(drop=True)

            # Rename columns if necessary (optional)
            df_repeated.columns = ['Company Name', 'Revenue']  # Change as per your data
            # Or use `titles` for dynamic naming if needed

            # Save to CSV
            valid_filename = weblink.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '')  # Customize as needed
            path_ = r'C:\Users\Ahmed Hassan\Documents\python for beginner\csv files'
            df_repeated.to_csv(f'{path_}\\{valid_filename}.csv',
                               index=False)

            return f"Data saved to {valid_filename}.csv with repeated first column."

        else:
            return "Not enough columns to repeat."

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
weblink = input("Wikipedia URL please to scrape: ")
print(fetchdata_wikipedia(weblink))
