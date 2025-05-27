from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging
from .utils import get_bot_response, get_conversation_starter, extract_conversation_topics

logger = logging.getLogger(__name__)

def chatbot_page(request):
    """Render the main chatbot interface"""
    return render(request, 'chatbot/chat.html')

class ChatAPIView(View):
    """Enhanced API view for chatbot interactions"""
    
    def get(self, request):
        """Handle GET requests for chat messages"""
        try:
            user_message = request.GET.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({
                    'message': get_conversation_starter(),
                    'success': True,
                    'type': 'starter'
                })
            
            conversation_context = self._get_conversation_context(request)
            
            result = get_bot_response(user_message, conversation_context)
            
            self._update_conversation_history(request, user_message, result)
            
            if result.get('success', True):
                return JsonResponse({
                    'message': result.get('message', 'Sorry, I encountered an issue.'),
                    'success': True,
                    'response_time': result.get('response_time'),
                    'word_count': result.get('word_count'),
                    'context_applied': result.get('context_applied', False)
                })
            else:
                return JsonResponse({
                    'message': result.get('message', 'I apologize for the technical difficulty.'),
                    'success': False,
                    'error_type': result.get('error_type')
                })
                
        except Exception as e:
            logger.error(f"Chat API error: {str(e)}", exc_info=True)
            return JsonResponse({
                'message': '🔧 I\'m experiencing technical difficulties. Please try again!',
                'success': False,
                'error_type': 'api_error'
            })
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        """Handle POST requests for more complex chat interactions"""
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({
                    'error': 'Message cannot be empty',
                    'success': False
                }, status=400)
            
            conversation_context = self._get_conversation_context(request)
            
            if data.get('context'):
                conversation_context.update(data['context'])
            result = get_bot_response(user_message, conversation_context)
            self._update_conversation_history(request, user_message, result)
            
            return JsonResponse(result)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data',
                'success': False
            }, status=400)
        except Exception as e:
            logger.error(f"Chat POST API error: {str(e)}", exc_info=True)
            return JsonResponse({
                'message': '🔧 I\'m experiencing technical difficulties. Please try again!',
                'success': False,
                'error_type': 'api_error'
            })
    
    def _get_conversation_context(self, request):
        """Build conversation context from session data"""
        chat_history = request.session.get('chat_history', [])
        
        return {
            'previous_topics': extract_conversation_topics(chat_history),
            'conversation_length': len(chat_history),
            'session_id': request.session.session_key or 'anonymous'
        }
    
    def _update_conversation_history(self, request, user_message, bot_response):
        """Update conversation history in session"""
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []
        
        # Store user message
        request.session['chat_history'].append(user_message)
        
        # Optionally store bot response for better context
        if bot_response.get('success', True):
            request.session['chat_history'].append(f"[BOT] {bot_response.get('message', '')}")
        
        # Keep only last 20 messages to prevent session bloat
        if len(request.session['chat_history']) > 20:
            request.session['chat_history'] = request.session['chat_history'][-20:]
        
        # Mark session as modified
        request.session.modified = True

def chat_api(request):
    try:
        user_message = request.GET.get('message', '').strip()
        if not user_message:
            return JsonResponse({
                'message': get_conversation_starter(),
                'success': True
            })
        
        chat_history = request.session.get('chat_history', [])
        conversation_context = {
            'previous_topics': extract_conversation_topics(chat_history)
        }
        
        result = get_bot_response(user_message, conversation_context)
        
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []
        
        request.session['chat_history'].append(user_message)
        
        if len(request.session['chat_history']) > 15:
            request.session['chat_history'] = request.session['chat_history'][-15:]
        
        request.session.modified = True
        
        return JsonResponse({
            'message': result.get('message', 'Sorry, I encountered an issue.'),
            'success': result.get('success', True),
            'response_time': result.get('response_time'),
            'context_applied': result.get('context_applied', False)
        })
        
    except Exception as e:
        logger.error(f"Simple chat API error: {str(e)}", exc_info=True)
        return JsonResponse({
            'message': '🔧 Technical difficulties detected! Please try again in a moment.',
            'success': False
        })

def clear_chat_history(request):
    """Clear the chat history from session"""
    if 'chat_history' in request.session:
        del request.session['chat_history']
        request.session.modified = True
    
    return JsonResponse({
        'message': 'Chat history cleared successfully!',
        'success': True
    })

def get_chat_stats(request):
    """Get basic chat statistics"""
    chat_history = request.session.get('chat_history', [])
    
    return JsonResponse({
        'total_messages': len(chat_history),
        'session_active': bool(chat_history),
        'topics_discussed': extract_conversation_topics(chat_history),
        'success': True
    })