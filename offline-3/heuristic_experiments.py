#!/usr/bin/env python3
"""
Chain Reaction Heuristic Experiments
====================================

This script performs comprehensive experiments to evaluate different heuristics
at various depths in Chain Reaction game.

Experiments:
1. Each heuristic vs Random AI at depths 2, 3, 4
2. All heuristics vs each other at depths 2, 3, 4
3. Performance metrics: win rates, average move times, game statistics

Grid: 5x5
Time limit: 10 seconds per move
"""

import time
import random
import statistics
import csv
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from chainReactionEngine import (
    ChainReactionGame, MinimaxAI, RandomAI, Player, ChainReactionHeuristics
)

@dataclass
class GameResult:
    """Store results of a single game"""
    winner: Optional[Player]
    total_moves: int
    game_duration: float
    red_avg_move_time: float
    blue_avg_move_time: float
    red_ai_name: str
    blue_ai_name: str
    red_depth: int
    blue_depth: int

@dataclass
class ExperimentStats:
    """Store aggregated experiment statistics"""
    games_played: int
    wins: int
    losses: int
    draws: int
    avg_move_time: float
    avg_game_duration: float
    avg_moves_per_game: float
    win_rate: float

class HeuristicExperiment:
    def __init__(self, grid_size: int = 5, time_limit: float = 10.0, verbose: bool = True):
        self.grid_size = grid_size
        self.time_limit = time_limit
        self.verbose = verbose
        
        # Available heuristics
        self.heuristics = {
            "Orb Count": ChainReactionHeuristics.orb_count_heuristic,
            "Explosion Potential": ChainReactionHeuristics.explosion_potential_heuristic,
            "Strategic Evaluation": ChainReactionHeuristics.strategic_eval_heuristic,
            "Threat Analysis": ChainReactionHeuristics.threat_analysis_heuristic,
            "Tempo": ChainReactionHeuristics.tempo_heuristic,
            "Combined Strategy": ChainReactionHeuristics.strat_eval_expl_potential_combined_heuristic
        }
        
        self.depths = [2, 3, 4]
        self.results: List[GameResult] = []
        
        # Detailed performance tracking for CSV export
        self.heuristic_depth_stats = defaultdict(lambda: defaultdict(list))  # [heuristic][depth] = [move_times]
        self.heuristic_depth_moves = defaultdict(lambda: defaultdict(list))  # [heuristic][depth] = [move_counts]
        self.heuristic_depth_wins = defaultdict(lambda: defaultdict(int))    # [heuristic][depth] = win_count
        self.heuristic_depth_games = defaultdict(lambda: defaultdict(int))   # [heuristic][depth] = total_games
        
    def create_ai(self, player: Player, ai_type: str, depth: int = 0, heuristic_name: str = None) -> tuple:
        """Create AI instance based on type"""
        if ai_type == "Random":
            return RandomAI(player), "Random", 0
        elif ai_type == "Smart":
            heuristic_func = self.heuristics[heuristic_name]
            ai = MinimaxAI(player, depth=depth, heuristic_func=heuristic_func)
            ai.max_search_time = self.time_limit
            return ai, f"{heuristic_name} (D{depth})", depth
        else:
            raise ValueError(f"Unknown AI type: {ai_type}")
    
    def play_single_game(self, red_config: tuple, blue_config: tuple, game_id: int = 0) -> GameResult:
        """Play a single game between two AIs"""
        red_ai, red_name, red_depth = red_config
        blue_ai, blue_name, blue_depth = blue_config
        
        if self.verbose:
            print(f"\n🎮 Game {game_id}: {red_name} vs {blue_name}")
        
        game = ChainReactionGame(self.grid_size, self.grid_size)
        start_time = time.time()
        
        red_move_times = []
        blue_move_times = []
        move_count = 0
        max_moves = 1000  # Prevent infinite games
        
        while not game.game_over and move_count < max_moves:
            current_player = game.current_player
            move_start = time.time()
            
            if current_player == Player.RED:
                move = red_ai.get_best_move(game)
                ai_name = red_name
            else:
                move = blue_ai.get_best_move(game)
                ai_name = blue_name
            
            move_time = time.time() - move_start
            
            if move is None:
                if self.verbose:
                    print(f"❌ {ai_name} could not find a valid move!")
                break
                
            if not game.make_move(move[0], move[1], current_player):
                if self.verbose:
                    print(f"❌ Invalid move by {ai_name}: {move}")
                break
            
            # Record move time
            if current_player == Player.RED:
                red_move_times.append(move_time)
            else:
                blue_move_times.append(move_time)
            
            move_count += 1
            
            if self.verbose and move_count % 10 == 0:
                scores = game.get_score()
                print(f"   Move {move_count}: Red {scores[Player.RED]} - Blue {scores[Player.BLUE]}")
        
        game_duration = time.time() - start_time
        
        # Calculate average move times
        red_avg_time = statistics.mean(red_move_times) if red_move_times else 0.0
        blue_avg_time = statistics.mean(blue_move_times) if blue_move_times else 0.0
        
        result = GameResult(
            winner=game.winner,
            total_moves=move_count,
            game_duration=game_duration,
            red_avg_move_time=red_avg_time,
            blue_avg_move_time=blue_avg_time,
            red_ai_name=red_name,
            blue_ai_name=blue_name,
            red_depth=red_depth,
            blue_depth=blue_depth
        )
        
        if self.verbose:
            winner_name = game.winner.value if game.winner else "Draw"
            final_scores = game.get_score()
            print(f"🏆 Winner: {winner_name}")
            print(f"📊 Final Score: Red {final_scores[Player.RED]} - Blue {final_scores[Player.BLUE]}")
            print(f"⏱️  Game Duration: {game_duration:.2f}s, Moves: {move_count}")
            print(f"🕐 Avg Move Time: Red {red_avg_time:.3f}s, Blue {blue_avg_time:.3f}s")
        
        return result
    
    def run_heuristic_vs_random_experiments(self, games_per_config: int = 5):
        """Run experiments: Each heuristic vs Random AI at different depths"""
        print("\n" + "=" * 60)
        print("🧪 EXPERIMENT 1: Heuristics vs Random AI")
        print("=" * 60)
        
        experiment_results = {}
        
        for heuristic_name in self.heuristics.keys():
            for depth in self.depths:
                print(f"\n🔬 Testing {heuristic_name} at depth {depth} vs Random AI")
                print("-" * 50)
                
                games_results = []
                
                for game_num in range(games_per_config):
                    # Alternate who plays first
                    if game_num % 2 == 0:
                        red_config = self.create_ai(Player.RED, "Smart", depth, heuristic_name)
                        blue_config = self.create_ai(Player.BLUE, "Random")
                    else:
                        red_config = self.create_ai(Player.RED, "Random")
                        blue_config = self.create_ai(Player.BLUE, "Smart", depth, heuristic_name)
                    
                    result = self.play_single_game(red_config, blue_config, game_num + 1)
                    games_results.append(result)
                    self.results.append(result)
                
                # Calculate stats for this configuration
                smart_wins = 0
                smart_move_times = []
                
                for result in games_results:
                    # Determine if smart AI won
                    smart_player = Player.RED if heuristic_name in result.red_ai_name else Player.BLUE
                    if result.winner == smart_player:
                        smart_wins += 1
                    
                    # Collect smart AI move times
                    if smart_player == Player.RED:
                        smart_move_times.append(result.red_avg_move_time)
                    else:
                        smart_move_times.append(result.blue_avg_move_time)
                
                avg_move_time = statistics.mean(smart_move_times) if smart_move_times else 0.0
                win_rate = smart_wins / games_per_config * 100
                
                config_key = f"{heuristic_name}_D{depth}_vs_Random"
                experiment_results[config_key] = ExperimentStats(
                    games_played=games_per_config,
                    wins=smart_wins,
                    losses=games_per_config - smart_wins,
                    draws=0,
                    avg_move_time=avg_move_time,
                    avg_game_duration=statistics.mean([r.game_duration for r in games_results]),
                    avg_moves_per_game=statistics.mean([r.total_moves for r in games_results]),
                    win_rate=win_rate                )
                
                print(f"📈 Results: {smart_wins}/{games_per_config} wins ({win_rate:.1f}%)")
                print(f"⏱️  Average move time: {avg_move_time:.3f}s")
        
        return experiment_results
    
    def _update_heuristic_stats(self, result: GameResult, heuristic1: str, depth1: int, heuristic2: str, depth2: int):
        """Update detailed statistics for CSV export"""
        # Update stats for heuristic1
        if heuristic1 in result.red_ai_name and result.red_depth == depth1:
            self.heuristic_depth_stats[heuristic1][depth1].append(result.red_avg_move_time)
            self.heuristic_depth_moves[heuristic1][depth1].append(result.total_moves)
            self.heuristic_depth_games[heuristic1][depth1] += 1
            if result.winner == Player.RED:
                self.heuristic_depth_wins[heuristic1][depth1] += 1
        elif heuristic1 in result.blue_ai_name and result.blue_depth == depth1:
            self.heuristic_depth_stats[heuristic1][depth1].append(result.blue_avg_move_time)
            self.heuristic_depth_moves[heuristic1][depth1].append(result.total_moves)
            self.heuristic_depth_games[heuristic1][depth1] += 1
            if result.winner == Player.BLUE:
                self.heuristic_depth_wins[heuristic1][depth1] += 1
        
        # Update stats for heuristic2
        if heuristic2 in result.red_ai_name and result.red_depth == depth2:
            self.heuristic_depth_stats[heuristic2][depth2].append(result.red_avg_move_time)
            self.heuristic_depth_moves[heuristic2][depth2].append(result.total_moves)
            self.heuristic_depth_games[heuristic2][depth2] += 1
            if result.winner == Player.RED:
                self.heuristic_depth_wins[heuristic2][depth2] += 1
        elif heuristic2 in result.blue_ai_name and result.blue_depth == depth2:
            self.heuristic_depth_stats[heuristic2][depth2].append(result.blue_avg_move_time)
            self.heuristic_depth_moves[heuristic2][depth2].append(result.total_moves)
            self.heuristic_depth_games[heuristic2][depth2] += 1
            if result.winner == Player.BLUE:
                self.heuristic_depth_wins[heuristic2][depth2] += 1

    def run_heuristic_vs_heuristic_experiments(self, games_per_config: int = 3):
        """Run experiments: All heuristics vs each other at different depths"""
        print("\n" + "=" * 60)
        print("🧪 EXPERIMENT 2: Heuristics vs Heuristics")
        print("=" * 60)
        
        experiment_results = {}
        heuristic_names = list(self.heuristics.keys())
        
        for i, heuristic1 in enumerate(heuristic_names):
            for j, heuristic2 in enumerate(heuristic_names):
                if i >= j:  # Avoid duplicate matchups and self-play
                    continue
                
                for depth1 in self.depths:
                    for depth2 in self.depths:
                        print(f"\n🔬 {heuristic1} (D{depth1}) vs {heuristic2} (D{depth2})")
                        print("-" * 50)
                        
                        games_results = []
                        
                        for game_num in range(games_per_config):
                            # Alternate who plays first
                            if game_num % 2 == 0:
                                red_config = self.create_ai(Player.RED, "Smart", depth1, heuristic1)
                                blue_config = self.create_ai(Player.BLUE, "Smart", depth2, heuristic2)
                            else:
                                red_config = self.create_ai(Player.RED, "Smart", depth2, heuristic2)
                                blue_config = self.create_ai(Player.BLUE, "Smart", depth1, heuristic1)
                            
                            result = self.play_single_game(red_config, blue_config, game_num + 1)
                            games_results.append(result)
                            self.results.append(result)
                            
                            # Track detailed statistics for CSV export
                            self._update_heuristic_stats(result, heuristic1, depth1, heuristic2, depth2)
                        
                        # Calculate stats
                        h1_wins = sum(1 for r in games_results 
                                     if (heuristic1 in r.red_ai_name and r.winner == Player.RED) or
                                        (heuristic1 in r.blue_ai_name and r.winner == Player.BLUE))
                        
                        h1_move_times = []
                        h2_move_times = []
                        
                        for result in games_results:
                            if heuristic1 in result.red_ai_name:
                                h1_move_times.append(result.red_avg_move_time)
                                h2_move_times.append(result.blue_avg_move_time)
                            else:
                                h1_move_times.append(result.blue_avg_move_time)
                                h2_move_times.append(result.red_avg_move_time)
                        
                        config_key = f"{heuristic1}_D{depth1}_vs_{heuristic2}_D{depth2}"
                        experiment_results[config_key] = {
                            'h1_stats': ExperimentStats(
                                games_played=games_per_config,
                                wins=h1_wins,
                                losses=games_per_config - h1_wins,
                                draws=0,
                                avg_move_time=statistics.mean(h1_move_times),
                                avg_game_duration=statistics.mean([r.game_duration for r in games_results]),
                                avg_moves_per_game=statistics.mean([r.total_moves for r in games_results]),
                                win_rate=h1_wins / games_per_config * 100
                            ),
                            'h2_stats': ExperimentStats(
                                games_played=games_per_config,
                                wins=games_per_config - h1_wins,
                                losses=h1_wins,
                                draws=0,
                                avg_move_time=statistics.mean(h2_move_times),
                                avg_game_duration=statistics.mean([r.game_duration for r in games_results]),
                                avg_moves_per_game=statistics.mean([r.total_moves for r in games_results]),
                                win_rate=(games_per_config - h1_wins) / games_per_config * 100
                            )
                        }
                        
                        print(f"📈 {heuristic1}: {h1_wins}/{games_per_config} wins")
                        print(f"📈 {heuristic2}: {games_per_config - h1_wins}/{games_per_config} wins")
                        
                        # Report move counts and times for each heuristic at each depth
                        h1_avg_moves = statistics.mean([r.total_moves for r in games_results 
                                                       if heuristic1 in (r.red_ai_name if r.red_depth == depth1 else r.blue_ai_name)])
                        h2_avg_moves = statistics.mean([r.total_moves for r in games_results 
                                                       if heuristic2 in (r.red_ai_name if r.red_depth == depth2 else r.blue_ai_name)])
                        
                        print(f"📊 {heuristic1} D{depth1}: Avg {statistics.mean(h1_move_times):.3f}s/move, {h1_avg_moves:.1f} moves/game")
                        print(f"📊 {heuristic2} D{depth2}: Avg {statistics.mean(h2_move_times):.3f}s/move, {h2_avg_moves:.1f} moves/game")
        
        return experiment_results
    
    def generate_depth_performance_report(self):
        """Generate performance report by depth"""
        print("\n" + "=" * 60)
        print("📊 DEPTH PERFORMANCE ANALYSIS")
        print("=" * 60)
        
        depth_stats = {}
        
        for depth in self.depths:
            depth_games = [r for r in self.results 
                          if r.red_depth == depth or r.blue_depth == depth]
            
            if not depth_games:
                continue
                
            move_times = []
            for result in depth_games:
                if result.red_depth == depth:
                    move_times.append(result.red_avg_move_time)
                if result.blue_depth == depth:
                    move_times.append(result.blue_avg_move_time)
            
            if move_times:
                depth_stats[depth] = {
                    'games_count': len(depth_games),
                    'avg_move_time': statistics.mean(move_times),
                    'min_move_time': min(move_times),
                    'max_move_time': max(move_times),
                    'std_dev': statistics.stdev(move_times) if len(move_times) > 1 else 0
                }
        
        print("\n🕐 Average Move Times by Depth:")
        print("-" * 40)
        for depth in sorted(depth_stats.keys()):
            stats = depth_stats[depth]
            print(f"Depth {depth}: {stats['avg_move_time']:.3f}s ± {stats['std_dev']:.3f}s")
            print(f"  Range: {stats['min_move_time']:.3f}s - {stats['max_move_time']:.3f}s")
            print(f"  Games: {stats['games_count']}")
        
        return depth_stats
    
    def generate_heuristic_ranking_report(self):
        """Generate heuristic ranking based on performance"""
        print("\n" + "=" * 60)
        print("🏆 HEURISTIC PERFORMANCE RANKING")
        print("=" * 60)
        
        heuristic_performance = {}
        
        for heuristic_name in self.heuristics.keys():
            wins = 0
            total_games = 0
            move_times = []
            
            for result in self.results:
                # Check if this heuristic was involved
                if heuristic_name in result.red_ai_name:
                    total_games += 1
                    if result.winner == Player.RED:
                        wins += 1
                    move_times.append(result.red_avg_move_time)
                elif heuristic_name in result.blue_ai_name:
                    total_games += 1
                    if result.winner == Player.BLUE:
                        wins += 1
                    move_times.append(result.blue_avg_move_time)
            
            if total_games > 0:
                heuristic_performance[heuristic_name] = {
                    'win_rate': wins / total_games * 100,
                    'total_games': total_games,
                    'wins': wins,
                    'avg_move_time': statistics.mean(move_times) if move_times else 0
                }
        
        # Sort by win rate
        sorted_heuristics = sorted(heuristic_performance.items(), 
                                 key=lambda x: x[1]['win_rate'], reverse=True)
        
        print("\n🥇 Heuristic Rankings (by win rate):")
        print("-" * 50)
        for rank, (name, stats) in enumerate(sorted_heuristics, 1):
            print(f"{rank}. {name}")
            print(f"   Win Rate: {stats['win_rate']:.1f}% ({stats['wins']}/{stats['total_games']})")
            print(f"   Avg Move Time: {stats['avg_move_time']:.3f}s")
        
        return sorted_heuristics
    
    def save_detailed_results(self, filename: str = "experiment_results.txt"):
        """Save detailed results to file"""
        with open(filename, 'w') as f:
            f.write("Chain Reaction Heuristic Experiment Results\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Grid Size: {self.grid_size}x{self.grid_size}\n")
            f.write(f"Time Limit: {self.time_limit}s per move\n")
            f.write(f"Total Games: {len(self.results)}\n\n")
            
            f.write("Detailed Game Results:\n")
            f.write("-" * 30 + "\n")
            for i, result in enumerate(self.results, 1):
                f.write(f"Game {i}: {result.red_ai_name} vs {result.blue_ai_name}\n")
                f.write(f"  Winner: {result.winner.value if result.winner else 'Draw'}\n")
                f.write(f"  Duration: {result.game_duration:.2f}s, Moves: {result.total_moves}\n")
                f.write(f"  Move Times: Red {result.red_avg_move_time:.3f}s, Blue {result.blue_avg_move_time:.3f}s\n\n")
        
        print(f"\n💾 Detailed results saved to {filename}")
    
    def save_heuristic_performance_csv(self, filename: str = "heuristic_performance.csv"):
        """Save detailed heuristic performance data to CSV file"""
        csv_data = []
        
        # Create header
        headers = [
            "Heuristic", "Depth", "Total_Games", "Wins", "Win_Rate_%", 
            "Avg_Move_Time_s", "Std_Move_Time_s", "Min_Move_Time_s", "Max_Move_Time_s",
            "Avg_Moves_Per_Game", "Std_Moves_Per_Game", "Min_Moves_Per_Game", "Max_Moves_Per_Game"
        ]
        
        # Collect data for each heuristic and depth combination
        for heuristic_name in self.heuristics.keys():
            for depth in self.depths:
                if (heuristic_name in self.heuristic_depth_stats and 
                    depth in self.heuristic_depth_stats[heuristic_name] and 
                    self.heuristic_depth_stats[heuristic_name][depth]):
                    
                    move_times = self.heuristic_depth_stats[heuristic_name][depth]
                    move_counts = self.heuristic_depth_moves[heuristic_name][depth]
                    total_games = self.heuristic_depth_games[heuristic_name][depth]
                    wins = self.heuristic_depth_wins[heuristic_name][depth]
                    
                    # Calculate statistics
                    win_rate = (wins / total_games * 100) if total_games > 0 else 0
                    
                    # Move time statistics
                    avg_move_time = statistics.mean(move_times) if move_times else 0
                    std_move_time = statistics.stdev(move_times) if len(move_times) > 1 else 0
                    min_move_time = min(move_times) if move_times else 0
                    max_move_time = max(move_times) if move_times else 0
                    
                    # Move count statistics
                    avg_moves = statistics.mean(move_counts) if move_counts else 0
                    std_moves = statistics.stdev(move_counts) if len(move_counts) > 1 else 0
                    min_moves = min(move_counts) if move_counts else 0
                    max_moves = max(move_counts) if move_counts else 0
                    
                    # Create row
                    row = [
                        heuristic_name, depth, total_games, wins, round(win_rate, 2),
                        round(avg_move_time, 4), round(std_move_time, 4), 
                        round(min_move_time, 4), round(max_move_time, 4),
                        round(avg_moves, 1), round(std_moves, 1), 
                        int(min_moves), int(max_moves)
                    ]
                    csv_data.append(row)
        
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(csv_data)
        
        print(f"\n📊 Heuristic performance data saved to {filename}")
        print(f"   Data includes {len(csv_data)} heuristic-depth combinations")
        
        return filename
    
    def generate_performance_summary(self):
        """Generate a comprehensive performance summary"""
        print("\n" + "=" * 60)
        print("📈 COMPREHENSIVE PERFORMANCE SUMMARY")
        print("=" * 60)
        
        # Summary by depth
        print("\n🔍 Performance by Depth:")
        print("-" * 40)
        for depth in sorted(self.depths):
            depth_games = 0
            depth_avg_times = []
            depth_wins = 0
            
            for heuristic in self.heuristics.keys():
                if heuristic in self.heuristic_depth_stats and depth in self.heuristic_depth_stats[heuristic]:
                    depth_games += self.heuristic_depth_games[heuristic][depth]
                    depth_avg_times.extend(self.heuristic_depth_stats[heuristic][depth])
                    depth_wins += self.heuristic_depth_wins[heuristic][depth]
            
            if depth_games > 0:
                avg_time = statistics.mean(depth_avg_times) if depth_avg_times else 0
                win_rate = depth_wins / depth_games * 100
                print(f"  Depth {depth}: {depth_games} games, {avg_time:.4f}s avg move time, {win_rate:.1f}% win rate")
        
        # Summary by heuristic
        print("\n🎯 Performance by Heuristic (across all depths):")
        print("-" * 50)
        heuristic_summary = []
        
        for heuristic in self.heuristics.keys():
            total_games = sum(self.heuristic_depth_games[heuristic][depth] for depth in self.depths 
                            if depth in self.heuristic_depth_games[heuristic])
            total_wins = sum(self.heuristic_depth_wins[heuristic][depth] for depth in self.depths 
                           if depth in self.heuristic_depth_wins[heuristic])
            all_times = []
            for depth in self.depths:
                if depth in self.heuristic_depth_stats[heuristic]:
                    all_times.extend(self.heuristic_depth_stats[heuristic][depth])
            
            if total_games > 0:
                win_rate = total_wins / total_games * 100
                avg_time = statistics.mean(all_times) if all_times else 0
                heuristic_summary.append((heuristic, win_rate, avg_time, total_games))
        
        # Sort by win rate
        heuristic_summary.sort(key=lambda x: x[1], reverse=True)
        
        for rank, (heuristic, win_rate, avg_time, games) in enumerate(heuristic_summary, 1):
            print(f"  {rank}. {heuristic}: {win_rate:.1f}% win rate, {avg_time:.4f}s avg move time ({games} games)")

