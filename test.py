import google.generativeai as genai
from core.config import API_KEY
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')
response = model.generate_content("Dis 'OK'")
print(response.text)