import PyPDF2
import re
import pandas as pd

def extract_data(file_name, trip_pattern, details_pattern):
    with open(file_name, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        number_of_pages = len(reader.pages)
        print(f'The PDF "{file_name}" has {number_of_pages} pages.')

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
        date, tag, vehicle_class, time, finish_time, details, amount = match
        print(f"Trip - Tag: {tag}, Date: {date}, Vehicle Class: {vehicle_class}, Start Time: {time}, Finish Time: {finish_time}, Details: {details}, Amount: {amount}")
        data.append({
            'PDF Name': file_name,
            'Date': date,
            'Tag': tag,
            'Time': time,
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
            'PDF Name': file_name,
            'Date': date,
            'Tag': tag_no,
            'Time': time,
            'Amount': amount
        })

    return data

# Define regex patterns
trip_pattern = r'(\d{2}[A-Za-z]{3}\d{4})\s+(\d{12})\s+(\w+)\s+(\d{2}:\d{2}:\d{2})(\d{2}:\d{2}:\d{2})\s+([\w/\s]+)\s+\$(\d+\.\d{2})'
details_pattern = r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})\s+([\w-]+)\s+(\d{2})\s+(\d+\.\d{2})'

# Process both PDF files
data_combined = []
data_combined.extend(extract_data('test.pdf', trip_pattern, details_pattern))
data_combined.extend(extract_data('Feb 2022ST.pdf', trip_pattern, details_pattern))

# Create DataFrame and save to CSV
df = pd.DataFrame(data_combined)
print(df)
df.to_excel('output.xlsx', index=False)
