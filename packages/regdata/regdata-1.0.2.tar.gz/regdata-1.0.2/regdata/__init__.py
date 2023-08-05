
# Dataloaders
from .dataloaders.step import Step
from .dataloaders.smooth1d import Smooth1D
from .dataloaders.noisy_sine import SineNoisy
from .dataloaders.sinejump import SineJump1D
from .dataloaders.olympic import Olympic
from .dataloaders.mcycle import MotorcycleHelmet
from .dataloaders.della_gatta_gene import DellaGattaGene
from .config import set_backend
import os
os.environ['BACKEND'] = 'numpy'
os.environ['DATAPATH'] = '/tmp/somerandomtexthere_'
