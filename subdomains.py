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

# List to store domains that encountered errors
error_domains = []

def search_domain(domain, output_file):
    query = f"domain:{domain}"

    try:
        with open(output_file, 'a') as file:
            # Download all available results
            for resp in netlas_connection.download_all(
                query=query, 
                datatype='domain',
                fields='domain'
            ):
                # decode from binary stream
                response = json.loads(resp.decode('utf-8'))
                domain_name = response['data']['domain']
                print(domain_name)
                file.write(domain_name + '\n')
                
            # Add a delay of 1 second between domain queries
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred while processing {domain}: {str(e)}")
        error_domains.append(domain)  # Add domain to error list

# Read domains from input file or single domain
domains = []
if args.inputfile:
    with open(args.inputfile, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
else:
    domains = [args.domain]

# Process each domain sequentially with a delay
for domain in domains:
    search_domain(domain, args.output)

# Print domains that encountered errors
if error_domains:
    print("\nDomains that encountered errors:")
    for domain in error_domains:
        print(domain)
