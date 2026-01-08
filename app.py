from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import logging
import csv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {'Yes' if api_key else 'No'}")  # Debug info

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("Gemini model initialized successfully")  # Debug info
else:
    model = None
    print("ERROR: No API key found!")  # Debug info

def load_medical_terms():
    """Load medical terms from CSV file"""
    medical_terms = {}
    try:
        with open('medis_prudential.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                term = row['Istilah'].lower().strip()
                definition = row['Definisi']
                medical_terms[term] = definition
        print(f"Loaded {len(medical_terms)} medical terms from CSV")  # Debug info
        # Print some sample terms for debugging
        sample_terms = list(medical_terms.keys())[:10]
        print(f"Sample terms loaded: {sample_terms}")  # Debug info
    except FileNotFoundError:
        print("medis_prudential.csv file not found")  # Debug info
    except Exception as e:
        print(f"Error loading medical terms: {str(e)}")  # Debug info
    return medical_terms

medical_terms = load_medical_terms()

def sanitize_input(text):
    """Sanitize user input to prevent harmful prompts"""
    # Remove potentially harmful patterns
    sanitized = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print(f"Received message: {user_message}")  # Debug info

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Sanitize user input
    sanitized_message = sanitize_input(user_message)
    print(f"Sanitized message: {sanitized_message}")  # Debug info

    if not sanitized_message:
        return jsonify({
            'response': 'Harap berikan deskripsi yang valid tentang gejala atau keluhan kesehatan Anda.'
        })

    # Check if the user's message contains any medical terms from our CSV
    matched_terms = []
    user_message_lower = sanitized_message.lower()
    print(f"User message (lowercase): {user_message_lower}")  # Debug info
    print(f"Available medical terms: {list(medical_terms.keys())[:10]}...")  # Debug info (first 10)

    for term, definition in medical_terms.items():
        print(f"Checking if '{term}' is in user message")  # Debug info
        if term in user_message_lower:
            print(f"Match found: {term}")  # Debug info
            matched_terms.append((term, definition))

    print(f"Matched terms: {matched_terms}")  # Debug info

    if not model:
        print("Model not available - API key issue")  # Debug info
        return jsonify({'response': 'Kunci API tidak dikonfigurasi. Harap atur GEMINI_API_KEY di variabel lingkungan.'}), 500

    try:
        if matched_terms:
            # If we found matching terms, create a response using the CSV definitions
            csv_response = "**Berdasarkan informasi dari Prudential**, berikut penjelasan tentang istilah yang Anda sebutkan:\n\n"
            for term, definition in matched_terms:
                csv_response += f"**{term.title()}**: {definition}\n\n"

            csv_response += f"Namun, untuk gejala yang Anda alami ('{sanitized_message}'), berikut adalah penjelasan tambahan:\n\n"

            # Generate response using Gemini with specialized medical prompting in Indonesian
            prompt = f"""
            {csv_response}

            Anda adalah dokter yang ramah dan profesional. Gunakan nada yang hangat namun informatif, seperti seorang dokter yang menjelaskan kondisi medis kepada pasien.

            Pengguna telah menjelaskan gejala atau keluhan kesehatan berikut: '{sanitized_message}'

            Harap berikan jawaban dalam format berikut:

            1. **Penjelasan mengenai istilah medis tersebut** - berikan penjelasan yang mudah dipahami tentang kondisi medis yang relevan. Jika informasi berasal dari sumber Prudential, tulis "**Menurut Prudential:**" lalu dilanjutkan dengan penjelasan dalam paragraf. Jika informasi berasal dari AI, tulis "**Menurut Gemini:**" lalu dilanjutkan dengan penjelasan dalam paragraf.

            2. **Cara Pencegahan** - jelaskan langkah-langkah pencegahan yang bisa diambil untuk menghindari kondisi tersebut.

            3. **Cara Pengobatan** - jelaskan pendekatan pengobatan umum untuk kondisi tersebut (intervensi non-medis seperti istirahat, hidrasi, dll.).

            Format respons Anda dalam paragraf-paragraf yang mudah dibaca. Gunakan tanda ** untuk membuat teks tebal (bold) pada bagian-bagian penting. Gunakan bahasa sederhana, hangat, dan non-teknis yang bisa dipahami oleh seseorang tanpa latar belakang medis. Gunakan pendekatan yang empatik namun profesional.

            PENTING: Tekankan bahwa ini hanya untuk tujuan pendidikan dan bukan pengganti nasihat medis profesional, diagnosis, atau pengobatan. Selalu sarankan untuk berkonsultasi dengan penyedia layanan kesehatan yang berkualifikasi.

            Mohon berikan respons dalam bahasa Indonesia dengan nada yang ramah, profesional, dan to the point, dalam bentuk paragraf-paragraf yang rapi dan mudah dibaca.
            """
        else:
            # If no matching terms, use the standard prompt
            prompt = f"""
            Anda adalah dokter yang ramah dan profesional. Gunakan nada yang hangat namun informatif, seperti seorang dokter yang menjelaskan kondisi medis kepada pasien.

            Pengguna telah menjelaskan gejala atau keluhan kesehatan berikut: '{sanitized_message}'

            Harap berikan jawaban dalam format berikut:

            1. **Penjelasan mengenai istilah medis tersebut** - berikan penjelasan yang mudah dipahami tentang kondisi medis yang relevan. Karena informasi berasal dari AI, tulis "**Menurut Gemini:**" lalu dilanjutkan dengan penjelasan dalam paragraf.

            2. **Cara Pencegahan** - jelaskan langkah-langkah pencegahan yang bisa diambil untuk menghindari kondisi tersebut.

            3. **Cara Pengobatan** - jelaskan pendekatan pengobatan umum untuk kondisi tersebut (intervensi non-medis seperti istirahat, hidrasi, dll.).

            Format respons Anda dalam paragraf-paragraf yang mudah dibaca. Gunakan tanda ** untuk membuat teks tebal (bold) pada bagian-bagian penting. Gunakan bahasa sederhana, hangat, dan non-teknis yang bisa dipahami oleh seseorang tanpa latar belakang medis. Gunakan pendekatan yang empatik namun profesional.

            PENTING: Tekankan bahwa ini hanya untuk tujuan pendidikan dan bukan pengganti nasihat medis profesional, diagnosis, atau pengobatan. Selalu sarankan untuk berkonsultasi dengan penyedia layanan kesehatan yang berkualifikasi.

            Mohon berikan respons dalam bahasa Indonesia dengan nada yang ramah, profesional, dan to the point, dalam bentuk paragraf-paragraf yang rapi dan mudah dibaca.
            """
        
        print(f"Sending prompt to Gemini: {prompt[:100]}...")  # Debug info (first 100 chars)
        response = model.generate_content(prompt)
        
        print(f"Response received from Gemini: {response.text[:100] if response.text else 'None'}...")  # Debug info
        
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug info
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)