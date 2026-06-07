import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Ensure we can import from src
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'src'))

from multi_agent import Swarm
from lattice import Lattice
from transformation import PerceptualSieve

SIZE = 100
NUM_STEPS = 50

lattice = Lattice(size=SIZE, dimensions=2)
swarm = Swarm(num_agents=100, size=SIZE, dimensions=2)
sieve = PerceptualSieve()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

def update(frame):
    ax1.clear()
    ax2.clear()
    
    lattice.evolve(1)
    
    class DummyField:
        def __init__(self, state):
            self.state = state
        def get_state(self):
            return self.state
            
    dummy_field = DummyField(lattice.get_state())
    swarm.step(dummy_field, proximity_threshold=5.0)
    sieve.process(swarm, dummy_field)
    
    ax1.imshow(np.abs(dummy_field.get_state()), cmap='inferno')
    positions = np.array([agent.position for agent in swarm.agents])
    if len(positions) > 0:
        ax1.scatter(positions[:, 1], positions[:, 0], c='cyan', s=10)
    ax1.set_title(f"Lattice & Swarm (Turn {frame})\nActive Agents: {len(swarm.agents)}")
    ax1.axis('off')
    
    ax2.imshow(np.abs(sieve.reality_tensor), cmap='viridis')
    ax2.set_title(f"Perceived Reality\nVariance: {np.var(np.abs(sieve.reality_tensor)):.2f}")
    ax2.axis('off')
    
    print(f"Rendered frame {frame}/{NUM_STEPS}")

ani = animation.FuncAnimation(fig, update, frames=NUM_STEPS, interval=200)
ani.save('simulation_class4.gif', writer='pillow', fps=5)
print("Saved animation to simulation_class4.gif")
