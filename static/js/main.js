document.addEventListener('DOMContentLoaded', () => {
    const puzzleType = document.body.dataset.puzzle;
    if (!puzzleType) return;

    const missionText = document.getElementById('mission-text');
    const hintText = document.getElementById('hint-text');
    const hintContainer = document.getElementById('hint-container');
    const hintBtn = document.getElementById('hint-btn');
    const interactionZone = document.getElementById('interaction-zone');
    const feedbackPanel = document.getElementById('feedback-panel');
    const feedbackText = document.getElementById('feedback-text');
    const gameScore = document.getElementById('game-score');
    const gameTimer = document.getElementById('game-timer');

    let startTime = Date.now();
    let timerID = null;

    // Start timer
    timerID = setInterval(() => {
        const elapsed = (Date.now() - startTime) / 1000;
        gameTimer.innerText = elapsed.toFixed(1);
    }, 100);

    // Initial load
    fetch(`/api/puzzle/${puzzleType}`)
        .then(res => res.json())
        .then(data => {
            missionText.innerText = data.mission;
            if (data.hint) {
                hintText.innerText = data.hint;
            }
            renderInputFields(puzzleType);
        })
        .catch(err => {
            console.error("Link broken:", err);
            missionText.innerText = "Oh no! Something went wrong! Try again!";
        });

    // Handle Hint button
    if (hintBtn) {
        hintBtn.addEventListener('click', () => {
            hintContainer.classList.remove('hidden');
            hintBtn.classList.add('hidden');
        });
    }

    function renderInputFields(type) {
        if (type === 'age' || type === 'fruit') {
            interactionZone.innerHTML = `
                <div class="input-group">
                    <label class="input-label">>>> TYPE YOUR ANSWER</label>
                    <input type="number" id="user-input" class="terminal-input" autofocus autocomplete="off">
                </div>
                <button id="submit-btn" class="btn">CHECK IT!</button>
            `;
            
            document.getElementById('submit-btn').addEventListener('click', () => {
                const val = document.getElementById('user-input').value;
                submitAnswer(type, { 
                    answer: val, 
                    time_taken: (Date.now() - startTime) / 1000 
                });
            });

            document.getElementById('user-input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') document.getElementById('submit-btn').click();
            });
        } else if (type === 'pattern') {
            interactionZone.innerHTML = `
                <div class="input-group">
                    <label class="input-label">>>> IS THE RULE...</label>
                    <div class="radio-group">
                        <label class="radio-item"><input type="radio" name="pattern-type" value="multiply" checked> TIMES (X)</label>
                        <label class="radio-item"><input type="radio" name="pattern-type" value="add"> PLUS (+)</label>
                    </div>
                </div>
                <div class="input-group">
                    <label class="input-label">>>> MISSING NUMBER</label>
                    <input type="number" id="user-val" class="terminal-input" autocomplete="off">
                </div>
                <button id="submit-btn" class="btn">GUESS!</button>
            `;

            document.getElementById('submit-btn').addEventListener('click', () => {
                const op = document.querySelector('input[name="pattern-type"]:checked').value;
                const val = document.getElementById('user-val').value;
                submitAnswer(type, { 
                    pattern_type: op, 
                    missing_value: val,
                    time_taken: (Date.now() - startTime) / 1000
                });
            });
        }
    }

    function submitAnswer(type, payload) {
        const btn = document.getElementById('submit-btn');
        btn.disabled = true;
        btn.innerText = "WAIT A SEC...";

        fetch(`/check/${type}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            clearInterval(timerID);
            
            feedbackPanel.classList.remove('hidden', 'feedback-success', 'feedback-error');
            feedbackText.innerText = data.message;
            feedbackPanel.classList.add(data.status === 'success' ? 'feedback-success' : 'feedback-error');
            
            if (gameScore) gameScore.innerText = data.score_update;

            setTimeout(() => {
                interactionZone.innerHTML = `
                    <div class="button-group" style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem;">
                        <button class="btn" onclick="window.location.reload()">GO AGAIN!</button> 
                        <a href="/" class="btn btn-outline" style="background: rgba(255,255,255,0.2); border-radius: 50px; font-family: var(--font-title); text-decoration: none; padding: 1rem 2rem; color: white;">HOME</a>
                    </div>
                `;
            }, 500);
        })
        .catch(err => {
            console.error("Error:", err);
            feedbackPanel.classList.remove('hidden');
            feedbackPanel.classList.add('feedback-error');
            feedbackText.innerText = "Oh man! The computer had a hiccup! Please try again!";
            btn.disabled = false;
            btn.innerText = "TRY AGAIN!";
        });
    }
});
