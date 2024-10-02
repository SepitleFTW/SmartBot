from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .ai_model import generate_response
from .models import User, Convo

def save_convo(user_id, user_message, bot_response):
    """
    Save the conversation to the database.
    """
    try:
        user = User.objects.get(id=user_id)
        Convo.objects.create(
            user=user,
            message=user_message,
            response=bot_response
        )
    except User.DoesNotExist:
        logging.error(f"User with id {user_id} does not exist.")
    except Exception as e:
        logging.error(f"Error saving conversation: {str(e)}")

def get_convo(user_id):
    """
    Retrieve conversation history for a specific user.
    """
    try:
        user = User.objects.get(id=user_id)
        return Convo.objects.filter(user=user).order_by('-timestamp')
    except User.DoesNotExist:
        logging.error(f"User with id {user_id} does not exist.")
        return Convo.objects.none()  # Return an empty queryset if user does not exist

def index(request):
    return render(request, 'chatbot/index.html')

def chatbot_view(request):
    response = ""
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        ai_choice = request.POST.get('ai_choice', 'gemini')  # Default to gemini

        if not user_input:
            response = 'Please enter some text.'
        else:
            try:
                response = generate_response(user_input, model_choice=ai_choice)
            except Exception as e:
                response = f"Error generating a valid response: {str(e)}"

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
