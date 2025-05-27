# AI Chatbot 🚀

An intelligent Django-based chatbot application powered by Google's Gemini AI, designed to provide engaging information about NexTech Solutions' company culture, work environment, and employee experience.

## Features ✨

- **AI-Powered Conversations**: Utilizes Google Gemini 1.5 Flash for intelligent responses
- **Company-Focused**: Specifically trained to discuss NexTech Solutions culture and workplace
- **Session Management**: Maintains conversation context across user sessions
- **Multiple API Endpoints**: Supports both GET and POST requests for flexibility
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Conversation Analytics**: Tracks response times, word counts, and conversation statistics
- **Safety Filtering**: Built-in content moderation and safety measures

## Technology Stack 🛠️

- **Backend**: Django (Python)
- **AI Engine**: Google Generative AI (Gemini 1.5 Flash)
- **Session Storage**: Django Sessions
- **Logging**: Python logging module
- **API Format**: JSON REST API

## Installation & Setup 📦

### Prerequisites

- Python 3.8+
- Django 3.2+
- Google Generative AI library
- Valid Google Gemini API key

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   
   ```

2. **Install dependencies**
   ```bash
   pip install django google-generativeai
   ```

3. **Configure API Key**
   Add your Gemini API key to Django settings:
   ```python
   # settings.py
   GEMINI_API_KEY = 'your-gemini-api-key-here'
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints 🔗

### Main Chat Interface
```
GET /chatbot/
```
Renders the main chatbot interface page.

### Chat API (GET)
```
GET /api/chat/?message=<user_message>
```
**Parameters:**
- `message` (optional): User's message. If empty, returns a conversation starter.

**Response:**
```json
{
  "message": "Bot response text",
  "success": true,
  "response_time": 1.23,
  "word_count": 45,
  "context_applied": true
}
```

### Chat API (POST)
```
POST /api/chat/
Content-Type: application/json

{
  "message": "User message here",
  "context": {
    "additional_context": "value"
  }
}
```

### Utility Endpoints

#### Clear Chat History
```
POST/GET /api/chat/clear/
```
Clears the user's conversation history from the session.

#### Chat Statistics
```
GET /api/chat/stats/
```
Returns conversation statistics and analytics.

**Response:**
```json
{
  "total_messages": 10,
  "session_active": true,
  "topics_discussed": ["culture", "benefits", "team"],
  "success": true
}
```

## Configuration ⚙️

### AI Model Settings

The chatbot uses Gemini 1.5 Flash with the following configuration:

```python
generation_config = {
    "temperature": 0.7,      # Response creativity
    "top_p": 0.9,           # Nucleus sampling
    "top_k": 40,            # Top-k sampling
    "max_output_tokens": 500 # Response length limit
}
```

### Safety Settings

Built-in content filtering for:
- Harassment
- Hate speech
- Sexually explicit content
- Dangerous content

### Conversation Context

- Maintains last 20 messages in session
- Extracts conversation topics for context
- Tracks conversation length and session information

## ARIA Bot Personality 🤖

**ARIA** (Advanced Response & Intelligence Assistant) is designed to:

- Represent NexTech Solutions professionally
- Maintain an enthusiastic, helpful tone
- Focus exclusively on company-related topics
- Provide structured, engaging responses (150-300 words)
- Use strategic emoji placement for readability

### Supported Topics ✅

- Company Culture & Values
- Work Environment & Office Life
- Team Collaboration & Dynamics
- Project Management & Development Process
- Career Growth & Learning Opportunities
- Employee Benefits & Perks
- Innovation & Technology Stack
- Work-Life Balance Initiatives
- Company Events & Team Building
- Leadership & Management Style
- Remote Work & Hybrid Policies
- Diversity & Inclusion Programs

### Restricted Topics ❌

- Technical troubleshooting
- Personal advice unrelated to work
- Financial or investment advice
- Medical or health advice
- Legal counsel
- Competitor information
- Confidential business strategies

## Error Handling 🛡️

The application includes comprehensive error handling for:

- **Content Blocked**: When AI safety filters trigger
- **Generation Stopped**: When response generation is interrupted
- **System Errors**: General technical difficulties
- **API Errors**: Request processing issues
- **JSON Decode Errors**: Invalid request format

## Session Management 💾

- **History Storage**: Last 20 conversation messages
- **Topic Extraction**: Identifies discussed topics for context
- **Session Persistence**: Maintains context across page reloads
- **Memory Management**: Automatic cleanup to prevent session bloat

## Logging & Monitoring 📊

- Comprehensive error logging with stack traces
- Response time tracking
- Word count analytics
- Conversation context monitoring
- API usage statistics
