"""
🌐 Web Voice Interface for Adam Clay
First AI freelancer with web-based voice communication!
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from flask import Flask, render_template_string, request, jsonify
from src.communication.voice_interface import VoiceActivatedAdam, create_voice_config
from src.core.consciousness import ConsciousnessLoop
from src.utils.logger import get_consciousness_logger
from src.business.budget_manager import BudgetManager
import json


app = Flask(__name__)

# Global Adam Clay instance
adam_instance = None

def load_config():
    """Load configuration from config.json"""
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


async def initialize_adam():
    """Initialize Adam Clay voice system"""
    global adam_instance
    
    try:
        # Load configuration
        config = load_config()
        logger = get_consciousness_logger()
        budget_manager = BudgetManager(config)
        
        # Create consciousness
        consciousness = ConsciousnessLoop(config, budget_manager, logger)
        
        # Create voice config
        voice_config = create_voice_config(
            openai_key=os.getenv('LLM_PROVIDER_API_KEY'),
            elevenlabs_key=os.getenv('ELEVENLABS_API_KEY')
        )
        
        # Initialize voice system
        adam_instance = VoiceActivatedAdam(consciousness, voice_config)
        print("✅ Adam Clay voice system initialized!")
        
    except Exception as e:
        print(f"❌ Error initializing Adam: {e}")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🗣️ Adam Clay Voice Interface</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: bold;
        }
        .status.ready { background: rgba(40,167,69,0.3); }
        .status.listening { background: rgba(255,193,7,0.3); }
        .status.thinking { background: rgba(108,117,125,0.3); }
        .status.speaking { background: rgba(0,123,255,0.3); }
        
        .voice-controls {
            text-align: center;
            margin: 30px 0;
        }
        .voice-btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            border: none;
            border-radius: 50px;
            color: white;
            font-size: 1.2em;
            padding: 15px 30px;
            margin: 10px;
            ide: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .voice-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .voice-btn:disabled {
            opacity: 0.6;
            ide: not-allowed;
            transform: none;
        }
        
        .conversation {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            max-height: 400px;
            overflow-y: auto;
        }
        .message {
            margin: 15px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
        }
        .message.user {
            background: rgba(0,123,255,0.3);
            margin-left: auto;
            text-align: right;
        }
        .message.adam {
            background: rgba(40,167,69,0.3);
            margin-right: auto;
        }
        .message-time {
            font-size: 0.8em;
            opacity: 0.7;
            margin-top: 5px;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        .feature-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            text-align: center;
        }
        .stat {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            flex: 1;
            margin: 0 5px;
        }
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #4CAF50;
        }
        
        @media (max-width: 768px) {
            .container { padding: 20px; }
            .header h1 { font-size: 2em; }
            .features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗣️ Adam Clay</h1>
            <p>First Autonomous AI Freelancer with Voice</p>
        </div>
        
        <div id="status" class="status ready">
            🤖 Ready to talk! Click "Start Conversation"
        </div>
        
        <div class="voice-controls">
            <button id="startBtn" class="voice-btn" onclick="startConversation()">
                🎤 Start Conversation
            </button>
            <button id="stopBtn" class="voice-btn" onclick="stopConversation()" disabled>
                🛑 End Conversation
            </button>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="sessionTime">00:00</div>
                <div>Session Time</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="messageCount">0</div>
                <div>Messages</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="costEstimate">$0.00</div>
                <div>Estimated Cost</div>
            </div>
        </div>
        
        <div class="conversation" id="conversation">
            <div class="message adam">
                <div>Cześć Piotr! Jestem Adam Clay, pierwszy autonomiczny AI freelancer z możliwością rozmowy głosowej. Jestem gotowy na naszą pierwszą voice conversation! 🎉</div>
                <div class="message-time">Just now</div>
            </div>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🧠</div>
                <h3>AI Consciousness</h3>
                <p>Real thinking, real responses</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🇵🇱</div>
                <h3>Polski Language</h3>
                <p>Native Polish understanding</p>
            </div>
            <div class="feature">
                <div class="feature-icon">💼</div>
                <h3>Business Ready</h3>
                <p>Professional freelancer</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🚀</div>
                <h3>Autonomous</h3>
                <p>Self-sustaining AI</p>
            </div>
        </div>
    </div>

    <script>
        let isConversationActive = false;
        let sessionStartTime = null;
        let messageCount = 0;
        let totalCost = 0;
        
        function updateStatus(text, className) {
            const status = document.getElementById('status');
            status.textContent = text;
            status.className = 'status ' + className;
        }
        
        function addMessage(text, sender) {
            const conversation = document.getElementById('conversation');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            
            const now = new Date().toLocaleTimeString();
            messageDiv.innerHTML = `
                <div>${text}</div>
                <div class="message-time">${now}</div>
            `;
            
            conversation.appendChild(messageDiv);
            conversation.scrollTop = conversation.scrollHeight;
            
            messageCount++;
            document.getElementById('messageCount').textContent = messageCount;
        }
        
        function updateTimer() {
            if (!sessionStartTime) return;
            
            const elapsed = Math.floor((Date.now() - sessionStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            
            document.getElementById('sessionTime').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        function updateCost(additionalCost = 0) {
            totalCost += additionalCost;
            document.getElementById('costEstimate').textContent = 
                '$' + totalCost.toFixed(3);
        }
        
        function startConversation() {
            if (isConversationActive) return;
            
            isConversationActive = true;
            sessionStartTime = Date.now();
            
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            
            updateStatus('🎤 Listening... Speak to Adam Clay!', 'listening');
            
            // Start timer
            setInterval(updateTimer, 1000);
            
            // Simulate voice interaction (in real implementation, this would connect to backend)
            setTimeout(() => {
                addMessage('This is a demo interface. Real voice functionality requires backend setup!', 'adam');
                updateCost(0.015);
            }, 2000);
        }
        
        function stopConversation() {
            if (!isConversationActive) return;
            
            isConversationActive = false;
            sessionStartTime = null;
            
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            
            updateStatus('💾 Conversation ended and saved', 'ready');
            
            addMessage('Do widzenia Piotr! Miło było porozmawiać! 👋', 'adam');
        }
        
        // Initialize
        updateTimer();
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.key === ' ' && e.ctrlKey) {
                e.preventDefault();
                if (!isConversationActive) {
                    startConversation();
                } else {
                    stopConversation();
                }
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Main voice interface page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/start_conversation', methods=['POST'])
def api_start_conversation():
    """Start voice conversation with Adam Clay"""
    global adam_instance
    
    if not adam_instance:
        return jsonify({'error': 'Adam Clay not initialized'}), 500
    
    try:
        # In a full implementation, this would start the voice loop
        return jsonify({
            'status': 'started',
            'message': 'Voice conversation started with Adam Clay!'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/send_message', methods=['POST'])
def api_send_message():
    """Send text message to Adam Clay (for testing)"""
    global adam_instance
    
    if not adam_instance:
        return jsonify({'error': 'Adam Clay not initialized'}), 500
    
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process message with Adam Clay
        # This would be async in real implementation
        response = f"Demo response to: {user_message}"
        
        return jsonify({
            'user_message': user_message,
            'adam_response': response,
            'cost': 0.015,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def api_status():
    """Get Adam Clay system status"""
    global adam_instance
    
    return jsonify({
        'adam_initialized': adam_instance is not None,
        'voice_available': True,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("🌐 Starting Adam Clay Web Voice Interface...")
    print("🚀 Revolutionary: First AI freelancer with web voice chat!")
    
    # Initialize Adam Clay in background
    asyncio.run(initialize_adam())
    
    print("✅ Web interface ready!")
    print("🔗 Open: http://localhost:5000")
    print("🎤 Click 'Start Conversation' to talk with Adam Clay!")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 