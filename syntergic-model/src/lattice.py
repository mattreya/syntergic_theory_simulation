import numpy as np

class Lattice:
    """
    Represents the Holographic Lattice (Pre-space Matrix) as a Cellular Automaton.
    It evolves based on simple rules, generating complex patterns.
    """
    def __init__(self, size: int = 100, dimensions: int = 2, initial_density: float = 0.1):
        """
        Initialize the Lattice as a Cellular Automaton.
        
        Args:
            size (int): The number of nodes along each dimension.
            dimensions (int): The dimensionality of the lattice.
            initial_density (float): Density of '1's in the initial random state (0.0 to 1.0).
        """
        if dimensions != 2:
            raise ValueError("Currently, only 2D cellular automata are supported for the Lattice.")

        self.size = size
        self.dimensions = dimensions
        self.shape = tuple([size] * dimensions)
        
        # Initialize the CA matrix with binary states (0 or 1)
        self.matrix = (np.random.rand(*self.shape) < initial_density).astype(int)

    def _count_neighbors(self):
        """Counts active neighbors for each cell in a 2D grid (Moore neighborhood)."""
        neighbors = np.zeros(self.shape, dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                # Iterate over 3x3 neighborhood
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue # Don't count self
                        
                        nx, ny = (i + dx) % self.size, (j + dy) % self.size # Toroidal wrapping
                        neighbors[i, j] += self.matrix[nx, ny]
        return neighbors

    def evolve(self, num_steps: int = 1):
        """
        Evolves the cellular automaton for a given number of steps.
        Rule:
            - A living cell (1) with exactly 1 active neighbor dies (turns 0).
            - A dead cell (0) with exactly 2 active neighbors becomes alive (turns 1).
            - All other cells maintain their state.
            This is a very simple custom rule, not Conway's Game of Life.
        """
        for _ in range(num_steps):
            new_matrix = self.matrix.copy()
            neighbors = self._count_neighbors()

            for i in range(self.size):
                for j in range(self.size):
                    cell_state = self.matrix[i, j]
                    neighbor_count = neighbors[i, j]

                    if cell_state == 1 and neighbor_count == 1:
                        new_matrix[i, j] = 0  # Dies with exactly 1 neighbor
                    elif cell_state == 0 and neighbor_count == 2:
                        new_matrix[i, j] = 1  # Becomes alive with exactly 2 neighbors
                    # Else: state remains unchanged
            self.matrix = new_matrix

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
