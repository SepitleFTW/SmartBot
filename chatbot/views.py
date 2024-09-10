from django.shortcuts import render
from .ai_model import generate_huggingface_response
from .openai_model import generate_openai_response

def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        ai_choice = request.POST.get('ai_choice')

        if ai_choice == 'huggingface':
            response = generate_huggingface_response(user_input)
        elif ai_choice == 'openai':
            response = generate_openai_response(user_input)
        else:
            response = "Invalid AI choice."

        return render(request, 'chatbot/index.html', {'response': response})

    return render(request, 'chatbot/index.html')
