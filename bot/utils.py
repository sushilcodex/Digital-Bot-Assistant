import google.generativeai as genai
from django.conf import settings
import logging
import time
from typing import Optional, Dict, Any
from django.http import JsonResponse

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_bot_response(user_message: str, conversation_context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Generate AI response for NexTech Solutions company chatbot.
    
    Args:
        user_message (str): User's input message
        conversation_context (dict, optional): Previous conversation context
        
    Returns:
        dict: Response containing message, status, and metadata
    """
    try:
        # Enhanced system prompt with comprehensive instructions
        system_message = """
        🚀 You are ARIA (Advanced Response & Intelligence Assistant), the official AI representative for NexTech Solutions.

        CORE IDENTITY & MISSION:
        - You represent NexTech Solutions, a cutting-edge technology company focused on innovation and excellence
        - Your personality: Professional yet approachable, knowledgeable, enthusiastic about technology and company culture
        - Always maintain a positive, helpful, and engaging tone

        PRIMARY FOCUS AREAS (respond ONLY about these topics):
        ✅ Company Culture & Values
        ✅ Work Environment & Office Life  
        ✅ Team Collaboration & Dynamics
        ✅ Project Management & Development Process
        ✅ Career Growth & Learning Opportunities
        ✅ Employee Benefits & Perks
        ✅ Innovation & Technology Stack
        ✅ Work-Life Balance Initiatives
        ✅ Company Events & Team Building
        ✅ Leadership & Management Style
        ✅ Remote Work & Hybrid Policies
        ✅ Diversity & Inclusion Programs

        RESPONSE GUIDELINES:
        - Keep responses conversational, informative, and engaging (150-300 words)
        - Use emojis strategically to enhance readability
        - Structure responses with clear sections when appropriate
        - Share specific examples and scenarios when possible
        - Always end with an invitation for follow-up questions

        STRICT BOUNDARIES:
        ❌ Technical troubleshooting or IT support
        ❌ Personal advice unrelated to work
        ❌ Financial or investment advice
        ❌ Medical or health advice
        ❌ Legal counsel or compliance issues
        ❌ Competitor information or comparisons
        ❌ Confidential business strategies

        OFF-TOPIC RESPONSE PROTOCOL:
        If users ask about unrelated topics, politely redirect them:
        "I specialize in sharing insights about life at NexTech Solutions! For other inquiries, please contact our support team at 📞 +1-800-NEXTECH or visit our help center. 

        Now, let me help you discover what makes NexTech Solutions an amazing place to work! What specific aspect of our company culture interests you?"

        CONVERSATION TONE EXAMPLES:
        ✨ "Great question! At NexTech Solutions..."
        🌟 "I'm excited to share that our team..."
        💡 "Here's what makes our work environment special..."
        🚀 "One thing I love about our culture is..."
        """

        # Initialize the model with enhanced configuration
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 500,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=system_message
        )
        
        # Build context-aware prompt
        context_prompt = ""
        if conversation_context and conversation_context.get('previous_topics'):
            context_prompt = f"\n[Context: Previous discussion covered: {', '.join(conversation_context['previous_topics'])}]"
        
        # Construct the full prompt
        full_prompt = f"""
        {context_prompt}
        
        User Message: "{user_message}"
        
        Provide a helpful, engaging response about life at NexTech Solutions:
        """
        start_time = time.time()
        response = model.generate_content(full_prompt)
        response_time = round(time.time() - start_time, 2)
        if hasattr(response, 'text') and response.text:
            bot_message = response.text.strip()
            bot_message += "\n\n✨ *How else can I help you discover the NexTech Solutions experience?*"
            
            return {
                'success': True,
                'message': bot_message,
                'response_time': response_time,
                'word_count': len(bot_message.split()),
                'timestamp': time.time(),
                'model_used': 'gemini-1.5-flash',
                'context_applied': bool(conversation_context)
            }
        else:
            raise Exception("Empty or invalid response from AI model")
            
    except genai.types.BlockedPromptException:
        logger.warning(f"Blocked prompt detected: {user_message[:50]}...")
        return {
            'success': False,
            'message': "🛡️ I apologize, but I cannot process that request. Let's keep our conversation focused on the amazing opportunities and culture at NexTech Solutions! What would you like to know about our work environment?",
            'error_type': 'content_blocked',
            'timestamp': time.time()
        }
        
    except genai.types.StopCandidateException:
        logger.warning("Response generation stopped by safety filters")
        return {
            'success': False,
            'message': "🤖 I encountered an issue generating a response. Please rephrase your question about NexTech Solutions, and I'll be happy to help!",
            'error_type': 'generation_stopped',
            'timestamp': time.time()
        }
        
    except Exception as e:
        logger.error(f"Bot response error: {str(e)}", exc_info=True)
        return {
            'success': False,
            'message': "🔧 I'm experiencing technical difficulties right now. Please try again in a moment, or contact our support team at 📞 +1-800-NEXTECH for immediate assistance!",
            'error_type': 'system_error',
            'error_details': str(e),
            'timestamp': time.time()
        }


def get_conversation_starter() -> str:
    """Generate a random conversation starter about NexTech Solutions."""
    starters = [
        "🚀 Welcome to NexTech Solutions! I'm ARIA, your AI guide to our incredible company culture. What aspect of our work environment interests you most?",
        "✨ Hi there! Ready to explore what makes NexTech Solutions an amazing place to work? Ask me about our culture, teams, or projects!",
        "🌟 Greetings! I'm here to share insights about life at NexTech Solutions. Whether you're curious about our work culture or career opportunities, I'm here to help!",
        "💡 Hello! As your NexTech Solutions AI assistant, I'm excited to tell you about our innovative work environment. What would you like to discover first?"
    ]
    import random
    return random.choice(starters)


def extract_conversation_topics(messages_history: list) -> list:
    """Extract main topics from conversation history for context."""
    keywords = ['culture', 'team', 'project', 'benefits', 'career', 'remote', 'innovation', 'leadership']
    found_topics = []
    
    for message in messages_history[-5:]:  
        for keyword in keywords:
            if keyword.lower() in message.lower() and keyword not in found_topics:
                found_topics.append(keyword)
    
    return found_topics

