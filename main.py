import time_series_visualizer
from unittest import main

# Testear función
time_series_visualizer.draw_line_plot()
time_series_visualizer.draw_bar_plot()
time_series_visualizer.draw_box_plot()

# Correr test automáticamente
main(module='test_module', exit=False)