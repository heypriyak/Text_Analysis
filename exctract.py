import pandas as pd
import PyPDF2
import re

file_name = 'Feb 2022ST.pdf'

# Open the PDF file and extract text
with open(file_name, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    number_of_pages = len(reader.pages)
    print(f'The PDF has {number_of_pages} pages.')

    text = ''
    for page in range(number_of_pages):
        page_text = reader.pages[page].extract_text()
        if page_text:
            text += page_text + '\n'  # Add a newline for clarity
    print(text)

# Regex patterns
tag_pattern = r'Tag No:\s*(\d+)'  # For extracting the Tag No
details_pattern = r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})\s+([\w-]+)\s+(\d{2})\s+(\d+\.\d{2})'  # For extracting the date, time, etc.

# Extracting the Tag No
tag_match = re.search(tag_pattern, text)
if tag_match:
    tag_no = tag_match.group(1)
    print(f"Tag No: {tag_no}")
else:
    tag_no = 'Unknown'  # Handle the case where tag number is missing

# Extracting the details
details_matches = re.findall(details_pattern, text)

# Function to create DataFrame
def create_df(details_matches):
    data = []
    for match in details_matches:
        date, time, code, number, amount = match
        print(f"Date: {date}, Time: {time}, Code: {code}, Number: {number}, Value: {amount}")
        data.append({
            'PDF Name': file_name,
            'Date': date,
            'Tag': tag_no,
            'Time': time,
            
            
            'Amount': amount
        })
    df = pd.DataFrame(data)
    return df

# Create the DataFrame and print it
df = create_df(details_matches)
print(df)

# Save the DataFrame to a CSV file
df.to_csv('extracted_data.csv', index=False)
