import numpy as np

class Lattice:
    """
    Represents the Holographic Lattice (Pre-space Matrix).
    It is modeled as a high-density N-dimensional complex tensor
    where each point contains an integrated informational state.
    """
    def __init__(self, size: int = 100, dimensions: int = 2):
        """
        Initialize the Lattice.
        
        Args:
            size (int): The number of nodes along each dimension.
            dimensions (int): The dimensionality of the lattice (e.g., 2D or 3D).
        """
        self.size = size
        self.dimensions = dimensions
        self.shape = tuple([size] * dimensions)
        
        # Initialize the state matrix with random phase and amplitude
        # representing the "undifferentiated" high-density information.
        amplitude = np.random.rand(*self.shape)
        phase = np.random.uniform(0, 2 * np.pi, self.shape)
        
        self.matrix = amplitude * np.exp(1j * phase)

    def get_state(self):
        """Returns the current raw complex tensor of the lattice."""
        return self.matrix
