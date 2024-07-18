# netlas-search
### Script for getting result from netlas

#### Create a Virtual Environment (optional but recommended):
```
python3 -m venv venv
source venv/bin/activate
```

#### Install the required libraries:
```
pip install netlas python-dotenv chardet
```

#### Create a .env file in the root directory of your project:
```
NETLAS_API_KEY=YOUR_API_KEY
```

#### Run the script with the -h flag to see the help message:
```
python netlas-search.py -h
```

#### Ex. Output
```
python netlas-search.py -d 135.125.237.168 -o netlas-result.txt
```
```
smtpstarttls://135.125.237.168:25
smtps://135.125.237.168:465
https://135.125.237.168:443/
imap://135.125.237.168:143
imaps://135.125.237.168:993
smtp://135.125.237.168:25
http://135.125.237.168:80/
imapstarttls://135.125.237.168:143
```

----------
## subdomains.py

```
python subdomains.py -h
```

```
python subdomains.py -i inputfile -o outputfile
```
#### For better result use URL with *

```
*.example.com
example.*
*.example.net
```

#### Ex. Output
```
python subdomains.py -d "*.netlas.io"
```
```
app.netlas.io
pay.netlas.io
www.netlas.io
mail.netlas.io
```