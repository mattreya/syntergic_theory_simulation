import numpy as np

class PerceptualSieve:
    """
    Models the interference between the Neuronal Field and the Lattice
    to produce the Perceived Reality Output (Rp).
    """
    
    @staticmethod
    def generate_reality(lattice, neuronal_field):
        """
        Takes the Lattice matrix (L) and Neuronal Field operator (Fn)
        and computes the interference pattern.
        
        Args:
            lattice (Lattice): The underlying pre-space matrix.
            neuronal_field (NeuronalField): The agent's field operator.
            
        Returns:
            np.ndarray: The resulting 'Perceived Reality' array.
        """
        L = lattice.get_state()
        Fn = neuronal_field.get_operator()
        
        if L.shape != Fn.shape:
            raise ValueError(f"Shape mismatch: Lattice {L.shape} and Neuronal Field {Fn.shape} must match.")
        
        # In Syntergic theory, the interaction is often conceptualized as a convolution or 
        # complex interference. Here, we model it as an element-wise multiplication in the 
        # frequency domain, which equates to a spatial convolution, filtering the lattice.
        
        # Transform both to frequency domain
        L_fft = np.fft.fftn(L)
        Fn_fft = np.fft.fftn(Fn)
        
        # The Neuronal Field acts as a filter/sieve on the Lattice
        # Rp = T(Fn * L)
        interference_fft = L_fft * Fn_fft
        
        # Transform back to spatial domain
        Rp = np.fft.ifftn(interference_fft)
        
        # Return the magnitude (perceived physical reality is observable amplitude)
        return np.abs(Rp)
