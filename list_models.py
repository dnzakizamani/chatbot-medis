import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)

    # List all available models
    print("Available models:")
    for model in genai.list_models():
        print(f"Name: {model.name}")
        print(f"Description: {model.description}")
        # Check if the model supports generateContent
        if hasattr(model, 'supported_generation_methods'):
            print(f"Supported Generation Methods: {model.supported_generation_methods}")
        elif hasattr(model, 'generation_methods'):
            print(f"Generation Methods: {model.generation_methods}")
        else:
            # Print available attributes to understand the model object
            print(f"Available attributes: {[attr for attr in dir(model) if not attr.startswith('_')]}")
        print("---")
else:
    print("API key not found!")