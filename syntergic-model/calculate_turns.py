import sys
import os
import time

sys.path.append(os.path.abspath('src'))
from multi_agent import Swarm

def run_headless_sim(start_agents=500, target_agents=100, max_steps=2000):
    print(f"Starting headless simulation with {start_agents} agents. Target: {target_agents} macro-agents.")
    swarm = Swarm(num_agents=start_agents, size=100, dimensions=2)
    
    for step in range(max_steps):
        # advance physics
        swarm.step(proximity_threshold=15.0, freq_tolerance=3.0, drift_speed=5.0)
        
        active = sum(1 for a in swarm.agents if a.active)
        
        if active <= target_agents:
            print(f"Target reached in {step + 1} turns! (Active agents: {active})")
            return step + 1
            
        if step > 0 and step % 50 == 0:
            print(f"Turn {step}: {active} agents remaining...")
            
    print(f"Failed to reach target within {max_steps} turns. Ended with {active} agents.")
    return max_steps

if __name__ == "__main__":
    run_headless_sim(start_agents=1000, target_agents=100)
