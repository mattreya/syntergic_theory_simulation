import numpy as np

class Lattice:
    """
    Represents the Holographic Lattice (Pre-space Matrix) as a Cellular Automaton.
    It evolves based on simple rules, generating complex patterns.
    """
    def __init__(self, size: int = 100, dimensions: int = 2, initial_density: float = 0.1,
                 birth_rules=(3,), survival_rules=(2, 3)):
        """
        Initialize the Lattice as a Cellular Automaton.
        
        Args:
            size (int): The number of nodes along each dimension.
            dimensions (int): The dimensionality of the lattice.
            initial_density (float): Density of '1's in the initial random state (0.0 to 1.0).
            birth_rules (tuple): Number of neighbors required for a dead cell to become alive.
            survival_rules (tuple): Number of neighbors required for a living cell to survive.
        """
        if dimensions != 2:
            raise ValueError("Currently, only 2D cellular automata are supported for the Lattice.")

        self.size = size
        self.dimensions = dimensions
        self.shape = tuple([size] * dimensions)
        self.birth_rules = birth_rules
        self.survival_rules = survival_rules
        
        # Initialize the CA matrix with binary states (0 or 1)
        self.matrix = (np.random.rand(*self.shape) < initial_density).astype(int)

    def _count_neighbors(self):
        """Counts active neighbors for each cell in a 2D grid using fast convolution."""
        from scipy.signal import convolve2d
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        # Use mode='same' to keep matrix size, boundary='wrap' for toroidal topology
        return convolve2d(self.matrix, kernel, mode='same', boundary='wrap')

    def evolve(self, num_steps: int = 1):
        """
        Evolves the cellular automaton for a given number of steps.
        Uses the configured birth and survival rules. Default is B3/S23 (Game of Life)
        which is known for yielding Class 4 complex emergent structures.
        """
        for _ in range(num_steps):
            neighbors = self._count_neighbors()
            
            # Apply rules using fast numpy boolean indexing
            birth = np.isin(neighbors, self.birth_rules) & (self.matrix == 0)
            survive = np.isin(neighbors, self.survival_rules) & (self.matrix == 1)
            
            self.matrix = (birth | survive).astype(int)

    def get_state(self):
        """
        Returns the current CA matrix converted to a complex tensor.
        Active cells (1) will have a higher amplitude/defined phase.
        Inactive cells (0) will have zero or very low amplitude.
        """
        # For now, let's map 1 to (1 + 1j) and 0 to 0.0, or a small complex noise.
        # This can be made more sophisticated later.
        complex_state = self.matrix.astype(complex) # 1 -> (1+0j), 0 -> (0+0j)
        
        # Add a small, uniform background noise to 'dead' cells
        # This prevents division by zero in FFT operations if the lattice becomes all zeros
        # and represents the 'undifferentiated pre-space' more accurately even for inactive regions
        noise_amplitude = 0.01 # Small background noise
        background_noise = (np.random.rand(*self.shape) * noise_amplitude) * np.exp(1j * np.random.uniform(0, 2 * np.pi, self.shape))
        
        # Only add noise where cell is '0'
        complex_state[self.matrix == 0] = background_noise[self.matrix == 0]
        
        return complex_state
