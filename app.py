from flask import Flask, render_template, request, jsonify
import re
import json
import os
from datetime import datetime
import random

app = Flask(__name__)

# Ensure the uploads directory exists
os.makedirs('uploads', exist_ok=True)

def detect_tech_conversation(text):
    """Detect if the conversation is tech/SDLC related"""
    tech_keywords = [
        'app', 'application', 'software', 'development', 'code', 'programming',
        'database', 'api', 'website', 'web', 'mobile', 'ios', 'android',
        'system', 'platform', 'server', 'cloud', 'deployment', 'testing',
        'ui', 'ux', 'frontend', 'backend', 'framework', 'integration',
        'authentication', 'security', 'scalable', 'architecture', 'design',
        'requirements', 'specifications', 'sprint', 'agile', 'scrum',
        'repository', 'git', 'version', 'build', 'deploy', 'devops',
        'bug', 'feature', 'functionality', 'performance', 'optimization'
    ]

    text_lower = text.lower()
    tech_count = sum(1 for keyword in tech_keywords if keyword in text_lower)

    return tech_count >= 3

def generate_tech_analysis(text):
    """Generate tech project analysis"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Identify stakeholders
    stakeholders = []
    stakeholder_regex = r'^([^:]+):'
    for line in lines:
        match = re.search(stakeholder_regex, line)
        if match:
            stakeholder = match.group(1).strip()
            stakeholder = re.sub(r'^\[.*?\]\s*', '', stakeholder)
            if stakeholder not in stakeholders and len(stakeholder) < 50:
                stakeholders.append(stakeholder)

    # Extract project type and generate title
    project_title = "Digital Project"
    text_lower = text.lower()

    if any(keyword in text_lower for keyword in ['mobile app', 'ios', 'android']):
        project_title = "Mobile Application Development"
    elif any(keyword in text_lower for keyword in ['website', 'web app', 'e-commerce']):
        project_title = "Web Platform Development"
    elif any(keyword in text_lower for keyword in ['crm', 'customer relationship']):
        project_title = "CRM System Implementation"
    elif any(keyword in text_lower for keyword in ['dashboard', 'analytics']):
        project_title = "Analytics Dashboard Development"
    elif any(keyword in text_lower for keyword in ['api', 'integration']):
        project_title = "System Integration Project"
    elif any(keyword in text_lower for keyword in ['database', 'data']):
        project_title = "Data Management System"

    # Extract requirements using keyword detection
    requirements = []
    requirement_keywords = {
        'mobile': 'Mobile application development',
        'ios': 'iOS platform support',
        'android': 'Android platform support',
        'web': 'Web platform development',
        'database': 'Database design and implementation',
        'api': 'API development and integration',
        'authentication': 'User authentication system',
        'payment': 'Payment processing integration',
        'dashboard': 'Administrative dashboard',
        'reporting': 'Reporting and analytics features',
        'user management': 'User management system',
        'notification': 'Notification system',
        'search': 'Search functionality',
        'integration': 'Third-party system integration',
        'security': 'Security implementation',
        'responsive': 'Responsive design',
        'real-time': 'Real-time data processing',
        'cloud': 'Cloud infrastructure setup',
        'backup': 'Data backup and recovery',
        'scalable': 'Scalable architecture design'
    }

    for keyword, requirement in requirement_keywords.items():
        if keyword in text_lower and requirement not in requirements:
            requirements.append(requirement)

    if not requirements:
        requirements = [
            'System architecture design',
            'User interface development',
            'Database implementation',
            'Testing and quality assurance',
        ]

    # Generate timeline based on project complexity
    complexity = len(requirements)
    total_weeks = 8

    if complexity > 10:
        total_weeks = 16
    elif complexity > 7:
        total_weeks = 12
    elif complexity > 5:
        total_weeks = 10

    # Extract timeline mentions from text
    timeline_matches = re.findall(r'(\d+)\s*(week|month|day)s?', text, re.IGNORECASE)
    if timeline_matches:
        time_value, time_unit = timeline_matches[0]
        time_value = int(time_value)
        if 'month' in time_unit.lower():
            total_weeks = time_value * 4
        elif 'week' in time_unit.lower():
            total_weeks = time_value

    # Generate phase-specific tasks
    phases = [
        {
            "phase": "Requirements Gathering",
            "tasks": [
                "Conduct stakeholder interviews",
                "Document functional requirements",
                "Create user stories and acceptance criteria",
                "Define technical specifications",
                "Establish project scope and constraints"
            ],
            "duration": f"{max(1, round(total_weeks * 0.15))} weeks",
            "priority": "High",
            "color": "blue"
        },
        {
            "phase": "Design & Planning",
            "tasks": [
                "Create system architecture design",
                "Develop UI/UX wireframes and mockups",
                "Design database schema",
                "Plan development sprints",
                "Set up project infrastructure"
            ],
            "duration": f"{max(1, round(total_weeks * 0.2))} weeks",
            "priority": "High",
            "color": "purple"
        },
        {
            "phase": "Development",
            "tasks": [
                "Set up development environment",
                "Implement core functionality",
                "Develop user interface components",
                "Build backend services and APIs",
                "Integrate third-party services"
            ],
            "duration": f"{max(1, round(total_weeks * 0.45))} weeks",
            "priority": "Critical",
            "color": "green"
        },
        {
            "phase": "Testing",
            "tasks": [
                "Unit testing implementation",
                "Integration testing",
                "User acceptance testing",
                "Performance and load testing",
                "Security testing and validation"
            ],
            "duration": f"{max(1, round(total_weeks * 0.15))} weeks",
            "priority": "High",
            "color": "orange"
        },
        {
            "phase": "Deployment",
            "tasks": [
                "Production environment setup",
                "Deployment automation",
                "Go-live support and monitoring",
                "User training and documentation",
                "Post-launch support planning"
            ],
            "duration": f"{max(1, round(total_weeks * 0.05))} weeks",
            "priority": "High",
            "color": "red"
        }
    ]

    # Generate risk factors
    risk_factors = []

    if any(keyword in text_lower for keyword in ['tight', 'urgent', 'asap']):
        risk_factors.append("Aggressive timeline may require additional resources or scope reduction")

    if 'budget' in text_lower and 'limited' in text_lower:
        risk_factors.append("Budget constraints may impact feature scope or timeline")

    if 'integration' in text_lower or 'legacy' in text_lower:
        risk_factors.append("Legacy system integration complexity may cause delays")

    if 'compliance' in text_lower or 'regulation' in text_lower:
        risk_factors.append("Regulatory compliance requirements need careful validation")

    if len(stakeholders) > 5:
        risk_factors.append("Multiple stakeholders may require additional coordination and communication")

    if not risk_factors:
        risk_factors = [
            "Scope creep during development phase",
            "Third-party service dependencies may cause integration challenges",
            "User acceptance testing may reveal additional requirements"
        ]

    return {
        "type": "tech",
        "projectTitle": project_title,
        "stakeholders": stakeholders if stakeholders else ["Client", "Project Team"],
        "requirements": requirements,
        "todos": phases,
        "timeline": f"{total_weeks} weeks total",
        "riskFactors": risk_factors
    }

def generate_general_analysis(text):
    """Generate general todo list analysis"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Identify participants
    participants = []
    participant_regex = r'^([^:]+):'
    for line in lines:
        match = re.search(participant_regex, line)
        if match:
            participant = match.group(1).strip()
            participant = re.sub(r'^\[.*?\]\s*', '', participant)
            if participant not in participants and len(participant) < 50:
                participants.append(participant)

    # Determine conversation type
    text_lower = text.lower()
    conversation_title = "General Discussion"

    if any(keyword in text_lower for keyword in ['meeting', 'agenda', 'minutes']):
        conversation_title = "Team Meeting"
    elif any(keyword in text_lower for keyword in ['event', 'party', 'celebration', 'wedding']):
        conversation_title = "Event Planning"
    elif any(keyword in text_lower for keyword in ['business', 'strategy', 'plan', 'goals']):
        conversation_title = "Business Planning"
    elif any(keyword in text_lower for keyword in ['project', 'task', 'deadline']):
        conversation_title = "Project Discussion"
    elif any(keyword in text_lower for keyword in ['budget', 'finance', 'cost', 'money']):
        conversation_title = "Financial Planning"
    elif any(keyword in text_lower for keyword in ['travel', 'trip', 'vacation']):
        conversation_title = "Travel Planning"

    # Extract action items
    action_items = []
    action_keywords = ['need to', 'should', 'must', 'have to', 'will', 'going to', 'plan to', 'decide', 'contact', 'call', 'email', 'schedule', 'book', 'order', 'buy', 'prepare', 'organize', 'arrange']

    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in action_keywords):
            # Clean up the line and extract the action
            action = re.sub(r'^[^:]*:', '', line).strip()
            if len(action) > 10 and len(action) < 200:
                action_items.append(action)

    # If no specific actions found, generate generic ones
    if not action_items:
        action_items = [
            "Follow up on discussed topics",
            "Schedule next meeting or check-in",
            "Review and confirm decisions made",
            "Prepare materials for next steps",
            "Communicate updates to relevant parties"
        ]

    # Categorize items
    categories = []
    if any(keyword in text_lower for keyword in ['meeting', 'call', 'discuss']):
        categories.append("Communication")
    if any(keyword in text_lower for keyword in ['plan', 'organize', 'schedule']):
        categories.append("Planning")
    if any(keyword in text_lower for keyword in ['research', 'find', 'look up']):
        categories.append("Research")
    if any(keyword in text_lower for keyword in ['buy', 'order', 'purchase']):
        categories.append("Procurement")
    if any(keyword in text_lower for keyword in ['prepare', 'create', 'make']):
        categories.append("Preparation")
    if any(keyword in text_lower for keyword in ['review', 'check', 'verify']):
        categories.append("Review")

    if not categories:
        categories = ["General Tasks", "Follow-up"]

    # Determine priorities
    priorities = []
    if any(keyword in text_lower for keyword in ['urgent', 'asap', 'immediately', 'critical']):
        priorities.append("High Priority - Urgent items requiring immediate attention")
    if any(keyword in text_lower for keyword in ['important', 'key', 'crucial', 'essential']):
        priorities.append("Important - Key items for project success")
    if any(keyword in text_lower for keyword in ['later', 'eventually', 'when possible']):
        priorities.append("Low Priority - Items to address when time permits")

    if not priorities:
        priorities = ["Normal Priority - Standard follow-up items"]

    # Generate next steps
    next_steps = [
        "Review all action items and assign responsibilities",
        "Set deadlines for each identified task",
        "Schedule follow-up meeting or check-in",
        "Begin work on highest priority items",
        "Communicate progress to all stakeholders"
    ]

    # Estimate timeline
    timeline = "1-2 weeks"
    if len(action_items) > 10:
        timeline = "3-4 weeks"
    elif len(action_items) > 5:
        timeline = "2-3 weeks"

    return {
        "type": "general",
        "conversationTitle": conversation_title,
        "participants": participants if participants else ["Participant 1", "Participant 2"],
        "actionItems": action_items[:10],  # Limit to 10 items
        "categories": categories,
        "priorities": priorities,
        "nextSteps": next_steps,
        "timeline": timeline
    }

