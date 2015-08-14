from lfdft.grid import GridDesc
from lfdft.setups import Setups
from lfdft.occupations import Occupations
from lfdft.density import Density
from lfdft.hamiltonian import Hamiltonian
from lfdft.wfs import WaveFunctions
from lfdft.scf import SCF


class Calculator:
    """Main object for a groundstate calculation."""
    def __init__(self, p, atoms, out):
        self.p = p
        self.out = out

        self.scf = SCF(p, out)
        self.grid = GridDesc(p, atoms, out)
        self.setups = Setups(atoms, out)
        atoms.set_charges(self.setups)
        self.fn = Occupations(atoms, self.setups, out)
        self.density = Density(self.grid, self.setups, atoms)            
        self.hamiltonian = Hamiltonian(p, self.grid, self.setups, atoms,
                                       self.density)
        self.wfs = WaveFunctions(self.grid, self.fn)            
        
    def solve_scf(self):
        self.scf.run(self.wfs, self.hamiltonian, self.density, self.fn)
        self.out.write('total_energy (eV): {}\n'.format(
            self.scf.total_energy[-1]))
            

