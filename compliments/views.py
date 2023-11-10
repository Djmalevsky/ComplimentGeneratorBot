from django.http import HttpResponse
from .forms import UploadFileForm  # Ensure this form only has the 'file' field
from .Compliment import generate_compliment, generate_generic_compliment, scrape_website
from io import StringIO
import csv
from django.shortcuts import render

def upload_and_process_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            output_file_name = form.cleaned_data['output_file_name']
            csv_file = request.FILES['csv_file']
            custom_prompt = form.cleaned_data.get('compliment_prompt', '')  # Get the custom prompt
            temperature = form.cleaned_data.get('temperature', 0.7)  # Default to 0.7 if not provided
            GPT_Version = form.cleaned_data.get('GPT_Version', 'text-davinci-003')
            csv_file.seek(0)
            reader = csv.DictReader(csv_file.read().decode('utf-8-sig').splitlines())
            output = StringIO()
            fieldnames = reader.fieldnames + ['Compliment', 'Scrape Status']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                company_name = row['Company']
                city = row.get('City', '')  # Use .get() to avoid KeyError if the column is missing
                state = row.get('State', '')
                url = row['Website']
                content = scrape_website(url)
                if content:
                    compliment = generate_compliment(content, company_name, custom_prompt, temperature, GPT_Version)
                    scrape_status = 'Success'
                else:
                    compliment = generate_generic_compliment(company_name, city, state)
                    scrape_status = 'Failed'
                row['Compliment'] = compliment
                row['Scrape Status'] = scrape_status
                writer.writerow(row)

            output.seek(0)
            response = HttpResponse(output.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{output_file_name}.csv"'
            return response
    else:
        form = UploadFileForm()

    return render(request, 'compliments/upload.html', {'form': form})
