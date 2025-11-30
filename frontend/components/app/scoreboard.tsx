'use client';

import { useEffect, useState } from 'react';
import { useDataChannel } from '@livekit/components-react';

interface RoundData {
    round: number;
    scenario: string;
    critique: string;
    rating: string;
}

interface ScoreboardData {
    playerName?: string;
    currentRound: number;
    maxRounds: number;
    rounds: RoundData[];
    phase: string;
}

export function Scoreboard() {
    const [scoreboardData, setScoreboardData] = useState<ScoreboardData>({
        currentRound: 0,
        maxRounds: 3,
        rounds: [],
        phase: 'intro',
    });

    // Listen for data messages from the agent
    const { message } = useDataChannel('scoreboard');

    useEffect(() => {
        if (message && message.payload) {
            try {
                const data = JSON.parse(new TextDecoder().decode(message.payload));
                setScoreboardData(data);
            } catch (error) {
                console.error('Failed to parse scoreboard data:', error);
            }
        }
    }, [message]);

    if (scoreboardData.rounds.length === 0) {
        return null;
    }

    return (
        <div className="fixed top-4 right-4 w-80 rounded-lg border border-border bg-background/95 p-4 shadow-lg backdrop-blur">
            <h2 className="mb-3 text-lg font-bold">Improv Battle</h2>

            {scoreboardData.playerName && (
                <p className="mb-2 text-sm text-muted-foreground">
                    Player: <span className="font-medium text-foreground">{scoreboardData.playerName}</span>
                </p>
            )}

            <p className="mb-4 text-sm text-muted-foreground">
                Round: {scoreboardData.currentRound} / {scoreboardData.maxRounds}
            </p>

            <div className="space-y-3">
                {scoreboardData.rounds.map((round, index) => (
                    <div
                        key={index}
                        className="rounded-md border border-border/50 bg-muted/30 p-3"
                    >
                        <div className="mb-1 flex items-center justify-between">
                            <span className="text-xs font-semibold">Round {round.round}</span>
                            <span
                                className={`rounded-full px-2 py-0.5 text-xs font-medium ${round.rating.toLowerCase().includes('great')
                                        ? 'bg-green-500/20 text-green-700 dark:text-green-300'
                                        : round.rating.toLowerCase().includes('okay')
                                            ? 'bg-yellow-500/20 text-yellow-700 dark:text-yellow-300'
                                            : 'bg-blue-500/20 text-blue-700 dark:text-blue-300'
                                    }`}
                            >
                                {round.rating}
                            </span>
                        </div>
                        <p className="mb-1 text-xs text-muted-foreground line-clamp-2">
                            {round.scenario}
                        </p>
                        <p className="text-xs italic text-foreground/80 line-clamp-2">
                            "{round.critique}"
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
