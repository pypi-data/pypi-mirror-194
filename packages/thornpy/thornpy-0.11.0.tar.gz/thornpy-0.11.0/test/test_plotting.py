from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from thornpy.plotting import plot_3d, save_multifig
import matplotlib.pyplot as plt
import numpy as np

class Test_Plotting(unittest.TestCase):

    def setUp(self):
        return

    def test_plot_3d(self):
        x = [1,2,3,4,5]
        y = [10, 15, 20, 15, 10]
        z = [0, 0, 0, 0, 0]
        figure = plot_3d(x, y, z)
        plt.show()
        
        self.assertEqual(0,1)

    def test_concat_figs(self):
        x = np.array([1,2,3,4,5])
        y = np.array([10, 15, 20, 15, 10])
        fig_1, ax_1 = plt.subplots()
        ax_1.plot(x, y)
        fig_2, ax_2 = plt.subplots()
        ax_2.plot(x, y*2)

        with TemporaryDirectory() as tmp:
            png_file = Path(tmp) / 'tmp.png'
            fig = save_multifig([fig_1, fig_2], png_file)
            self.assertTrue(png_file.exists())
    
    def tearDown(self):
        return

    