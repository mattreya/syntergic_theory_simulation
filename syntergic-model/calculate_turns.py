import os
import sys
import time
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'src'))

from multi_agent import Swarm
from lattice import Lattice
from transformation import PerceptualSieve

class DummyField:
    def __init__(self, op):
        self.op = op
    def get_operator(self):
        return self.op

def run_headless_sim(start_agents=100, max_steps=100):
    print(f"Starting Integrated Lattice/Swarm simulation with {start_agents} agents.")
    
    lattice = Lattice(size=100, dimensions=2)
    swarm = Swarm(num_agents=start_agents, size=100, dimensions=2)
    
    for step in range(max_steps):
        # 1. Evolve the Lattice CA (Wolfram Class 4 search)
        lattice.evolve(1)
        
        # 2. Advance the Swarm Physics (Grinberg Empathetic Gravity)
        swarm.step(proximity_threshold=5.0, freq_tolerance=3.0, drift_speed=5.0)
        
        active = sum(1 for a in swarm.agents if a.active)
        
        # 3. Compute Perceived Reality (The Sieve)
        swarm_op = swarm.get_operator()
        reality = PerceptualSieve.generate_reality(lattice, DummyField(swarm_op))
        
        # 4. Calculate Structural Complexity metrics
        reality_variance = float(np.var(reality))
        reality_max = float(np.max(reality))
        
        if step % 5 == 0 or step == max_steps - 1:
            print(f"Turn {step:>2}: {active:>3} agents | Reality Variance: {reality_variance:.6f} | Reality Max: {reality_max:.6f}")
            
    print(f"Simulation ended after {max_steps} turns with {active} agents.")

if __name__ == "__main__":
    run_headless_sim(start_agents=100, max_steps=100)
