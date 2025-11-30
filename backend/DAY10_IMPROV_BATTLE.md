# Day 10: Voice Improv Battle

## Overview
A voice-first improv game show where an AI host guides players through improv scenarios. This agent acts as a charismatic host, setting the scene, listening to your performance, and providing witty feedback.

## Features

### Primary Goal (Single-Player)
- ✅ **Single-Player Mode**: Join and play solo against the AI host
- ✅ **AI Host Persona**: Witty, high-energy host who reacts realistically to your performance
- ✅ **Improv Scenarios**: 10 creative scenarios randomly selected
- ✅ **Varied Feedback**: Host provides mixed positive and critical feedback
- ✅ **Game State Management**: Tracks rounds, scenarios, and critiques
- ✅ **Early Exit**: Players can stop the game at any time

### Advanced Goal 1 (Multi-Player)
- ✅ **Room Code Support**: Players can join the same room using a shared code
- ✅ **Two-Player Relay**: Player 1 starts, Player 2 continues the story
- ✅ **Turn Management**: Host manages turn-taking between players
- ✅ **Continuity Feedback**: Host comments on how well P2 picked up from P1

### Advanced Goal 2 (Scoreboard)
- ✅ **Live Scoreboard UI**: Displays rounds, scenarios, and critiques
- ✅ **Rating Display**: Color-coded ratings (Great/Okay/Weird)
- ✅ **Round Progress**: Shows current round out of total rounds

## How to Run

### 1. Start the Backend Agent
```bash
cd backend
uv run python src/day10_agent.py dev
```

### 2. Start the Frontend
```bash
cd frontend
pnpm dev
```

### 3. Play

#### Single-Player Mode
1. Open `http://localhost:3000`
2. Enter your **Name**
3. Leave **Room Code** empty
4. Click **"Start Improv Battle"**

#### Multi-Player Mode
1. **Player 1**: Open `http://localhost:3000`
   - Enter your name
   - Enter a **Room Code** (e.g., "game123")
   - Click "Start Improv Battle"

2. **Player 2**: Open `http://localhost:3000` in another tab/browser
   - Enter your name
   - Enter the **same Room Code** (e.g., "game123")
   - Click "Start Improv Battle"

3. The host will welcome both players and explain the relay rules

## Architecture

### Backend
- **`backend/src/day10_agent.py`**: Main agent logic
  - `ImprovState`: Tracks game state, rounds, and players
  - `PlayerInfo`: Stores player identity, name, and role
  - Multi-player detection based on room name prefix
  - Dynamic system prompts for single vs multi-player modes
  - Tools: `start_round`, `advance_turn`, `evaluate_performance`, `end_game`

### Frontend
- **`frontend/components/app/welcome-view.tsx`**: Join screen with name and room code inputs
- **`frontend/components/app/scoreboard.tsx`**: Live scoreboard component
- **`frontend/hooks/useRoom.ts`**: Connection logic with room code support
- **`frontend/app/api/connection-details/route.ts`**: Token generation with room code handling

## Game Flow

### Single-Player
1. **Intro**: Host welcomes player and explains rules
2. **Round 1-3**: 
   - Host announces scenario
   - Player improvises
   - Player says "End scene" or "I'm done"
   - Host reacts with critique
3. **Summary**: Host summarizes player's improv style
4. **End**: Host thanks player and closes show

### Multi-Player
1. **Intro**: Host welcomes both players and explains relay rules
2. **Round 1-3**:
   - Host announces scenario
   - Player 1 starts the improv
   - Player 1 says "Passing it on" or similar
   - Host hands off to Player 2
   - Player 2 continues from where P1 left off
   - Host reacts to both performances and continuity
3. **Summary**: Host summarizes both players' styles
4. **End**: Host thanks both players and closes show

## Scenarios
The agent includes 10 creative improv scenarios:
- Barista with a dimensional portal latte
- Time-travelling tour guide
- Waiter with escaped food
- Customer returning a cursed object
- Cat convincing a dog to steal pizza
- Alien at a human dinner party
- Toast-making superhero
- Friendly ghost haunting
- Seasick pirate captain
- Detective vs mime suspect

## Technical Details

### Room Code System
- Room codes create shared rooms with prefix `improv_room_<code>`
- Multiple players entering the same code join the same LiveKit room
- Agent detects multi-player mode based on room name and participant count

### State Management
- Backend maintains `ImprovState` per session
- Tracks current round, phase, scenario, and player info
- Multi-player mode adds turn order and player roles

### Scoreboard Data
- Agent can send scoreboard updates via LiveKit data channel
- Frontend listens on 'scoreboard' channel
- Displays rounds, scenarios, critiques, and ratings

## Future Enhancements
- Persistent scoring across sessions
- More scenarios (or LLM-generated scenarios)
- 3+ player support
- Audience voting mode
- Video recording of performances
