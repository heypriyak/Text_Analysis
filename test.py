import PyPDF2
import re
import pandas as pd
import os

folder_path = r'C:\Users\vinay\OneDrive\Desktop\BlackCoffer_Task\data'

# List all files in the folder
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

def extract_data(file_path, trip_pattern, details_pattern):
    print(f"Reading PDF file: {os.path.basename(file_path)}")  # Log the file being read
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        print(f'The PDF "{os.path.basename(file_path)}" has {number_of_pages} pages.')

        text = ''
        for page in range(number_of_pages):
            page_text = reader.pages[page].extract_text()
            if page_text:
                text += page_text + '\n'  # Add a newline for clarity

    # Extracting trip details
    trip_matches = re.findall(trip_pattern, text)
    data = []

    # Process trip matches
    for match in trip_matches:
        date, tag, vehicle_class, start_time, finish_time, details, amount = match
        print(f"Trip - Tag: {tag}, Date: {date}, Vehicle Class: {vehicle_class}, Start Time: {start_time}, Finish Time: {finish_time}, Details: {details}, Amount: {amount}")
        data.append({
            'PDF Name': os.path.basename(file_path),
            'Date': date,
            'Tag': tag,
            'Start Time': start_time,
            'Finish Time': finish_time,
            'Amount': amount
        })

    # Extracting additional details
    tag_pattern = r'Tag No:\s*(\d+)'  # For extracting the Tag No
    tag_match = re.search(tag_pattern, text)
    tag_no = tag_match.group(1) if tag_match else 'Unknown'

    details_matches = re.findall(details_pattern, text)
    
    # Process details matches
    for match in details_matches:
        date, time, code, number, amount = match
        print(f"Detail - Date: {date}, Time: {time}, Code: {code}, Number: {number}, Value: {amount}")
        data.append({
            'PDF Name': os.path.basename(file_path),
            'Date': date,
            'Tag': tag_no,
            'Time': time,
            'Amount': amount
        })

    return data

# Define regex patterns (correcting escape sequences and formats)
trip_pattern = r'(\d{2}[A-Za-z]{3}\d{4})\s+(\d{12})\s+(\w+)\s+(\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2})\s+([\w/\s]+)\s+\$(\d+\.\d{2})'
details_pattern = r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})\s+([\w-]+)\s+(\d{2})\s+(\d+\.\d{2})'

# Process all PDF files
data_combined = []
for pdf_file in pdf_files:
    file_path = os.path.join(folder_path, pdf_file)
    print(f"Processing file: {pdf_file}")  # Log which file is being processed
    data_combined.extend(extract_data(file_path, trip_pattern, details_pattern))
    print(f"Completed reading {pdf_file}\n")

# Create DataFrame
df = pd.DataFrame(data_combined)

# Remove duplicates based on relevant columns (you can choose the appropriate subset of columns)
df.drop_duplicates(subset=['Date', 'Tag', 'Time', 'Amount'], inplace=True)

# Save to Excel
print(df)
df.to_excel('output.xlsx', index=False)
