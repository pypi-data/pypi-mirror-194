# Note: to run tests type 'pytest' in the terminal at the parent directory using: pytest -p no:warnings
# https://stackoverflow.com/questions/27948126/how-can-i-write-unit-tests-against-code-that-uses-matplotlib
# To see attributes:
#   fig = phyplot.PhyPlot().plot_tree(tree)
#   fig._localaxes().__dict__

# Import libraries
import sciphy
import numpy as np, pandas as pd
import phyplot

# Load toy tree (nexus) & data
toy_trees, toy_data = sciphy.DataSets().load_toy()

# Load plant tree & data
plant_trees, plant_data = sciphy.DataSets().load_plant_genome_phys()

def test_static_tree():
	'''static tree plot test'''
	
	fig = phyplot.PlotTree().plot_tree(toy_trees[0])

	assert str(fig._localaxes().texts[1]) == "Text(3.0300000000000002, 20.0, 'a')"

def test_interactive_boxplot():
	'''interactive boxplot plot test'''

	fig = phyplot.Interact().boxplot(toy_data.df)

	assert fig._data[0]['text'][0] == 'a'

