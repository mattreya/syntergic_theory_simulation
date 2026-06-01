import numpy as np

class ProtoAgent:
    """
    A simple, localized unit of consciousness in the Lattice.
    """
    def __init__(self, x: float, y: float, coherence: float, frequency: float, radius: float = 10.0):
        self.x = x
        self.y = y
        self.coherence = coherence
        self.frequency = frequency
        self.radius = radius
        self.active = True # False if merged into another agent

class Swarm:
    """
    Manages multiple ProtoAgents, simulating Brownian drift and resonance chaining.
    """
    def __init__(self, num_agents: int = 50, size: int = 100, dimensions: int = 2):
        self.size = size
        self.dimensions = dimensions
        self.shape = tuple([size] * dimensions)
        self.agents = []
        
        # Initialize random proto-agents with low coherence
        for _ in range(num_agents):
            agent = ProtoAgent(
                x=np.random.uniform(0, size),
                y=np.random.uniform(0, size),
                coherence=np.random.uniform(0.01, 0.15),
                frequency=np.random.uniform(0.1, 2.0),
                radius=np.random.uniform(5.0, 15.0)
            )
            self.agents.append(agent)

    def step(self, proximity_threshold: float = 10.0, freq_tolerance: float = 2.0, drift_speed: float = 2.0, attraction_strength: float = 1.0):
        """
        Advances the simulation by one step.
        1. Empathy Gravity: Agents calculate a vector toward the largest resonant neighbor.
        2. Agents drift randomly.
        3. Agents that are close and share similar frequencies merge.
        """
        active_agents = [a for a in self.agents if a.active]
        
        # 1. Empathy Gravity (Transferred Potential)
        for agent in active_agents:
            best_target = None
            max_pull = 0.0
            
            for other in active_agents:
                if agent is other: continue
                
                # Check if they are empathetic (resonant frequencies)
                freq_diff = abs(agent.frequency - other.frequency)
                if freq_diff < freq_tolerance:
                    dist = np.sqrt((agent.x - other.x)**2 + (agent.y - other.y)**2)
                    if dist > 0:
                        # Gravity formula: proportional to size/coherence, inversely proportional to distance squared
                        pull = (other.radius * other.coherence) / (dist**2)
                        if pull > max_pull:
                            max_pull = pull
                            best_target = other
                            
            if best_target:
                # Calculate directional vector
                dx = best_target.x - agent.x
                dy = best_target.y - agent.y
                dist = np.sqrt(dx**2 + dy**2)
                
                # Apply attraction
                agent.x += (dx / dist) * attraction_strength
                agent.y += (dy / dist) * attraction_strength

        # 2. Drift
        for agent in active_agents:
            agent.x = np.clip(agent.x + np.random.uniform(-drift_speed, drift_speed), 0, self.size - 1)
            agent.y = np.clip(agent.y + np.random.uniform(-drift_speed, drift_speed), 0, self.size - 1)
                
        # 3. Check for Resonance and Merge
        active_agents = [a for a in self.agents if a.active]
        
        for i in range(len(active_agents)):
            a1 = active_agents[i]
            if not a1.active: continue
            
            for j in range(i + 1, len(active_agents)):
                a2 = active_agents[j]
                if not a2.active: continue
                
                # Check distance
                dist = np.sqrt((a1.x - a2.x)**2 + (a1.y - a2.y)**2)
                
                if dist < proximity_threshold:
                    # Check frequency resonance
                    freq_diff = abs(a1.frequency - a2.frequency)
                    if freq_diff < freq_tolerance:
                        # Entangle and Merge!
                        # a1 absorbs a2
                        a1.coherence = min(1.0, a1.coherence + a2.coherence * 0.5)
                        
                        # Calculate new radius conserving area (creates large amoeba growth)
                        a1.radius = np.sqrt(a1.radius**2 + a2.radius**2)
                        
                        # Average and slightly lower their frequency to smooth out the blob
                        a1.frequency = ((a1.frequency + a2.frequency) / 2.0) * 0.95
                        
                        # Center point between them
                        a1.x = (a1.x + a2.x) / 2.0
                        a1.y = (a1.y + a2.y) / 2.0
                        
                        a2.active = False # a2 is consumed

    def get_operator(self):
        """
        Combines all active agents into a single macroscopic Neuronal Field operator.
        """
        global_operator = np.zeros(self.shape, dtype=complex)
        
        coords = [np.arange(self.size) for _ in range(self.dimensions)]
        grid = np.meshgrid(*coords, indexing='ij')
        
        active_agents = [a for a in self.agents if a.active]
        
        for agent in active_agents:
            # Calculate distance from this agent's center
            r = np.sqrt((grid[0] - agent.x)**2 + (grid[1] - agent.y)**2)
            
            # Create a localized envelope (Gaussian falloff)
            envelope = np.exp(-(r**2) / (2 * agent.radius**2))
            
            # Coherent component (harmonic oscillation)
            coherent_part = np.cos(2 * np.pi * agent.frequency * r) + 1j * np.sin(2 * np.pi * agent.frequency * r)
            
            # Incoherent component (noise)
            noise_amplitude = np.random.rand(*self.shape)
            noise_phase = np.random.uniform(0, 2 * np.pi, self.shape)
            incoherent_part = noise_amplitude * np.exp(1j * noise_phase)
            
            # Local operator for this agent
            local_op = (agent.coherence * coherent_part) + ((1 - agent.coherence) * incoherent_part)
            
            # Apply spatial envelope and add to global operator
            global_operator += local_op * envelope
            
        # Normalize
        norm_factor = np.mean(np.abs(global_operator))
        if norm_factor > 0:
            global_operator = global_operator / norm_factor
            
        return global_operator