def generate_analysis_from_transcript(text):
    """Main analysis function that routes to tech or general analysis"""
    if detect_tech_conversation(text):
        return generate_tech_analysis(text)
    else:
        return generate_general_analysis(text)

# ... (rest of the helper functions remain the same)

def extract_youtube_video_id(url):
    """Extract YouTube video ID from URL"""
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def process_youtube_url(url):
    """Process YouTube URL and return simulated transcript"""
    video_id = extract_youtube_video_id(url) or "unknown"

    return f"""[Processed from YouTube Video: {video_id}]

Meeting Transcript - {datetime.now().strftime('%Y-%m-%d')}

Note: This is a demonstration of YouTube processing. In production, this would:
1. Use YouTube Data API to fetch video metadata
2. Extract audio using youtube-dl or similar
3. Process audio through speech-to-text service (Google Cloud Speech, AWS Transcribe, etc.)
4. Return the actual transcript

For now, here's a sample of what the processed content might look like:

Project Manager: Welcome to our project discussion. We're reviewing the requirements for the new system.

Client: Thank you for having us. We need a comprehensive solution that can handle our growing business needs.

Developer: What are the main challenges you're facing with your current setup?

Client: Our current system is outdated and doesn't scale well. We need something modern and efficient.

Project Manager: What's your target timeline for this project?

Client: We're hoping to have everything ready within 6 months.

[End of processed transcript]"""

