from django.shortcuts import render 
from django.http import JsonResponse
from .models import ChatMessage,QuestionAnswer
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def chatbot_view(request):
    messages = ChatMessage.objects.all().order_by('timestamp')
    return render(request, 'chatbot.html', {'messages': messages})

@csrf_exempt
def save_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            # Save the user's message
            user_msg = ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=message_text,
                is_bot=False
            )

            message_lower = message_text.lower().strip()
            bot_response = "I'm sorry, I don't understand your question. Could you please rephrase it or check the Services page for more information: /services/"

            try:
                # Fetch question-answer pairs from the database
                qa_pairs = QuestionAnswer.objects.all()
                for qa in qa_pairs:
                    keywords = qa.keywords.lower().split(',')
                    if any(keyword.strip() in message_lower for keyword in keywords):
                        bot_response = qa.answer
                        break
            except Exception as e:
                # Log the error (you can use logging instead of print in production)
                print(f"Error fetching question-answer pairs: {e}")
                bot_response = "I'm sorry, there was an issue processing your request. Please try again later."

            # Save the bot's response
            bot_message = ChatMessage.objects.create(
                user=None,
                message=bot_response,
                is_bot=True
            )

            return JsonResponse({
                'status': 'success',
                'bot_message': bot_message.message,
                'bot_timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)