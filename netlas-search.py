import netlas
import time
import argparse
from dotenv import load_dotenv
import os

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
parser = argparse.ArgumentParser(description='Search for responses from a specified host.')
parser.add_argument('-d', '--host', required=True, help='Host to search for either IP address or domain name.')
parser.add_argument('-o', '--output', required=True, help='Output file to save results')
args = parser.parse_args()

# Define the query
query = f"host:{args.host}"

# Get the count of responses for the given query
cnt_of_res = netlas_connection.count(query=query, datatype='response')

# Check if there are any responses and search for them if there are
if cnt_of_res['count'] > 0:
    print("Responses for " + query)

    # Calculate the number of pages needed based on 20 results per page
    num_pages = (cnt_of_res['count'] + 19) // 20  # rounding up

    with open(args.output, 'w') as file:
        # Loop through each page and fetch the results
        for page in range(num_pages):
            search_results = netlas_connection.search(
                query=query, datatype='response', page=page, fields='uri'
            )

            if 'items' in search_results:
                # iterate over data and print: IP address, port, path and protocol
                for response in search_results['items']:
                    uri = response['data']['uri']
                    print(uri)
                    file.write(uri + '\n')

            # wait for a second to avoid throttling
            time.sleep(1)
else:
    print("No responses found.")
