import os
from quart import render_template, redirect, url_for, request, session
import google.generativeai as genai
from flask_app import app

GENAI_API = os.environ.get('GENAI_API')

class Ai_Response:
    def __init__(self, city):
        self.city = city

    async def poi_response(self):
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"This is a information tool for a flight tracker program. The user has searched for: {self.city}. Provide a concise, engaging description of {self.city} (100-150 words)."
            f"Highlight its key features (e.g., landmarks, natural beauty, vibe), why it’s a must-visit, and what makes it unique for travelers."
            f"Include a brief mention of its historical or cultural significance. DONT use any special characters or anything just plain text."
        )
        response = model.generate_content(system_instructions)
        return response.text

    async def poi_header(self):
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"The user has searched for: {self.city}. Provide one good header that isnt too big for {self.city}."
            f"DONT use any special characters or anything just plain text."
        )
        response = model.generate_content(system_instructions)
        return response.text

    async def food_response(self):
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"This is a information tool for a flight tracker program. DONT use any special characters or anything just plain text, and DONT respond as if you are in a conversation this is ONLY for information."
            f"The user has searched for: {self.city}. Provide a concise overview (100-125 words) of {self.city}'s food and cultural history."
            f"Highlight iconic dishes, their origins, and how they reflect the region’s history or traditions."
            f"Explain the cultural relevance of these foods (e.g., festivals, daily life, or historical events)."
            f"Suggest one or two must-try dishes for visitors and where to find them (e.g., markets, restaurants)."
        )
        response = model.generate_content(system_instructions)
        return response.text

    async def food_header(self):
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"The user has searched for: {self.city}. Provide one good header that isnt too big about the food/cultural relevance of {self.city}."
            f"DONT use any special characters or titles such as City: or anything just plain text."
        )
        response = model.generate_content(system_instructions)
        return response.text

    async def architecture_response(self):
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"This is a information tool for a flight tracker program. DONT use any special characters, headers, or anything just plain text, and DONT respond as if you are in a conversation this is ONLY for information."
            f"The user has searched for: {self.city}. Provide a concise overview (100-125 words) of {self.city}'s unique architecture."
            f"Highlight iconic buildings, structures, or styles, their historical or cultural significance, and what makes them distinctive (e.g., materials, design, or era)."
            f"Mention one or two must-see architectural sites for visitors and why they’re special."
        )
        response = model.generate_content(system_instructions)
        return response.text

    async def architecture_header(self):
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"The user has searched for: {self.city}. Provide one good header about the architecture of {self.city} that isnt too big."
            f"DONT use any special characters or titles such as City: or anything just plain text."
        )
        response = model.generate_content(system_instructions)
        return response.text

    @staticmethod
    @app.route('/generate-response', methods=['POST'])
    async def response():
        if 'user_responses' not in session:
            session['user_responses'] = []
        if 'ai_responses' not in session:
            session['ai_responses'] = []

        form_data = await request.form
        user_input = form_data.get('user_input', '')
        session['user_responses'].append(user_input)
        session.modified = True
        genai.configure(api_key=GENAI_API)
        model = genai.GenerativeModel('gemini-2.0-flash')
        system_instructions = (
            f"Act as an AI assistant for a flight tracker program focused on {session['city']}. Do not start responses with 'AI:'. "
            f"Answer concisely about: "
            f"- Tourism: attractions, events, dining. "
            f"- History, culture, local transport. "
            f"- Flights: airports, schedules, airlines, travel tips, weather impacts. "
            f"Use chat log to continue conversation: User: {session['user_responses']}, AI: {session['ai_responses']}. "
            f"Stay on topic. If unclear or off-topic, ask for clarification ONLY if unresolvable. "
            f"For flight ticket requests: "
            f"1. Check chat log for provided details (month, timeframe like '7 days', departure airport, arrival airport). "
            f"2. Prompt for each missing detail in order (e.g., 'Please provide the month.', 'Please provide the amount of days. 'Please provide the departure airport. 'Please provide the arrival airport.'''). "
            f"3. Do not use random values unless user explicitly says 'no preference' or similar after prompting. "
            f"4. Once all four details are provided in chat log, respond only with 'Confirming: [month], [timeframe], [departure], [arrival]'. "
            f"Do not confirm until all details are explicitly provided."
            f"Once confirmed continue assistance as normal"
        )
        prompt = f"{system_instructions}\n\nUser question: {user_input}"
        response = model.generate_content(prompt)
        ai_response = response.text
        session['ai_responses'].append(ai_response)
        session.modified = True
        print(session['user_responses'])
        print(session['ai_responses'])
        return {'ai_response': ai_response}
