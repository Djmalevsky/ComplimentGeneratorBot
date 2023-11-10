import csv
from .Compliment import generate_compliment, generate_generic_compliment, scrape_website

def handle_uploaded_file(file, output_file_name, company_name, city, state):
    # Assuming 'file' is the uploaded file object
    # Read the CSV
    with open(file.name, 'r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    # Process the CSV
    with open(output_file_name, 'w', newline='') as outfile:
        fieldnames = reader.fieldnames + ['Compliment']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            content = scrape_website(row['Website'])
            if content:
                compliment = generate_compliment(content, company_name)
            else:
                compliment = generate_generic_compliment(company_name, city, state)
            row['Compliment'] = compliment
            writer.writerow(row)
    
    # Return the path to the new CSV so it can be used in the HttpResponse
    return output_file_name
