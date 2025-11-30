# Day 10 Quick Reference

## Start the Agent
```bash
cd backend
uv run python src/day10_agent.py dev
```

## Single-Player
1. Enter your name
2. Leave room code empty
3. Click "Start Improv Battle"
4. Listen to scenario
5. Improvise!
6. Say "End scene" when done
7. Listen to host's feedback
8. Repeat for 3 rounds

## Multi-Player
1. **Both players**: Enter same room code
2. **Player 1**: Starts the improv
3. **Player 1**: Say "Passing it on"
4. **Player 2**: Continue the story
5. **Host**: Reacts to both performances

## Key Commands
- "End scene" - Finish your improv
- "Passing it on" - Hand off to next player (multi-player)
- "Stop game" - Exit early
- "End show" - Exit early

## Files
- `backend/src/day10_agent.py` - Main agent
- `frontend/components/app/scoreboard.tsx` - Scoreboard UI
- `frontend/components/app/welcome-view.tsx` - Join screen
