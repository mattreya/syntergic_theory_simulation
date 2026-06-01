import numpy as np

class NeuronalField:
    """
    Represents the Agent's Neuronal Field.
    The Agent generates a field that acts as an operator on the Lattice.
    """
    def __init__(self, coherence: float = 0.5, frequency: float = 1.0, size: int = 100, dimensions: int = 2):
        """
        Initialize the Agent's Neuronal Field.
        
        Args:
            coherence (float): Sigma value between 0.0 and 1.0. 
                               1.0 = High Coherence (Shamanic state, low distortion).
                               0.0 = Low Coherence (Standard reality, high distortion).
            frequency (float): The operational frequency (omega) of the brain.
            size (int): Size of the field to match the Lattice.
            dimensions (int): Dimensionality.
        """
        # Constrain coherence between 0 and 1
        self.coherence = max(0.0, min(1.0, coherence))
        self.frequency = frequency
        self.size = size
        self.dimensions = dimensions
        self.shape = tuple([size] * dimensions)
        
        self.operator = self._generate_operator()

    def _generate_operator(self):
        """
        Generates the mathematical operator representing the neuronal field.
        A perfectly coherent field (sigma=1) is highly aligned and symmetric.
        A low coherence field (sigma->0) is noisy and misaligned.
        """
        # Base structured field (representing high coherence)
        # E.g., a simple radial frequency pattern
        coords = [np.linspace(-1, 1, self.size) for _ in range(self.dimensions)]
        grid = np.meshgrid(*coords, indexing='ij')
        
        # Calculate distance from center for a radial pattern
        r = np.sqrt(sum(g**2 for g in grid))
        
        # Coherent component: smooth harmonic oscillation
        coherent_part = np.cos(2 * np.pi * self.frequency * r) + 1j * np.sin(2 * np.pi * self.frequency * r)
        
        # Incoherent component: random noise
        noise_amplitude = np.random.rand(*self.shape)
        noise_phase = np.random.uniform(0, 2 * np.pi, self.shape)
        incoherent_part = noise_amplitude * np.exp(1j * noise_phase)
        
        # The final operator is a blend based on coherence (sigma)
        operator = (self.coherence * coherent_part) + ((1 - self.coherence) * incoherent_part)
        
        # Normalize the operator so it doesn't arbitrarily scale the lattice energy
        norm_factor = np.mean(np.abs(operator))
        if norm_factor > 0:
            operator = operator / norm_factor
            
        return operator

    def get_operator(self):
        return self.operator
