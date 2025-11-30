import logging
import random
from typing import Annotated, List, Dict, Any, Optional
from dataclasses import dataclass, field
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, deepgram, silero
from livekit import rtc

logger = logging.getLogger("day10-improv-agent")
logger.setLevel(logging.INFO)

@dataclass
class PlayerInfo:
    identity: str
    name: str
    role: str  # "P1" or "P2"

@dataclass
class ImprovState:
    player_name: Optional[str] = None
    current_round: int = 0
    max_rounds: int = 3
    rounds: List[Dict] = field(default_factory=list)
    phase: str = "intro"  # intro, awaiting_improv, reacting, done, P1_improv, P2_improv, host_react
    current_scenario: Optional[str] = None
    
    # Multi-player fields
    is_multiplayer: bool = False
    players: Dict[str, PlayerInfo] = field(default_factory=dict)  # identity -> PlayerInfo
    turn_order: List[str] = field(default_factory=list)  # list of identities
    current_player_index: int = 0

SCENARIOS = [
    "You are a barista who has to tell a customer that their latte is actually a portal to another dimension.",
    "You are a time-travelling tour guide explaining modern smartphones to someone from the 1800s.",
    "You are a restaurant waiter who must calmly tell a customer that their order has escaped the kitchen.",
    "You are a customer trying to return an obviously cursed object to a very skeptical shop owner.",
    "You are a cat trying to convince a dog to help you steal a pizza from the counter.",
    "You are an alien trying to blend in at a human dinner party but you don't understand how forks work.",
    "You are a superhero whose only power is making toast appear, trying to stop a bank robbery.",
    "You are a ghost trying to haunt a house, but the new owners are really into it and think you're cool.",
    "You are a pirate captain who gets seasick very easily, trying to give a motivational speech.",
    "You are a detective interrogating a suspect who is a mime and refuses to break character."
]

