#!/usr/bin/env python3

import requests
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm

def check_website(session, domain):
    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain
    try:
        response = session.get(domain, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title available'

        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description and 'content' in meta_description.attrs:
            description = meta_description['content']
        else:
            description = 'No description available'

        return True, title, description

    except requests.RequestException as e:
        return False, str(e), None

def read_domains(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    domains_file = "domains.txt"
    output_file = "output.csv"

    domains = read_domains(domains_file)

    with requests.Session() as session, open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Domain", "Status", "Title", "Description"])

        for domain in tqdm(domains, desc="Analyzing Domains"):
            status, title, description = check_website(session, domain)
            csv_writer.writerow([domain, status, title, description])

if __name__ == "__main__":
    main()

