# 🤖 Gemini AI Slack Bot

A powerful Slack bot that uses Socket Mode to process messages and mentions, integrating with Google's Gemini AI to provide intelligent responses. The bot implements comprehensive message handling with Block Kit formatting for visual feedback and includes robust error handling.

## ✨ Features

- 🔌 **Socket Mode Integration**
  - Secure WebSocket connection
  - No public endpoints needed
  - Real-time message processing

- 🧠 **Gemini AI Integration**
  - Advanced language model responses
  - Context-aware conversations
  - Structured output formatting

- 📱 **Slack Block Kit UI**
  - Rich message formatting
  - Visual feedback through reactions
  - Thread support
  - Direct message support

- 🛡️ **Robust Error Handling**
  - Comprehensive logging
  - Visual error feedback
  - Graceful failure recovery

## 🚀 Prerequisites

- Python 3.8 or higher
- Slack Workspace Admin access
- Google Cloud Account (for Gemini API)
- Required API Keys:
  - Slack Bot Token
  - Slack App Token
  - Gemini API Key

## 📦 Installation

1. **Set up on Replit**
   - Fork this repository on Replit
   - Configure environment variables in Replit Secrets
   - Replit will automatically handle dependencies

2. **Manual Installation**
```bash
# Install required Python packages
pip install slack-bolt==1.18.0
pip install litellm==1.10.1
pip install python-dotenv==1.0.0
pip install loguru==0.7.2
```

3. **Set up environment variables**
```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
export GEMINI_API_KEY="your-gemini-api-key"
```

## 🔧 Slack App Configuration

1. Create a new Slack App at [api.slack.com/apps](https://api.slack.com/apps)

2. **Enable Socket Mode**
   - Go to Basic Information → Socket Mode
   - Enable Socket Mode
   - Generate an App-Level Token with `connections:write` scope

3. **Configure Bot Token Scopes**
   - Navigate to OAuth & Permissions
   - Add the following scopes:
     - `app_mentions:read`
     - `chat:write`
     - `im:history`
     - `reactions:write`

4. **Subscribe to Events**
   - In the Event Subscriptions section:
     - Subscribe to `app_mention`
     - Subscribe to `message.im`

5. **Install the App**
   - Install to your workspace
   - Copy the Bot User OAuth Token

## 💻 Usage

### Running the Bot

```bash
python main.py
```

### Interacting with the Bot

1. **Channel Mentions**
```
@bot-name Tell me about Python programming
```

2. **Direct Messages**
- Open a DM with the bot
- Type your message directly

### Example Interactions

1. **Basic Question**
```
User: @bot-name What is Python?
Bot: 🐍 **Python Programming Language**

Python is a versatile, high-level programming language known for:

✨ Key Features:
• Simple, readable syntax
• Large standard library
• Cross-platform compatibility
• Dynamic typing

🚀 Common Uses:
• Web Development
• Data Science
• AI/ML
• Automation
```

2. **Code Example Request**
```
User: @bot-name Show me a hello world example in Python
Bot: 👋 **Python Hello World Example**

Here's a simple Hello World program:

```python
print("Hello, World!")
```

✨ You can also make it more interactive:
```python
name = input("Enter your name: ")
print(f"Hello, {name}!")
```
```

## 📝 Logging

Logs are stored in `logs/slack_bot.log` with the following format:
```
2024-11-16 10:00:00.123 | INFO     | bot:start | === Gemini Slack Bot 起動 ===
```

Log levels:
- DEBUG: Detailed debugging information
- INFO: General operational information
- ERROR: Error conditions and exceptions

## 🔒 Security Considerations

1. **API Key Management**
   - Store API keys securely in environment variables
   - Never commit API keys to version control
   - Rotate API keys periodically

2. **Access Control**
   - Limit bot installation to specific workspaces
   - Review and minimize required OAuth scopes
   - Monitor bot usage and access patterns

3. **Data Privacy**
   - Messages are processed in memory only
   - No persistent storage of conversation data
   - Comply with workspace data retention policies

## 🛠️ Troubleshooting

1. **Bot Not Responding**
   - Verify environment variables are set correctly
   - Check logs for error messages
   - Ensure bot is invited to the channel
   - Verify Socket Mode connection status

2. **API Errors**
   - Validate API key permissions
   - Check rate limits
   - Verify network connectivity
   - Review Gemini API quota

3. **Message Format Issues**
   - Check Block Kit formatting
   - Validate message length limits
   - Review markdown syntax
   - Ensure proper emoji support

## 🚀 Deployment

### Replit Deployment (Recommended)
1. Fork the repository on Replit
2. Set up environment variables in Replit Secrets
3. Click "Run" to start the bot
4. Enable "Always On" for 24/7 operation

### Alternative Deployment Options
1. **Local Machine**
   - Follow manual installation steps
   - Use screen/tmux for persistent running
   - Set up system service (optional)

2. **Cloud Platforms**
   - Deploy as serverless function
   - Use container orchestration
   - Set up auto-scaling (optional)

## 🛠️ Development

### Project Structure
```
├── src/
│   ├── __init__.py
│   ├── bot.py         # Main bot implementation
│   └── config.py      # Configuration and logging setup
├── logs/              # Log files directory
├── main.py           # Application entry point
└── README.md
```

### Key Components

1. **GeminiSlackBot Class** (`src/bot.py`)
   - Handles Slack events
   - Manages message processing
   - Integrates with Gemini AI

2. **Configuration** (`src/config.py`)
   - Environment variable management
   - Logging setup
   - System configuration

### Error Handling

The bot implements multiple layers of error handling:
1. Input validation
2. API error handling
3. Response formatting validation
4. Visual feedback through reactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Slack Bolt for Python](https://slack.dev/bolt-python/concepts)
- [Google Gemini AI](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Slack Block Kit](https://api.slack.com/block-kit)
