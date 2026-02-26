import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import random
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Rock Paper Scissors AI",
    page_icon="🎮",
    layout="wide"
)

# Modern CSS Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .card-header {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .score-display {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .score-item {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 12px;
        flex: 1;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
    }
    
    .score-label {
        color: rgba(255,255,255,0.8);
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .score-value {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    
    .mode-selector {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .mode-badge {
        background: #f1f5f9;
        color: #475569;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 600;
        text-align: center;
        flex: 1;
    }
    
    .mode-badge.active {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    .camera-container {
        position: relative;
        border-radius: 16px;
        overflow: hidden;
        background: #f8fafc;
        border: 2px dashed #cbd5e1;
    }
    
    .detection-guide {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 2px solid #6366f1;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 500;
        color: #6366f1;
    }
    
    .stCameraInput > div > div::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        border: 4px solid #6366f1;
        border-radius: 12px;
        pointer-events: none;
        z-index: 10;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
        animation: pulse-border 2s ease-in-out infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    .confidence-container {
        margin: 1.5rem 0;
    }
    
    .confidence-item {
        margin-bottom: 1rem;
    }
    
    .confidence-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
        color: #334155;
    }
    
    .confidence-bar-bg {
        background: #f1f5f9;
        border-radius: 8px;
        height: 32px;
        overflow: hidden;
        position: relative;
    }
    
    .confidence-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 0.75rem;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-card {
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 2rem 0;
        animation: slideUp 0.5s ease-out;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    @keyframes slideUp {
        from {
            transform: translateY(30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .result-card.win {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .result-card.lose {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .result-card.tie {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .result-moves {
        font-size: 3rem;
        margin: 1rem 0;
        font-weight: 300;
    }
    
    .history-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        border-left: 4px solid #6366f1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s;
    }
    
    .history-item:hover {
        transform: translateX(4px);
    }
    
    .history-moves {
        font-weight: 600;
        color: #1e293b;
    }
    
    .history-result {
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .history-result.win {
        background: #d1fae5;
        color: #059669;
    }
    
    .history-result.lose {
        background: #fee2e2;
        color: #dc2626;
    }
    
    .history-result.tie {
        background: #e0e7ff;
        color: #6366f1;
    }
    
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: #f8fafc;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .streak-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        margin: 0.5rem 0;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        font-style: italic;
        font-weight: 500;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
    }
    
    .countdown {
        font-size: 6rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: scale-pulse 0.6s ease-in-out;
    }
    
    @keyframes scale-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.875rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }
    
    .gesture-icon {
        font-size: 4rem;
        margin: 1rem 0;
    }
    
    .info-text {
        color: #64748b;
        font-size: 0.875rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('CNN_model1.keras')
    return model

# Initialize session state
if 'scores' not in st.session_state:
    st.session_state.scores = {'player': 0, 'ai': 0, 'tie': 0}
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'endless'
if 'match_wins' not in st.session_state:
    st.session_state.match_wins = {'player': 0, 'ai': 0}
if 'current_streak' not in st.session_state:
    st.session_state.current_streak = {'player': 0, 'ai': 0}
if 'best_streak' not in st.session_state:
    st.session_state.best_streak = {'player': 0, 'ai': 0}
if 'ai_message' not in st.session_state:
    st.session_state.ai_message = None

# AI Messages
AI_MESSAGES = {
    'win': [
        "Nice try, but I calculated that move.",
        "My neural network is too strong!",
        "Better luck next time, human.",
        "Predicted and countered.",
        "The AI remains undefeated... for now.",
    ],
    'lose': [
        "Impressive move! Recalibrating...",
        "You got me that time. Well played.",
        "Error detected. Updating strategy.",
        "Unexpected result. Analyzing...",
        "You're learning. This could be interesting.",
    ],
    'tie': [
        "Great minds think alike.",
        "Perfectly matched. Interesting.",
        "A rare synchronization.",
        "We're evenly matched.",
        "Calculated tie. Fascinating.",
    ]
}

# Game logic
def determine_winner(player, ai):
    if player == ai:
        return "TIE"
    wins = {'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper'}
    return "PLAYER" if wins[player] == ai else "AI"

def update_streaks(winner):
    if winner == "PLAYER":
        st.session_state.current_streak['player'] += 1
        st.session_state.current_streak['ai'] = 0
        if st.session_state.current_streak['player'] > st.session_state.best_streak['player']:
            st.session_state.best_streak['player'] = st.session_state.current_streak['player']
    elif winner == "AI":
        st.session_state.current_streak['ai'] += 1
        st.session_state.current_streak['player'] = 0
        if st.session_state.current_streak['ai'] > st.session_state.best_streak['ai']:
            st.session_state.best_streak['ai'] = st.session_state.current_streak['ai']
    else:
        st.session_state.current_streak['player'] = 0
        st.session_state.current_streak['ai'] = 0

def predict_gesture(image, model):
    img = cv2.resize(image, (128, 128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    predictions = model.predict(img, verbose=0)[0]
    class_idx = np.argmax(predictions)
    confidence = predictions[class_idx] * 100
    
    class_names = ['Paper', 'Rock', 'Scissors']
    all_confidences = {class_names[i]: predictions[i] * 100 for i in range(3)}
    
    return class_names[class_idx], confidence, all_confidences

def check_match_winner():
    if st.session_state.game_mode == 'best_of_3':
        target = 2
    elif st.session_state.game_mode == 'best_of_5':
        target = 3
    else:
        return None
    
    if st.session_state.match_wins['player'] >= target:
        return 'PLAYER'
    elif st.session_state.match_wins['ai'] >= target:
        return 'AI'
    return None

# Header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Rock Paper Scissors</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Battle Arena</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Load model
try:
    model = load_model()
except Exception as e:
    st.error(f"Error Loading Model: {e}")
    st.stop()

# Game Mode Selection
col_mode1, col_mode2, col_mode3, col_mode4 = st.columns(4)

with col_mode1:
    if st.button("Endless Mode", use_container_width=True):
        st.session_state.game_mode = 'endless'
        st.session_state.match_wins = {'player': 0, 'ai': 0}
        st.rerun()

with col_mode2:
    if st.button("Best of 3", use_container_width=True):
        st.session_state.game_mode = 'best_of_3'
        st.session_state.match_wins = {'player': 0, 'ai': 0}
        st.rerun()

with col_mode3:
    if st.button("Best of 5", use_container_width=True):
        st.session_state.game_mode = 'best_of_5'
        st.session_state.match_wins = {'player': 0, 'ai': 0}
        st.rerun()

with col_mode4:
    if st.button("Reset", use_container_width=True):
        st.session_state.scores = {'player': 0, 'ai': 0, 'tie': 0}
        st.session_state.history = []
        st.session_state.last_result = None
        st.session_state.match_wins = {'player': 0, 'ai': 0}
        st.session_state.current_streak = {'player': 0, 'ai': 0}
        st.session_state.best_streak = {'player': 0, 'ai': 0}
        st.session_state.ai_message = None
        st.rerun()

# Current mode display
mode_names = {
    'endless': 'Endless Mode',
    'best_of_3': 'Best of 3',
    'best_of_5': 'Best of 5'
}
st.markdown(f'<div class="mode-badge active">{mode_names[st.session_state.game_mode]}</div>', 
            unsafe_allow_html=True)

st.markdown("---")

# Main Layout
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Scoreboard</div>', unsafe_allow_html=True)
    
    # Match score for Best of modes
    if st.session_state.game_mode != 'endless':
        st.markdown(f"""
        <div class="score-display">
            <div class="score-item">
                <div class="score-label">You</div>
                <div class="score-value">{st.session_state.match_wins['player']}</div>
            </div>
            <div class="score-item">
                <div class="score-label">AI</div>
                <div class="score-value">{st.session_state.match_wins['ai']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Total rounds
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-value">{st.session_state.scores['player']}</div>
            <div class="stat-label">Wins</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{st.session_state.scores['ai']}</div>
            <div class="stat-label">Losses</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{st.session_state.scores['tie']}</div>
            <div class="stat-label">Ties</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    total_games = sum(st.session_state.scores.values())
    if total_games > 0:
        win_rate = (st.session_state.scores['player'] / total_games) * 100
        
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-value">{win_rate:.0f}%</div>
                <div class="stat-label">Win Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_games}</div>
                <div class="stat-label">Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{st.session_state.best_streak['player']}</div>
                <div class="stat-label">Best Streak</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current streak
    if st.session_state.current_streak['player'] >= 3:
        st.markdown(f'<div class="streak-badge">On Fire: {st.session_state.current_streak["player"]} Wins</div>', 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # History
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Recent Matches</div>', unsafe_allow_html=True)
    
    if st.session_state.history:
        gesture_symbols = {'Paper': '✋', 'Rock': '✊', 'Scissors': '✌'}
        for record in reversed(st.session_state.history[-5:]):
            result_class = 'win' if record['winner'] == 'PLAYER' else ('lose' if record['winner'] == 'AI' else 'tie')
            result_text = 'Win' if record['winner'] == 'PLAYER' else ('Loss' if record['winner'] == 'AI' else 'Tie')
            
            st.markdown(f"""
            <div class="history-item">
                <div class="history-moves">{gesture_symbols[record['player']]} vs {gesture_symbols[record['ai']]}</div>
                <div class="history-result {result_class}">{result_text}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p class="info-text">No matches yet. Start playing!</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # AI Message
    if st.session_state.ai_message:
        st.markdown(f'<div class="ai-message">{st.session_state.ai_message}</div>', unsafe_allow_html=True)
    
    # Camera guide
    st.markdown('<div class="detection-guide">Position your hand inside the frame</div>', unsafe_allow_html=True)
    
    # Camera input
    camera_image = st.camera_input("Capture", label_visibility="collapsed")
    
    if camera_image is not None:
        image = Image.open(camera_image)
        img_array = np.array(image)
        
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        st.image(image, use_container_width=True)
        
        # Predict
        player_gesture, confidence, all_confidences = predict_gesture(img_array, model)
        
        st.markdown(f"<h3 style='text-align: center; color: #1e293b; margin: 1.5rem 0;'>Detected: {player_gesture}</h3>", 
                   unsafe_allow_html=True)
        
        # Confidence bars
        st.markdown('<div class="confidence-container">', unsafe_allow_html=True)
        for gesture, conf in all_confidences.items():
            st.markdown(f"""
            <div class="confidence-item">
                <div class="confidence-label">
                    <span>{gesture}</span>
                    <span>{conf:.1f}%</span>
                </div>
                <div class="confidence-bar-bg">
                    <div class="confidence-bar-fill" style="width: {conf}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Play button
        if st.button("Play Round", use_container_width=True, type="primary"):
            # Countdown
            countdown_placeholder = st.empty()
            for i in range(3, 0, -1):
                countdown_placeholder.markdown(f'<div class="countdown">{i}</div>', unsafe_allow_html=True)
                time.sleep(0.7)
            countdown_placeholder.markdown('<div class="countdown">Go!</div>', unsafe_allow_html=True)
            time.sleep(0.4)
            countdown_placeholder.empty()
            
            # AI choice
            ai_gesture = random.choice(['Paper', 'Rock', 'Scissors'])
            winner = determine_winner(player_gesture, ai_gesture)
            
            # Update scores
            if winner == "PLAYER":
                st.session_state.scores['player'] += 1
                st.session_state.match_wins['player'] += 1
                st.session_state.ai_message = random.choice(AI_MESSAGES['lose'])
            elif winner == "AI":
                st.session_state.scores['ai'] += 1
                st.session_state.match_wins['ai'] += 1
                st.session_state.ai_message = random.choice(AI_MESSAGES['win'])
            else:
                st.session_state.scores['tie'] += 1
                st.session_state.ai_message = random.choice(AI_MESSAGES['tie'])
            
            update_streaks(winner)
            
            # History
            st.session_state.history.append({
                'player': player_gesture,
                'ai': ai_gesture,
                'winner': winner,
                'confidence': confidence,
                'time': datetime.now().strftime("%H:%M")
            })
            
            st.session_state.last_result = {
                'player': player_gesture,
                'ai': ai_gesture,
                'winner': winner,
                'confidence': confidence
            }
            
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">AI Response</div>', unsafe_allow_html=True)
    
    if st.session_state.last_result:
        result = st.session_state.last_result
        gesture_symbols = {'Paper': '✋', 'Rock': '✊', 'Scissors': '✌'}
        
        st.markdown(f'<div class="gesture-icon">{gesture_symbols[result["ai"]]}</div>', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #1e293b;'>{result['ai']}</h3>", unsafe_allow_html=True)
        
        # Result
        result_class = 'win' if result['winner'] == 'PLAYER' else ('lose' if result['winner'] == 'AI' else 'tie')
        result_text = 'You Win!' if result['winner'] == 'PLAYER' else ('AI Wins' if result['winner'] == 'AI' else "It's a Tie")
        
        st.markdown(f'<div class="result-card {result_class}"><div class="result-title">{result_text}</div></div>', 
                   unsafe_allow_html=True)
        
        # Check match winner
        match_winner = check_match_winner()
        if match_winner:
            if match_winner == 'PLAYER':
                st.success("Match Won!")
                st.balloons()
            else:
                st.error("Match Lost")
            
            if st.button("New Match", use_container_width=True):
                st.session_state.match_wins = {'player': 0, 'ai': 0}
                st.session_state.last_result = None
                st.session_state.ai_message = None
                st.rerun()
    else:
        st.markdown('<p class="info-text" style="text-align: center; margin-top: 3rem;">Waiting for your move...</p>', 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; font-size: 0.875rem; padding: 2rem 0;'>
    <p>Powered by TensorFlow & Streamlit</p>
</div>
""", unsafe_allow_html=True)