def main():
    """Run all experiments"""
    print("🧪 Chain Reaction Heuristic Experiments")
    print("=" * 60)
    print("Configuration:")
    print("- Grid Size: 5x5")
    print("- Time Limit: 10 seconds per move")
    print("- Depths: 2, 3, 4")
    print("- Heuristics: 6 different heuristics")
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create experiment instance
    experiment = HeuristicExperiment(grid_size=5, time_limit=10.0, verbose=False)
    
    print(f"\n🎯 Available Heuristics:")
    for i, name in enumerate(experiment.heuristics.keys(), 1):
        print(f"  {i}. {name}")
    
    # Run experiments
    start_time = time.time()
    
    # Experiment 1: Heuristics vs Random
    # exp1_results = experiment.run_heuristic_vs_random_experiments(games_per_config=3)
    
    # Experiment 2: Heuristics vs Heuristics (reduced to save time)
    exp2_results = experiment.run_heuristic_vs_heuristic_experiments(games_per_config=2)
    
    # Generate reports
    depth_stats = experiment.generate_depth_performance_report()
    heuristic_rankings = experiment.generate_heuristic_ranking_report()
    experiment.generate_performance_summary()
    
    # Save results
    experiment.save_detailed_results()
    experiment.save_heuristic_performance_csv("heuristic_performance.csv")
    
    total_time = time.time() - start_time
    print(f"\n⏱️  Total Experiment Duration: {total_time:.1f} seconds")
    print(f"🎮 Total Games Played: {len(experiment.results)}")
    
    print("\n✅ Experiments completed successfully!")
    print("📁 Files generated:")
    print("   - experiment_results.txt (detailed text results)")
    print("   - heuristic_performance.csv (structured performance data)")

if __name__ == "__main__":
    main()