def process_json_file(content):
    """Process JSON file content and extract transcript"""
    try:
        json_data = json.loads(content)
        extracted_transcript = ""

        if "transcript" in json_data:
            extracted_transcript = json_data["transcript"]
        elif "conversation" in json_data:
            if isinstance(json_data["conversation"], list):
                extracted_transcript = "\n\n".join([
                    f"{msg.get('speaker', 'Speaker')}: {msg.get('text', msg.get('message', ''))}"
                    for msg in json_data["conversation"]
                ])
            else:
                extracted_transcript = json_data["conversation"]
        elif "messages" in json_data:
            extracted_transcript = "\n\n".join([
                f"{msg.get('sender', msg.get('user', 'Speaker'))}: {msg.get('text', msg.get('content', msg.get('message', '')))}"
                for msg in json_data["messages"]
            ])
        elif isinstance(json_data, list):
            extracted_transcript = "\n\n".join([
                f"{item.get('speaker', item.get('name', f'Speaker {i+1}'))}: {item.get('text', item.get('message', item.get('content', item)))}"
                if isinstance(item, dict) else f"Speaker {i+1}: {item}"
                for i, item in enumerate(json_data)
            ])
        else:
            text_content = extract_text_from_object(json_data)
            extracted_transcript = text_content or "Unable to automatically extract conversation format."

        if not extracted_transcript.strip():
            extracted_transcript = "No conversation data found in the expected format."

        return extracted_transcript
    except Exception as e:
        return f"Error processing JSON: {str(e)}"