class ImprovAgent:
    def __init__(self, ctx: JobContext):
        self.ctx = ctx
        self.agent = None
        self.state = ImprovState()
        
        # Try to get player name from metadata
        if ctx.job.metadata:
            try:
                import json
                meta = json.loads(ctx.job.metadata)
                if "participantName" in meta:
                    self.state.player_name = meta["participantName"]
            except:
                pass

    async def start(self):
        # Initialize the agent
        self.agent = VoicePipelineAgent(
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-3"),
            llm=openai.LLM(model="gpt-4o"), 
            tts=openai.TTS(voice="onyx"),
            chat_ctx=llm.ChatContext().append(
                role="system",
                text=self._get_system_prompt()
            ),
            fnc_ctx=self._create_fnc_ctx(),
        )

        # Start the agent
        await self.agent.start(self.ctx.room)
        
        # Set up participant tracking for multi-player
        self.ctx.room.on("participant_connected", self._on_participant_connected)
        
        # Check for existing participants
        await self._check_participants()
        
        # Determine if multi-player based on room name
        room_name = self.ctx.room.name or ""
        if room_name.startswith("improv_room_"):
            logger.info(f"Multi-player room detected: {room_name}")
            # Wait a moment for second player to potentially join
            import asyncio
            await asyncio.sleep(2)
            await self._check_participants()
        
        # Generate intro
        intro_text = await self._generate_intro()
        await self.agent.say(intro_text, allow_interruptions=True)

    async def _check_participants(self):
        """Check and register participants"""
        for participant in self.ctx.room.remote_participants.values():
            await self._register_participant(participant)

    async def _on_participant_connected(self, participant: rtc.RemoteParticipant):
        """Handle new participant joining"""
        logger.info(f"Participant connected: {participant.identity}")
        await self._register_participant(participant)

    async def _register_participant(self, participant: rtc.RemoteParticipant):
        """Register a participant in the game state"""
        if participant.identity in self.state.players:
            return
        
        # Get participant name
        name = participant.name or "Player"
        if participant.metadata:
            try:
                import json
                meta = json.loads(participant.metadata)
                if "participantName" in meta:
                    name = meta["participantName"]
            except:
                pass
        
        # Assign role
        role = f"P{len(self.state.players) + 1}"
        
        player_info = PlayerInfo(
            identity=participant.identity,
            name=name,
            role=role
        )
        
        self.state.players[participant.identity] = player_info
        self.state.turn_order.append(participant.identity)
        
        # Set single player name for backward compatibility
        if not self.state.player_name:
            self.state.player_name = name
        
        # Enable multi-player if we have 2+ players
        if len(self.state.players) >= 2:
            self.state.is_multiplayer = True
            logger.info(f"Multi-player mode activated with {len(self.state.players)} players")

    async def _generate_intro(self) -> str:
        """Generate introduction based on player count"""
        if self.state.is_multiplayer and len(self.state.players) >= 2:
            player_names = [p.name for p in self.state.players.values()]
            return (
                f"Welcome to Improv Battle! I'm your host. "
                f"And we have TWO incredible contestants today: {player_names[0]} and {player_names[1]}! "
                f"This is going to be a relay improv showdown. Are you both ready?"
            )
        elif self.state.player_name:
            return (
                f"Welcome to Improv Battle! I'm your host. "
                f"And joining us today is the incredible {self.state.player_name}! "
                f"Are you ready to make some comedy magic?"
            )
        else:
            return "Welcome to Improv Battle! I'm your host. And who do I have the pleasure of improvising with today?"

    def _get_system_prompt(self):
        base_prompt = (
            "You are the host of a TV improv show called 'Improv Battle'. "
            "Your style is high-energy, witty, and clear about rules. "
            "You react realistically to the player's performance: sometimes amused, sometimes unimpressed, sometimes pleasantly surprised. "
            "You can tease and critique, but always stay respectful and non-abusive. "
            "\n\n"
        )
        
        if self.state.is_multiplayer:
            return base_prompt + (
                "MULTI-PLAYER MODE:\n"
                "1. Intro: Welcome both players and explain the relay rules.\n"
                "2. Rules: Player 1 starts the improv scene. Player 2 must continue from where P1 left off.\n"
                "3. Rounds: There are 3 rounds. For each round, use 'start_round' to get a scenario.\n"
                "4. Turn Management: Use 'advance_turn' to switch between players.\n"
                "5. Reacting: After both players perform, use 'evaluate_performance' to critique.\n"
                "   - Comment on continuity, creativity, and how well P2 picked up from P1.\n"
                "6. End Game: After 3 rounds, summarize both players' styles.\n"
                "\n"
                "Important:\n"
                "- Only the current player should speak during their turn.\n"
                "- If the wrong player speaks, gently redirect them.\n"
                "- Be spontaneous and fun!\n"
            )
        else:
            return base_prompt + (
                "SINGLE-PLAYER MODE:\n"
                "1. Intro: Welcome the player. If you don't know their name, ask for it. Once you have it, explain the rules.\n"
                "2. Rules: Explain that you will set a scenario, and the player must act it out. You will then react and move to the next round.\n"
                "3. Rounds: There are 3 rounds. For each round, use the 'start_round' tool to get a scenario. "
                "Announce the scenario clearly and tell the player to start.\n"
                "4. Reacting: Listen to the player. When they say 'End scene', 'I'm done', or stop talking for a while after a performance, "
                "you must react. Use the 'evaluate_performance' tool to log your reaction. "
                "Comment on what worked, what was weird, or what was flat. Mix positive and critical feedback.\n"
                "5. Next Round: After reacting, if there are rounds left, start the next one immediately.\n"
                "6. End Game: After 3 rounds, summarize the player's style and end the show using 'end_game'.\n"
                "\n"
                "Important:\n"
                "- If the user wants to stop, say goodbye and use 'end_game'.\n"
                "- If the user asks for a new scenario, you can generate one or pick another.\n"
                "- Be spontaneous and fun!\n"
            )

    def _create_fnc_ctx(self):
        fnc_ctx = llm.FunctionContext()

        @fnc_ctx.ai_callable(description="Set the player's name if not already set")
        def set_player_name(name: Annotated[str, llm.TypeInfo(description="The name of the player")]) -> str:
            self.state.player_name = name
            return f"Player name set to {name}. You can now proceed to explain the rules and start the game."

        @fnc_ctx.ai_callable(description="Start a new improv round with a scenario")
        def start_round() -> str:
            if self.state.current_round >= self.state.max_rounds:
                return "The game is already over. Please summarize and end the game."
            
            self.state.current_round += 1
            
            # Set phase based on mode
            if self.state.is_multiplayer:
                self.state.phase = "P1_improv"
                self.state.current_player_index = 0
            else:
                self.state.phase = "awaiting_improv"
            
            # Pick a random scenario
            scenario = random.choice(SCENARIOS)
            self.state.current_scenario = scenario
            
            if self.state.is_multiplayer:
                p1_name = self.state.players[self.state.turn_order[0]].name if self.state.turn_order else "Player 1"
                return f"Round {self.state.current_round} of {self.state.max_rounds}. Scenario: {scenario}. Tell {p1_name} to start the scene."
            else:
                return f"Round {self.state.current_round} of {self.state.max_rounds}. Scenario: {scenario}. Announce this to the player."

        @fnc_ctx.ai_callable(description="Advance to the next player's turn (multi-player only)")
        def advance_turn() -> str:
            if not self.state.is_multiplayer:
                return "This is single-player mode. No turn advancement needed."
            
            self.state.current_player_index += 1
            
            if self.state.current_player_index >= len(self.state.turn_order):
                # All players have gone, move to reaction
                self.state.phase = "host_react"
                return "All players have performed. Time to react and critique."
            
            # Move to next player
            self.state.phase = f"P{self.state.current_player_index + 1}_improv"
            next_player = self.state.players[self.state.turn_order[self.state.current_player_index]]
            return f"Now it's {next_player.name}'s turn. Tell them to continue the scene from where the previous player left off."

        @fnc_ctx.ai_callable(description="Evaluate the player's performance for the current round")
        def evaluate_performance(
            critique: Annotated[str, llm.TypeInfo(description="Your critique of the performance")],
            rating: Annotated[str, llm.TypeInfo(description="Short rating like 'Great', 'Okay', 'Weird'")]
        ) -> str:
            self.state.rounds.append({
                "round": self.state.current_round,
                "scenario": self.state.current_scenario,
                "critique": critique,
                "rating": rating
            })
            self.state.phase = "reacting"
            
            remaining = self.state.max_rounds - self.state.current_round
            if remaining > 0:
                return f"Reaction recorded. You have {remaining} rounds left. Proceed to the next round."
            else:
                return "Reaction recorded. That was the final round. Please summarize the player's overall performance and end the show."

        @fnc_ctx.ai_callable(description="End the game show")
        def end_game() -> str:
            self.state.phase = "done"
            return "Game ended. Say goodbye!"

        return fnc_ctx

def entrypoint(ctx: JobContext):
    agent = ImprovAgent(ctx)
    ctx.loop.create_task(agent.start())

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
