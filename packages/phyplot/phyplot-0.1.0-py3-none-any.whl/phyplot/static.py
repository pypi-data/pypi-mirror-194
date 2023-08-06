import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Static():
	'''
	 Data class for plotting trees and associated data.
	'''
    
	def __init__(self):
		'''
		Initializes the Data class.
		'''

	def plot_tree(self, tree):
		'''
		Plots a phylogenetic tree by postorder tree traversal.

		Args:
			tree (tree object): Phylogenetic tree.
		'''

		# Determine the number of taxa in the tree
		taxon_set = tree.root.partition
		n_taxa = len(tree.root.partition)

		# Scale font sizes
		fscale = round(15 - math.log(n_taxa, 1.5))
		if fscale < 1:
			fscale = 1

		# Scale line widths
		lscale = (1.5 - math.log(n_taxa, 1000))

		# Create axes and plot area
		self.plot_tree_format(tree, n_taxa, lscale)

		# Establish y-positions
		y_e = 0
		y_pos = []

		# Postorder tree traversal
		for node in tree.node_list_postorder:

			# Setup the line segment coordinates for edge (branches)
			x_min = node.dist_to_root - node.branch_length
			x_max = node.dist_to_root

			if node.tip:
				# Create spacing along the y-axis and append to list
				y_e += 100 / n_taxa
				y_pos.append(y_e)

				# Plot external branches with taxon labels
				self.plot_tree_edge(y_e, x_min, x_max, 'black', lscale)
				self.plot_tree_taxatags(1.01*x_max, y_e, node.taxa, fscale)

			if not node.tip:
				# Determine the size split line (it could be more than two for polytomies) & plot
				neg_clade_size = -1 * len(list(node.node_list))
				self.plot_tree_split(x_max, y_pos[neg_clade_size], y_pos[-1], 'black', lscale)

				# Determine the placement of the parent (ancestral) edge along the y-axis
				y_i = (y_pos[neg_clade_size] + y_pos[-1]) / 2

				# Delete all the taxa  contained in the clade just drawn (could be more than 2 for polytomies)
				del y_pos[neg_clade_size:]
				y_pos.append(y_i)

				# Plot the parent (ancestral) edge along the y-axis
				self.plot_tree_edge(y_i, x_min, x_max, 'black', lscale)

		# Add root branch
		root_length = -0.02 * tree.get_max_dist_to_root()
		self.plot_tree_edge(y_pos[0], 0, root_length, 'black', lscale)

		return self.fig

	def plot_tree_edge(self, y_e, x_min, x_max, color, lscale):
		'''
		Plots a phylogenetic edge (branch).

		Args:
			y_e (float): Coordinate for placement along the y-axis.
			x_min (float): Coordinate for start of edge.
			x_max (float): Coordinate for end of edge.
			color (string): Color of edge line.
			lscale (float): Scaling parameter for line width.
		'''

		plt.hlines(y=y_e, xmin=x_min, xmax=x_max, color=color, linewidths=lscale)

	def plot_tree_split(self, x_s, y_min, y_max, color, lscale):
		'''
		Plots a phylogenetic split.

		Args:
			x_s (float): Coordinate for placement along the x-axis.
			y_min (float): Coordinate for start of split.
			y_max (float): Coordinate for end of split.
			color (string): Color of split line.
			lscale (float): Scaling parameter for line width.
		'''

		plt.vlines(x=x_s, ymin=y_min, ymax=y_max, color=color, linewidths=lscale)

	def plot_tree_taxatags(self, x_taxa, y_taxa, taxon, fscale):
		'''
		Plots taxa at the tips of the terminal edges.

		Args:
			x_taxa (float): Coordinate for placement along the x-axis.
			y_taxa (float): Coordinate for placement along the x-axis.
			taxon (string): The name of the taxon.
			fscale (float): Scaling parameter for font size.
		'''

		plt.text(x_taxa, y_taxa, taxon, verticalalignment='center', fontsize=fscale)
		
	def plot_tree_format(self, tree, n_taxa, lscale):
		'''
		Formats the plot area for the phylogenetic tree.

		Args:
			tree (tree object): Phylogenetic tree.
			n_taxa (integer): The number of taxa in the tree.
			lscale (float): Scaling parameter for line width (for scale bar).
		'''
			
		# Setup figure & axes
		self.fig = plt.figure()

		# Set axes ranges
		x_adjust = tree.get_max_dist_to_root()
		y_adjust = 100 / n_taxa
		x_min = -0.05 * x_adjust
		x_max = 1.1 * x_adjust
		y_min = 0
		y_max = 100 + y_adjust
		plt.axis([x_min, x_max, y_max, y_min])

		# Create scale bar
		scale_bar_x = 0.2 * tree.get_max_dist_to_root()
		scale_bar_text = f'\n{scale_bar_x:.2f}'
		scale_bar_y = 100 + 0.1 * (100 - y_adjust)
		plt.hlines(y=100, xmin=0, xmax=scale_bar_x, linewidths=lscale, color='darkgrey')
		plt.text(scale_bar_x/2, 100, scale_bar_text, ha='center', va='top', fontsize=8, color='darkgrey')

		# Remove frames and axes
		plt.axis('off')
