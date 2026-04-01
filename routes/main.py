from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    if 'score' not in session:
        session['score'] = 0
    if 'attempts' not in session:
        session['attempts'] = 0
    if 'correct' not in session:
        session['correct'] = 0
        
    accuracy = 0
    if session['attempts'] > 0:
        accuracy = int((session['correct'] / session['attempts']) * 100)
        
    status = "STABLE" if accuracy >= 50 or session['attempts'] == 0 else "CRITICAL"
    
    return render_template('dashboard.html', 
                           score=session['score'], 
                           accuracy=accuracy, 
                           status=status)

@main_bp.route('/game/<puzzle_type>')
def game(puzzle_type):
    valid_puzzles = ['age', 'pattern', 'fruit']
    if puzzle_type not in valid_puzzles:
        return redirect(url_for('main.dashboard'))
        
    return render_template('game.html', puzzle_type=puzzle_type, score=session.get('score', 0))
