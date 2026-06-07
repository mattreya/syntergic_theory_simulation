import json
import sys

def update_nb():
    with open("notebooks/simulation.ipynb", "r") as f:
        nb = json.load(f)

    new_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Phase 2: Dynamic Multi-Agent Resonance Chaining\n",
                "This section simulates how simple, low-coherence units of consciousness (Proto-Agents) interact over time.\n",
                "As they drift through the lattice, agents that are in close proximity and share similar frequencies will entangle, merge, and increase their overall coherence. Watch how chaotic noise self-organizes into highly structured, amoeba-like macro-agents."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from multi_agent import Swarm\n",
                "from transformation import PerceptualSieve\n",
                "from IPython.display import display, clear_output\n",
                "import time\n",
                "\n",
                "NUM_STEPS = 50\n",
                "swarm = Swarm(num_agents=100, size=SIZE, dimensions=2)\n",
                "\n",
                "# Run the simulation\n",
                "for step in range(NUM_STEPS):\n",
                "    # Advance Lattice CA physics\n",
                "    lattice.evolve(1)\n",
                "    \n",
                "    # Calculate current state\n",
                "    swarm_op = swarm.get_operator()\n",
                "    \n",
                "    # Wrapper for PerceptualSieve\n",
                "    class DummyField:\n",
                "        def get_operator(self): return swarm_op\n",
                "        \n",
                "    reality = PerceptualSieve.generate_reality(lattice, DummyField())\n",
                "    \n",
                "    # Plot\n",
                "    clear_output(wait=True)\n",
                "    fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n",
                "    \n",
                "    axes[0].set_title(f\"Swarm Field (Step {step})\")\n",
                "    im0 = axes[0].imshow(np.abs(swarm_op), cmap='viridis')\n",
                "    fig.colorbar(im0, ax=axes[0])\n",
                "    \n",
                "    axes[1].set_title(f\"Perceived Reality (Step {step})\")\n",
                "    im1 = axes[1].imshow(reality, cmap='plasma')\n",
                "    fig.colorbar(im1, ax=axes[1])\n",
                "    \n",
                "    plt.show()\n",
                "    \n",
                "    # Advance physics with gentler parameters\n",
                "    swarm.step(proximity_threshold=5.0, freq_tolerance=3.0, drift_speed=5.0)\n",
                "    \n",
                "    # Small pause for animation effect\n",
                "    time.sleep(0.5)\n",
                "\n",
                "active = sum(1 for a in swarm.agents if a.active)\n",
                "print(f\"Simulation finished. 100 initial proto-agents merged into {active} macro-agents.\")"
            ]
        }
    ]

    nb["cells"].extend(new_cells)

    with open("notebooks/simulation.ipynb", "w") as f:
        json.dump(nb, f, indent=1)

if __name__ == "__main__":
    update_nb()
