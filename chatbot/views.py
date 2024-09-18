from django.shortcuts import render
from django.http import HttpResponse
from .ai_model import generate_response
from .models import User, Convo
from .services import generate_response

def save_convo(user_id, user_message, bot_response):
    """
    these functions will save and rettrieve conversations
    """
    user = User.objects.get(id=user.id)
    Convo.objects.create(
        user=user,
        message=user_message,
        response=bot_response
    )


def get_convo(user_id):
    """this function as stated above will get the convos in history
    """
    user = User.objects.get(id=user_id)
    return Convo.objects.filter(user=user).order_by('-timestamp')
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

def conversation_logs(request):
    # Logic to retrieve and display conversation logs
    return render(request, 'chatbot/conversation_logs.html')

def user_data(request):
    # Your logic for displaying user data
    return render(request, 'chatbot/user_data.html')

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('text')
        response_text = generate_response(user_input)

        return JsonResponse({'response': response_text})
    
    return render(request, 'chatbot/chat.html')

