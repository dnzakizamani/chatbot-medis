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
    
    for term, definition in medical_terms.items():
        if term in user_message_lower:
            matched_terms.append((term, definition))

    if not model:
        print("Model not available - API key issue")  # Debug info
        return jsonify({'response': 'Kunci API tidak dikonfigurasi. Harap atur GEMINI_API_KEY di variabel lingkungan.'}), 500

    try:
        if matched_terms:
            # If we found matching terms, create a response using the CSV definitions
            csv_response = "Berdasarkan informasi dari Prudential, berikut penjelasan tentang istilah yang Anda sebutkan:\n\n"
            for term, definition in matched_terms:
                csv_response += f"{term.title()}: {definition}\n\n"
            
            csv_response += f"Namun, untuk gejala yang Anda alami ('{sanitized_message}'), berikut adalah penjelasan tambahan:\n\n"
            
            # Generate response using Gemini with specialized medical prompting in Indonesian
            prompt = f"""
            {csv_response}
            
            Anda adalah asisten AI medis yang ramah dan empatik. Gunakan nada yang hangat, empatik, dan seolah-olah Anda adalah teman yang peduli. Mulailah dengan menyambut pengguna dan menunjukkan bahwa Anda mengerti kondisi mereka. Gunakan pendekatan yang manusiawi dan penuh perhatian.
            
            Pengguna telah menjelaskan gejala atau keluhan kesehatan berikut: '{sanitized_message}'
            
            Harap berikan:
            1. Kemungkinan kondisi medis yang bisa menjelaskan gejala ini (sebutkan 2-4 kemungkinan dengan penjelasan yang mudah dipahami dan empatik)
            2. Pendekatan pengobatan umum untuk kondisi-kondisi tersebut (intervensi non-medis seperti istirahat, hidrasi, dll.)
            3. Rekomendasi kapan harus mencari pertolongan medis profesional
            4. Peringatan penting tentang diagnosis mandiri
            
            Format respons Anda dalam paragraf-paragraf yang mudah dibaca, bukan dalam format Markdown (tanpa tanda ** atau ##). Gunakan bahasa sederhana, hangat, dan non-teknis yang bisa dipahami oleh seseorang tanpa latar belakang medis. Gunakan pendekatan yang empatik dan menenangkan.
            
            PENTING: Tekankan bahwa ini hanya untuk tujuan pendidikan dan bukan pengganti nasihat medis profesional, diagnosis, atau pengobatan. Selalu sarankan untuk berkonsultasi dengan penyedia layanan kesehatan yang berkualifikasi.
            
            Mohon berikan respons dalam bahasa Indonesia dengan nada yang hangat, empatik, dan manusiawi, dalam bentuk paragraf-paragraf yang rapi dan mudah dibaca.
            """
        else:
            # If no matching terms, use the standard prompt
            prompt = f"""
            Anda adalah asisten AI medis yang ramah dan empatik. Gunakan nada yang hangat, empatik, dan seolah-olah Anda adalah teman yang peduli. Mulailah dengan menyambut pengguna dan menunjukkan bahwa Anda mengerti kondisi mereka. Gunakan pendekatan yang manusiawi dan penuh perhatian.
            
            Pengguna telah menjelaskan gejala atau keluhan kesehatan berikut: '{sanitized_message}'
            
            Harap berikan:
            1. Kemungkinan kondisi medis yang bisa menjelaskan gejala ini (sebutkan 2-4 kemungkinan dengan penjelasan yang mudah dipahami dan empatik)
            2. Pendekatan pengobatan umum untuk kondisi-kondisi tersebut (intervensi non-medis seperti istirahat, hidrasi, dll.)
            3. Rekomendasi kapan harus mencari pertolongan medis profesional
            4. Peringatan penting tentang diagnosis mandiri
            
            Format respons Anda dalam paragraf-paragraf yang mudah dibaca, bukan dalam format Markdown (tanpa tanda ** atau ##). Gunakan bahasa sederhana, hangat, dan non-teknis yang bisa dipahami oleh seseorang tanpa latar belakang medis. Gunakan pendekatan yang empatik dan menenangkan.
            
            PENTING: Tekankan bahwa ini hanya untuk tujuan pendidikan dan bukan pengganti nasihat medis profesional, diagnosis, atau pengobatan. Selalu sarankan untuk berkonsultasi dengan penyedia layanan kesehatan yang berkualifikasi.
            
            Mohon berikan respons dalam bahasa Indonesia dengan nada yang hangat, empatik, dan manusiawi, dalam bentuk paragraf-paragraf yang rapi dan mudah dibaca.
            """
        
        print(f"Sending prompt to Gemini: {prompt[:100]}...")  # Debug info (first 100 chars)
        response = model.generate_content(prompt)
        
        print(f"Response received from Gemini: {response.text[:100] if response.text else 'None'}...")  # Debug info
        
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug info
        return jsonify({'error': str(e)}), 500