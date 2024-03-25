# Audio Guide Maker

## Installation
+ Install required modules.
```bash
pip install -r requirements.txt
```
+ Get an OpenAI API key by signing up from [the official cite](https://openai.com/).
+ Create a file '.env' and add below.
```
OPENAI_API_KEY="YOUR_OPENAI_KEY"
```

## Run 
```bash
streamlit run app.py --server.enableXsrfProtection=false --server.port 8080
```