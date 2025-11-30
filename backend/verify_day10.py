"""
Day 10 - Voice Improv Battle - Verification Script

This script verifies that all Day 10 components are properly implemented.
"""

import json
import os
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists and print result."""
    exists = os.path.exists(filepath)
    status = "[OK]" if exists else "[MISSING]"
    print(f"{status} {description}: {filepath}")
    return exists

def check_file_contains(filepath: str, search_text: str, description: str) -> bool:
    """Check if a file contains specific text."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            contains = search_text in content
            status = "[OK]" if contains else "[MISSING]"
            print(f"{status} {description}")
            return contains
    except Exception as e:
        print(f"[ERROR] Error reading {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("Day 10 - Voice Improv Battle - Verification")
    print("=" * 60)
    print("")

    # Check backend files
    print("Backend Files:")
    print("-" * 60)
    backend_agent = check_file_exists(
        "backend/src/day10_agent.py",
        "Main agent file"
    )
    backend_doc = check_file_exists(
        "backend/DAY10_IMPROV_BATTLE.md",
        "Backend documentation"
    )
    print("")

    # Check frontend files
    print("Frontend Files:")
    print("-" * 60)
    scoreboard = check_file_exists(
        "frontend/components/app/scoreboard.tsx",
        "Scoreboard component"
    )
    welcome_view = check_file_exists(
        "frontend/components/app/welcome-view.tsx",
        "Welcome view (modified)"
    )
    session_view = check_file_exists(
        "frontend/components/app/session-view.tsx",
        "Session view (modified)"
    )
    use_room = check_file_exists(
        "frontend/hooks/useRoom.ts",
        "useRoom hook (modified)"
    )
    connection_details = check_file_exists(
        "frontend/app/api/connection-details/route.ts",
        "Connection details API (modified)"
    )
    print("")

    # Check documentation files
    print("Documentation Files:")
    print("-" * 60)
    quick_ref = check_file_exists(
        "DAY10_QUICK_REF.md",
        "Quick reference"
    )
    summary = check_file_exists(
        "DAY10_SUMMARY.md",
        "Summary document"
    )
    getting_started = check_file_exists(
        "DAY10_GETTING_STARTED.md",
        "Getting started guide"
    )
    print("")

    # Check backend implementation details
    print("Backend Implementation:")
    print("-" * 60)
    if backend_agent:
        check_file_contains(
            "backend/src/day10_agent.py",
            "class ImprovAgent",
            "ImprovAgent class defined"
        )
        check_file_contains(
            "backend/src/day10_agent.py",
            "class ImprovState",
            "ImprovState dataclass defined"
        )
        check_file_contains(
            "backend/src/day10_agent.py",
            "SCENARIOS = [",
            "Scenarios list defined"
        )
        check_file_contains(
            "backend/src/day10_agent.py",
            "def start_round",
            "start_round tool defined"
        )
        check_file_contains(
            "backend/src/day10_agent.py",
            "def evaluate_performance",
            "evaluate_performance tool defined"
        )
        check_file_contains(
            "backend/src/day10_agent.py",
            "def advance_turn",
            "advance_turn tool defined (multi-player)"
        )
        check_file_contains(
            "backend/src/day10_agent.py",
            "is_multiplayer",
            "Multi-player mode support"
        )
    print("")

    # Check frontend implementation details
    print("Frontend Implementation:")
    print("-" * 60)
    if welcome_view:
        check_file_contains(
            "frontend/components/app/welcome-view.tsx",
            "Enter your name",
            "Name input field"
        )
        check_file_contains(
            "frontend/components/app/welcome-view.tsx",
            "Room Code",
            "Room code input field"
        )
    
    if scoreboard:
        check_file_contains(
            "frontend/components/app/scoreboard.tsx",
            "useDataChannel",
            "Data channel for scoreboard"
        )
        check_file_contains(
            "frontend/components/app/scoreboard.tsx",
            "RoundData",
            "RoundData interface"
        )
    
    if use_room:
        check_file_contains(
            "frontend/hooks/useRoom.ts",
            "roomCode",
            "Room code parameter support"
        )
    
    if connection_details:
        check_file_contains(
            "frontend/app/api/connection-details/route.ts",
            "improv_room_",
            "Room code prefix handling"
        )
    print("")

    # Summary
    print("=" * 60)
    print("Verification Complete!")
    print("=" * 60)
    print("")
    print("Next Steps:")
    print("1. Start LiveKit server: livekit-server --dev")
    print("2. Start backend: cd backend && uv run python src/day10_agent.py dev")
    print("3. Start frontend: cd frontend && pnpm dev")
    print("4. Open http://localhost:3000")
    print("")
    print("For single-player: Enter name, leave room code empty")
    print("For multi-player: Both players enter the same room code")
    print("")

if __name__ == "__main__":
    main()
