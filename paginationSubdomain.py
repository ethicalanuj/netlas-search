import netlas
import json
import argparse
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the API key from environment variables
api_key = os.getenv('NETLAS_API_KEY')

if not api_key:
    print("API key not found. Please set it in the .env file.")
    exit(1)

# Initialize the Netlas client
netlas_connection = netlas.Netlas(api_key=api_key)

# Set up argument parsing
parser = argparse.ArgumentParser(description='Search for subdomains from specified hosts.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-d', '--domain', help='Domain search query in the format <*.domain.com> or <domain.*>.')
group.add_argument('-i', '--inputfile', help='Input file with a list of domain queries (one per line).')
parser.add_argument('-o', '--output', required=True, help='Output file to save results')
args = parser.parse_args()

def search_domain(domain, output_file):
    query = f"domain:{domain}"

    try:
        with open(output_file, 'a') as file:
            # Fetch the first page of results
            search_results = netlas_connection.search(
                query=query,
                datatype='domain',
                page=0,
                fields='domain'
            )

            # Process each item in the first page
            if 'items' in search_results:
                for response in search_results['items']:
                    domain_name = response['data']['domain']
                    print(domain_name)
                    file.write(domain_name + '\n')

            # Handle pagination if there are more results
            total_pages = search_results.get('total_pages', 0)
            for page in range(1, total_pages):
                search_results = netlas_connection.search(
                    query=query,
                    datatype='domain',
                    page=page,
                    fields='domain'
                )

                if 'items' in search_results:
                    for response in search_results['items']:
                        domain_name = response['data']['domain']
                        print(domain_name)
                        file.write(domain_name + '\n')

                # Add a delay between pagination requests
                time.sleep(1)

    except Exception as e:
        print(f"An error occurred while processing {domain}: {str(e)}")

# Read domains from input file or single domain
domains = []
if args.inputfile:
    with open(args.inputfile, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
else:
    domains = [args.domain]

# Process each domain sequentially with pagination and a delay
for domain in domains:
    search_domain(domain, args.output)
