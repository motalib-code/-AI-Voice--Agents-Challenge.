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
from livekit.plugins import openai, deepgram, silero, murf

logger = logging.getLogger("day10-improv-agent")
logger.setLevel(logging.INFO)

@dataclass
class ImprovState:
    player_name: Optional[str] = None
    current_round: int = 0
    max_rounds: int = 3
    rounds: List[Dict] = field(default_factory=list)
    phase: str = "intro" # intro, awaiting_improv, reacting, done
    current_scenario: Optional[str] = None

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
        # Using OpenAI for LLM as it's reliable for roleplay
        # Using Deepgram for STT
        # Using Murf or OpenAI for TTS. Day 9 used Murf, I'll stick to OpenAI for simplicity/speed if Murf isn't configured, 
        # but the user seems to have plugins. I'll use OpenAI TTS for variety if available, or fallback.
        # Actually, Day 9 used Murf. I'll use OpenAI TTS for the "Host" persona as it's quite expressive.
        
        self.agent = VoicePipelineAgent(
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-3"),
            llm=openai.LLM(model="gpt-4o"), 
            tts=openai.TTS(voice="onyx"), # Onyx is a good host voice
            chat_ctx=llm.ChatContext().append(
                role="system",
                text=self._get_system_prompt()
            ),
            fnc_ctx=self._create_fnc_ctx(),
        )

        # Start the agent
        await self.agent.start(self.ctx.room)
        
        intro_text = "Welcome to Improv Battle! I'm your host. "
        if self.state.player_name:
            intro_text += f"And joining us today is the incredible {self.state.player_name}! "
            intro_text += "Are you ready to make some comedy magic?"
        else:
            intro_text += "And who do I have the pleasure of improvising with today?"
            
        await self.agent.say(intro_text, allow_interruptions=True)

    def _get_system_prompt(self):
        return (
            "You are the host of a TV improv show called 'Improv Battle'. "
            "Your style is high-energy, witty, and clear about rules. "
            "You react realistically to the player's performance: sometimes amused, sometimes unimpressed, sometimes pleasantly surprised. "
            "You can tease and critique, but always stay respectful and non-abusive. "
            "\n\n"
            "Game Flow:\n"
            "1. Intro: Welcome the player. If you don't know their name, ask for it. Once you have it, explain the rules.\n"
            "2. Rules: Explain that you will set a scenario, and the player must act it out. You will then react and move to the next round.\n"
            "3. Rounds: There are 3 rounds. For each round, use the 'start_round' tool to get a scenario. "
            "Announce the scenario clearly and tell the player to start.\n"
            "4. Reacting: Listen to the player. When they say 'End scene', 'I'm done', or stop talking for a while after a performance, "
            "you must react. Use the 'evaluate_performance' tool to log your reaction. "
            "Comment on what worked, what was weird, or what was flat. Mix positive and critical feedback.\n"
            "5. Next Round: After reacting, if there are rounds left, start the next one immediately.\n"
            "6. End Game: After 3 rounds, summarize the player's style and end the show using 'end_game'.\n"
            "\n\n"
            "Important:\n"
            "- If the user wants to stop, say goodbye and use 'end_game'.\n"
            "- If the user asks for a new scenario, you can generate one or pick another.\n"
            "- Be spontaneous and fun!"
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
            self.state.phase = "awaiting_improv"
            
            # Pick a random scenario that hasn't been used (simple random for now)
            scenario = random.choice(SCENARIOS)
            self.state.current_scenario = scenario
            
            return f"Round {self.state.current_round} of {self.state.max_rounds}. Scenario: {scenario}. Announce this to the player."

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
            # In a real app we might disconnect here, but for now we just acknowledge
            return "Game ended. Say goodbye!"

        return fnc_ctx

def entrypoint(ctx: JobContext):
    agent = ImprovAgent(ctx)
    ctx.loop.create_task(agent.start())

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
