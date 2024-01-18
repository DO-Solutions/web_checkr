#!/usr/bin/env python3

import requests 
import csv
from bs4 import BeautifulSoup

def check_website(domain):
    # Check if the domain starts with http:// or https://
    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain  # Prepend http:// by default
    try:
        response = requests.get(domain, timeout=10)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        # If the request is successful, parse the title or meta description for a basic summary
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title available'
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else 'No description available'

        return True, title, description

    except requests.RequestException as e:
        return False, str(e), None

def read_domains(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    domains_file = "domains.txt"
    output_file = "output.csv"  # Output file with .csv extension

    # Read list of domains from file
    domains = read_domains(domains_file)

    with open(output_file, 'w', newline='') as file:  # Open file for writing in CSV format
        csv_writer = csv.writer(file)

        # Write the header row
        csv_writer.writerow(["Domain", "Status", "Title", "Description"])

        # Check each domain and write the data
        for domain in domains:
            status, title, description = check_website(domain)

            # Write the domain data in a single row
            csv_writer.writerow([domain, status, title, description])
    
if __name__ == "__main__":
    main()
