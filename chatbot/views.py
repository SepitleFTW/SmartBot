from django.shortcuts import render
from django.http import HttpResponse
from .ai_model import generate_huggingface_response
from .openai_model import generate_openai_response

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
                if ai_choice == 'huggingface':
                    response = generate_huggingface_response(user_input)
                elif ai_choice == 'openai':
                    response = generate_openai_response(user_input)
                else:
                    response = 'Invalid AI choice.'
            except Exception as e:
                response = f"Error generating response: {str(e)}"

    return render(request, 'chatbot/index.html', {'response': response})
