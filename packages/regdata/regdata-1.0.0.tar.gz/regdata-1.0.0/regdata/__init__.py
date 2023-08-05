import os
os.environ['BACKEND'] = 'numpy'
os.environ['DATAPATH'] = '/tmp/somerandomtexthere_'

from .config import set_backend


# Dataloaders
from .dataloaders.della_gatta_gene import DellaGattaGene
from .dataloaders.mcycle import MotorcycleHelmet
from .dataloaders.olympic import Olympic
from .dataloaders.sinejump import SineJump1D
from .dataloaders.smooth1d import Smooth1D
from .dataloaders.step import Step




