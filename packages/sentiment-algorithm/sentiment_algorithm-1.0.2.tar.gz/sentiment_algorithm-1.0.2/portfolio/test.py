import sys

sys.path.append(".")
# Commented out IPython magic to ensure Python compatibility.
from portfolio.simulation import Simulation
my_figures= Simulation(stock_id="AAPL", start="2021-01-01", end ="2021-03-01")
my_figures.signal_raw_position_graph()
my_figures.signal_senti_graph()
my_figures.get_portfolio()