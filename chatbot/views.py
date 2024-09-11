from django.shortcuts import render
from django.http import HttpResponse
from .ai_model import generate_response

def index(request):
    return render(request, 'chatbot/index.html')


def chatbot_view(request):
    response = ""
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        ai_choice = request.POST.get('ai_choice', 'openai')  # Default to OpenAI

        if not user_input:
            response = 'Please enter some text.'
        else:
            try:
                response = generate_response(user_input, model_choice=ai_choice)
            except Exception as e:
                response = f"Error generating a valid response {str(e)}"

    return render(request, 'chatbot/index.html', {'response': response})
