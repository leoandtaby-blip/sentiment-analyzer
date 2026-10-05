import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load the .env file
load_dotenv()

# Get the API key
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f'API Key found: {bool(api_key)}')
print(f'API Key length: {len(api_key) if api_key else 0}')
print(f'API Key starts with: {api_key[:20] if api_key else "None"}...')

# Try to create a client
try:
    client = Anthropic(api_key=api_key)
    print('Client created successfully')
    
    # Try to make a simple API call
    response = client.messages.create(
        model='claude-3-5-sonnet-20241022',
        max_tokens=100,
        messages=[
            {'role': 'user', 'content': 'Say hello'}
        ]
    )
    print('API call successful!')
    print(f'Response: {response.content[0].text}')
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
