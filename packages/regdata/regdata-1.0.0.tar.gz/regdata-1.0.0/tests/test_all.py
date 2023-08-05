from .common import backend_test, plotting_test, non_syntetic_test
import regdata as rd


def test_della_gatta_gene():
    backend_test(rd.DellaGattaGene)
    plotting_test(rd.DellaGattaGene)
    non_syntetic_test(rd.DellaGattaGene)


def test_mcycle():
    backend_test(rd.MotorcycleHelmet)
    plotting_test(rd.MotorcycleHelmet)
    non_syntetic_test(rd.MotorcycleHelmet)
    
def test_olympic():
    backend_test(rd.Olympic)
    plotting_test(rd.Olympic)
    non_syntetic_test(rd.Olympic)

def test_sinejump():
    backend_test(rd.SineJump1D)
    plotting_test(rd.SineJump1D)

def test_smooth1d():
    backend_test(rd.Smooth1D)
    plotting_test(rd.Smooth1D)
    
def test_step():
    backend_test(rd.Step)
    plotting_test(rd.Step)