def extract_text_from_object(obj, max_depth=3, current_depth=0):
    """Extract text content from nested JSON object"""
    if current_depth > max_depth:
        return ""

    text = ""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and len(value) > 10:
                text += f"{key}: {value}\n\n"
            elif isinstance(value, (dict, list)):
                text += extract_text_from_object(value, max_depth, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            text += extract_text_from_object(item, max_depth, current_depth + 1)

    return text

def process_audio_file(filename, file_type, file_size):
    """Process audio file and return simulated transcript"""
    return f"""[Transcribed from audio file: {filename}]

Audio Processing Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Note: This is a demonstration of audio processing. In production, this would:
1. Upload audio to speech-to-text service (Google Cloud Speech API, AWS Transcribe, AssemblyAI, etc.)
2. Process audio with speaker diarization to identify different speakers
3. Return timestamped transcript with speaker labels

Sample of what the processed audio might contain:

Speaker 1: Hello everyone, thank you for joining today's project meeting.

Speaker 2: Thanks for having us. We're excited to discuss the new system requirements.

Speaker 1: Let's start by reviewing what we need to accomplish.

Speaker 2: Our main priority is improving user experience and system performance.

Speaker 1: What timeline are we working with?

Speaker 2: We'd like to have the initial version ready in about 3 months.

[End of transcribed content]

File Details:
- Duration: ~{round(file_size / 16000)} seconds (estimated)
- Size: {round(file_size / 1024 / 1024, 2)} MB
- Format: {file_type}"""

def process_video_file(filename, file_type, file_size):
    """Process video file and return simulated transcript"""
    return f"""[Transcribed from video file: {filename}]

Video Processing Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Note: This is a demonstration of video processing. In production, this would:
1. Extract audio track from video file using FFmpeg
2. Process audio through speech-to-text service
3. Optionally analyze video for speaker identification and scene detection
4. Return comprehensive transcript with timestamps

Sample of what the processed video might contain:

[00:00:15] Project Manager: Welcome to our video conference. Can everyone see the screen?

[00:00:22] Client Representative: Yes, we can see everything clearly.

[00:00:28] Technical Lead: The presentation looks good on our end as well.

[00:00:35] Project Manager: Excellent. Let's begin with the project overview.

[00:00:42] Client Representative: We're looking to modernize our current system and improve efficiency.

[00:00:58] Technical Lead: What are your main pain points with the existing solution?

[00:01:05] Client Representative: The system is slow and doesn't integrate well with our other tools.

[End of transcribed content]

File Details:
- Duration: ~{round(file_size / 1000000)} minutes (estimated)
- Size: {round(file_size / 1024 / 1024, 2)} MB
- Format: {file_type}"""

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze transcript and return results"""
    data = request.form
    transcript = data.get('transcript', '')

    if not transcript.strip():
        return jsonify({'error': 'No transcript provided'}), 400

    analysis = generate_analysis_from_transcript(transcript)
    return jsonify(analysis)

@app.route('/process-youtube', methods=['POST'])
def process_youtube():
    """Process YouTube URL and return transcript"""
    data = request.form
    youtube_url = data.get('youtube_url', '')

    if not youtube_url.strip():
        return jsonify({'error': 'No YouTube URL provided'}), 400

    transcript = process_youtube_url(youtube_url)
    return jsonify({'transcript': transcript})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    """Process uploaded file and return transcript"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_type = file.content_type
    file_size = 0

    temp_path = os.path.join('uploads', filename)
    file.save(temp_path)
    file_size = os.path.getsize(temp_path)

    transcript = ""

    if file_type == 'application/json':
        with open(temp_path, 'r') as f:
            content = f.read()
        transcript = f"[Processed from JSON file: {filename}]\n\n{process_json_file(content)}"
    elif file_type.startswith('audio/'):
        transcript = process_audio_file(filename, file_type, file_size)
    elif file_type.startswith('video/'):
        transcript = process_video_file(filename, file_type, file_size)
    else:
        transcript = f"Unsupported file type: {file_type}"

    try:
        os.remove(temp_path)
    except:
        pass

    return jsonify({'transcript': transcript})

@app.route('/sample-transcript')
def sample_transcript():
    """Return a sample transcript"""
    tech_sample = """Client: We need a mobile app for our restaurant chain. Customers should be able to browse our menu, place orders, and track delivery. We have 15 locations across the city.

PM: What payment methods do you want to support?

Client: Credit cards, PayPal, and maybe Apple Pay. We also want loyalty points - customers earn points with each order.

Developer: Do you need real-time order tracking?

Client: Yes, customers should see when their order is being prepared, ready for pickup, or out for delivery. We also need an admin dashboard for restaurant managers.

Client: Timeline is important - we want to launch before the holiday season, so maybe 3 months max?

PM: Any specific design requirements?

Client: Nothing too fancy, but it should match our brand colors - red and yellow. Easy to use for all ages."""

    general_sample = """Sarah: Thanks everyone for joining today's meeting. We need to plan the company retreat for next month.

Mike: What's our budget looking like for this event?

Sarah: We have about $5,000 to work with. I'm thinking we should book a venue first, then plan activities around it.

Lisa: I can research some venues this week. Should we look for something within 50 miles of the office?

Sarah: That sounds perfect. We also need to decide on catering. Mike, can you get quotes from a few restaurants?

Mike: Absolutely. I'll have those by Friday. What about team building activities?

Lisa: I have some contacts for outdoor activities like rope courses and scavenger hunts.

Sarah: Great! Let's also send out a survey to see what the team prefers. We need to finalize everything by the end of next week."""

    # Randomly choose between tech and general sample
    sample = tech_sample if random.choice([True, False]) else general_sample

    return jsonify({'transcript': sample})

if __name__ == '__main__':
    app.run(debug=True)