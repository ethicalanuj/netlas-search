# netlas-search
### Script for getting result from netlas

#### Create a Virtual Environment (optional but recommended):
- This ensures that you have an isolated environment for your project.
```
python3 -m venv venv
source venv/bin/activate
```

#### Install the required libraries:
```
pip install netlas python-dotenv
```

#### Create a .env file in the root directory of your project:
```
NETLAS_API_KEY=YOUR_API_KEY
```

#### Run the script with the -h flag to see the help message:
```
python netlas-search.py -h
```