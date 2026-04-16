from flask import Blueprint, request, jsonify, session
from utils.puzzle_logic import check_time_sync, check_sequence, check_inventory
import random

puzzles_bp = Blueprint('puzzles', __name__)

def update_session(is_correct, score_change=10):
    session['attempts'] = session.get('attempts', 0) + 1
    if is_correct:
        session['correct'] = session.get('correct', 0) + 1
        session['streak'] = session.get('streak', 0) + 1
        multiplier = 1 + (session['streak'] * 0.1)
        session['score'] = session.get('score', 0) + int(score_change * multiplier)
    else:
        session['streak'] = 0
    session.modified = True
    
def get_accuracy():
    if session.get('attempts', 0) > 0:
        return int((session.get('correct', 0) / session['attempts']) * 100)
    return 0

@puzzles_bp.route('/api/puzzle/age', methods=['GET'])
def get_age_puzzle():
    base_age = random.randint(3, 8)
    years_later = random.randint(4, 10)
    total_later = 3 * base_age + 2 * years_later
    session['current_age'] = {'base_age': base_age}
    return jsonify({
        "mission": f"Astronaut Sam is {base_age} years old. His big brother Leo is twice as old! In {years_later} years, if you add their ages, you get {total_later}. How old is Sam right now?",
        "hint": f"Try a small number for Sam's age. If Sam is 5, Leo must be 10! Then add {years_later} to both and see if it equals {total_later}."
    })

@puzzles_bp.route('/check/age', methods=['POST'])
def verify_age():
    data = request.json
    user_answer = data.get('answer', '')
    try:
        user_answer = int(user_answer)
    except ValueError:
        return jsonify({"status": "error", "message": "Oops! That's not a number! Please use numbers.", "score_update": session.get('score',0), "accuracy": get_accuracy()})
        
    correct_age = session.get('current_age', {}).get('base_age', -1)
    if user_answer == correct_age:
        update_session(True, 100)
        return jsonify({"status": "success", "message": "WHOOSH! You got it! You're a super space cadet!", "score_update": session.get('score'), "accuracy": get_accuracy()})
    else:
        update_session(False)
        return jsonify({"status": "error", "message": "Almost! Give it another try! You can do it!", "score_update": session.get('score'), "accuracy": get_accuracy()})

@puzzles_bp.route('/api/puzzle/pattern', methods=['GET'])
def get_pattern():
    start = random.randint(2, 5)
    multiplier = random.choice([2, 3])
    seq = [start * (multiplier ** i) for i in range(6)]
    missing = seq[4]
    seq_display = f"{seq[0]} -> {seq[1]} -> {seq[2]} -> {seq[3]} -> ? -> {seq[5]}"
    session['current_pattern'] = {'missing': missing, 'pattern_type': 'multiply'}
    return jsonify({
        "mission": f"Look at these numbers hopping along the magic train: {seq_display}. What's the mystery number under the question mark?",
        "hint": f"Look at {seq[0]} and {seq[1]}. Did we add something or multiply by {multiplier}? Keep following that rule!"
    })

@puzzles_bp.route('/check/pattern', methods=['POST'])
def verify_pattern():
    data = request.json
    pattern_type = data.get('pattern_type')
    missing_val = data.get('missing_value')
    current = session.get('current_pattern', {})
    
    try:
        missing_val = int(missing_val)
    except ValueError:
        return jsonify({"status": "error", "message": "That's not a number! Use your number keys!", "score_update": session.get('score',0), "accuracy": get_accuracy()})
        
    if pattern_type == current.get('pattern_type') and missing_val == current.get('missing'):
        update_session(True, 150)
        return jsonify({"status": "success", "message": "MAGIC! You solved the pattern! You're so smart!", "score_update": session.get('score'), "accuracy": get_accuracy()})
    else:
        update_session(False)
        return jsonify({"status": "error", "message": "Nearly! Peek at the numbers again and see if you can spot the rule!", "score_update": session.get('score'), "accuracy": get_accuracy()})

@puzzles_bp.route('/api/puzzle/fruit', methods=['GET'])
def get_fruit():
    total = random.randint(15, 30)
    apples = random.randint(5, total - 5)
    oranges = total - apples
    session['current_fruit'] = {'oranges': oranges}
    return jsonify({
        "mission": f"We have {total} space snacks in a big box. If {apples} of them are red apples, how many oranges are left for the astronauts?",
        "hint": f"If you take away {apples} from {total}, what's left over? That's your answer!"
    })

@puzzles_bp.route('/check/fruit', methods=['POST'])
def verify_fruit():
    data = request.json
    answer = data.get('answer')
    time_taken = data.get('time_taken', 10)
    try:
        answer = int(answer)
    except ValueError:
        return jsonify({"status": "error", "message": "Oops! Please type a number for the fruits!", "score_update": session.get('score',0), "accuracy": get_accuracy()})
        
    correct_val = session.get('current_fruit', {}).get('oranges', -1)
    if answer == correct_val:
        score = 50 + max(0, int(50 - time_taken*2))
        update_session(True, score)
        return jsonify({"status": "success", "message": "KABOOM! You're a counting expert! Let's launch!", "score_update": session.get('score'), "accuracy": get_accuracy()})
    else:
        update_session(False)
        return jsonify({"status": "error", "message": "So close! Try counting one more time!", "score_update": session.get('score'), "accuracy": get_accuracy()})
