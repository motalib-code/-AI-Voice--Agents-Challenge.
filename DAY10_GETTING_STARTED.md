# Day 10 Getting Started: Voice Improv Battle

## Overview
Build a voice-first improv game show where an AI host guides players through improv scenarios. Supports both single-player and multi-player relay modes.

## Prerequisites
- LiveKit server running (`livekit-server --dev`)
- Backend dependencies installed (`uv sync`)
- Frontend dependencies installed (`pnpm install`)
- OpenAI API key configured

## Quick Start

### 1. Start LiveKit Server
```bash
livekit-server --dev
```

### 2. Start the Backend Agent
```bash
cd backend
uv run python src/day10_agent.py dev
```

### 3. Start the Frontend
```bash
cd frontend
pnpm dev
```

### 4. Open Browser
Navigate to `http://localhost:3000`

## Single-Player Mode

### How to Play
1. **Enter Your Name**: Type your name in the input field
2. **Leave Room Code Empty**: Don't enter a room code
3. **Click "Start Improv Battle"**: Connect to the AI host
4. **Listen**: The host will welcome you and explain the rules
5. **Improvise**: When the host gives you a scenario, act it out!
6. **End Scene**: Say "End scene" or "I'm done" when finished
7. **Get Feedback**: Listen to the host's critique
8. **Repeat**: Play through 3 rounds
9. **Summary**: Hear the host's final thoughts on your style

### Example Interaction
```
Host: "Welcome to Improv Battle! I'm your host. And joining us today 
       is the incredible Alex! Are you ready to make some comedy magic?"

You: "Yes! Let's do this!"

Host: "Fantastic! Here's how it works... [explains rules]
       Round 1 of 3. You are a barista who has to tell a customer 
       that their latte is actually a portal to another dimension. 
       Action!"

You: [Improvises the scene]
     "So, um, about your latte... it's not just coffee. It's actually 
      a gateway to the shadow realm. But the good news is, it's still 
      only $4.50!"

You: "End scene"

Host: "Ha! I loved the commitment to the price point. That was 
       hilarious! The deadpan delivery really sold it. Great start!"
```

## Multi-Player Mode

### How to Play
1. **Player 1**:
   - Enter your name
   - Enter a room code (e.g., "game123")
   - Click "Start Improv Battle"
   - Wait for Player 2

2. **Player 2**:
   - Open `http://localhost:3000` in another tab/browser
   - Enter your name
   - Enter the **same room code** (e.g., "game123")
   - Click "Start Improv Battle"

3. **Game Flow**:
   - Host welcomes both players
   - Host explains relay rules
   - Player 1 starts the improv
   - Player 1 says "Passing it on" (or similar)
   - Host hands off to Player 2
   - Player 2 continues the story
   - Host reacts to both performances
   - Repeat for 3 rounds

### Example Multi-Player Interaction
```
Host: "Welcome to Improv Battle! I'm your host. And we have TWO 
       incredible contestants today: Alex and Jordan! This is going 
       to be a relay improv showdown. Are you both ready?"

Alex & Jordan: "Yes!"

Host: "Here's how the relay works... [explains rules]
       Round 1 of 3. You are a time-travelling tour guide explaining 
       modern smartphones to someone from the 1800s. Alex, you start!"

Alex: [Starts improv]
      "Good day, sir! Welcome to the year 2024. This magical device 
       is called a 'smartphone.' It's like a telegraph, but you can 
       also use it to look at pictures of cats."
      [Pauses] "Passing it on!"

Host: "Excellent setup! Now Jordan, pick it up from that last line 
       and keep the story going."

Jordan: [Continues]
        "Cats, you say? Fascinating! And how does one operate this 
         contraption? Do you feed it coal like a steam engine?"

Host: "Brilliant! Jordan, you picked up perfectly on Alex's cat 
       reference. Great continuity! And I love the steam engine 
       comparison. Well done, both of you!"
```

## Tips for Great Improv

### Do:
- **Commit to the character**: Fully embrace the role
- **Yes, and...**: Build on what's been established
- **Be specific**: Details make scenes funnier
- **Have fun**: The host appreciates enthusiasm
- **Listen**: Pay attention to the scenario and feedback

### Don't:
- **Block**: Don't deny what's been established
- **Overthink**: Go with your first instinct
- **Rush**: Take your time with the scene
- **Break character**: Stay in the moment

## Scenarios You Might Get
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

## Understanding the Scoreboard

The scoreboard appears in the top-right corner and shows:
- **Player Name**: Your name
- **Round Progress**: Current round / Total rounds (e.g., 2 / 3)
- **Past Rounds**: Each completed round with:
  - Round number
  - Scenario
  - Host's critique
  - Rating (color-coded: Green = Great, Yellow = Okay, Blue = Other)

## Troubleshooting

### "No audio"
- Check microphone permissions in browser
- Ensure LiveKit server is running
- Check browser console for errors

### "Can't connect"
- Verify backend agent is running
- Check that frontend is running on port 3000
- Ensure LiveKit server is running on default port

### "Room code not working"
- Make sure both players enter the **exact same code**
- Codes are case-sensitive
- Try a different code if issues persist

### "Host not responding"
- Check backend logs for errors
- Verify OpenAI API key is configured
- Try saying "Hello" to trigger a response

## Advanced: Customization

### Add More Scenarios
Edit `backend/src/day10_agent.py`:
```python
SCENARIOS = [
    "Your custom scenario here...",
    # Add more scenarios
]
```

### Change Number of Rounds
Edit `backend/src/day10_agent.py`:
```python
@dataclass
class ImprovState:
    max_rounds: int = 5  # Change from 3 to 5
```

### Customize Host Voice
Edit `backend/src/day10_agent.py`:
```python
tts=openai.TTS(voice="nova"),  # Try: alloy, echo, fable, onyx, nova, shimmer
```

## Next Steps
- Try both single-player and multi-player modes
- Experiment with different scenarios
- Invite friends to play multi-player
- Check out the full documentation in `backend/DAY10_IMPROV_BATTLE.md`

## Resources
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [OpenAI TTS Voices](https://platform.openai.com/docs/guides/text-to-speech)
- [Improv Comedy Basics](https://en.wikipedia.org/wiki/Improvisational_theatre)

Have fun improvising! 🎭
