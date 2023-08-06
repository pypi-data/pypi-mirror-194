from pathlib import Path
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt
import pandas as pd


class GeoScale():

	def __init__(self, divisions=['Eras', 'Periods', 'Epochs', 'Ages'], t0=0, t1=1000, alpha=1):
		'''
		Initializes the GeoScale class.
		'''

		data_folder = Path('./assets/')
		data_file = data_folder / 'geo_time_scale.csv'

		self.df = pd.read_csv(data_file, sep=',', header=0)

		# Set the time boundaries to be plotted
		self.t0 = t0
		self.t1 = t1

		# Define figure and axis, and format
		self.fig, self.ax = plt.subplots(dpi=300)
		self.geo_format()

		# Plot eras
		if 'Eras' in divisions:
			self.plot_eras(alpha, cap_on=True, font_size=8, abbreviate=False)

		# Plot periods
		if 'Periods' in divisions:
			self.plot_periods(alpha, cap_on=True, font_size=7, abbreviate=False)

		# Plot epochs
		if 'Epochs' in divisions:
			self.plot_epochs(alpha, cap_on=True, font_size=6, abbreviate=False)

		# Plot ages
		if 'Ages' in divisions:
			self.plot_ages(alpha, cap_on=True, font_size=5, abbreviate=False)

	def geo_format(self):

		# Define heights for rectangles
		self.heights = {'Base': 2, 'Era': 10, 'Period': 15, 'Epoch': 20, 'Age': 25}

		# Format plot
		self.ax.axis([self.t0, self.t1, 0, 100])
		self.ax.spines['bottom'].set_color('gray')
		self.ax.spines['bottom'].set_linewidth(0.5)
		self.ax.tick_params(axis='x', colors='gray', width=0.5)
		self.ax.set_xlabel("Age (Ma)", color='gray')

		# Hide the y axis, right and top spines
		self.ax.get_yaxis().set_visible(False)
		self.ax.spines['left'].set_visible(False)
		self.ax.spines['top'].set_visible(False)
		self.ax.spines['right'].set_visible(False)

		self.fig.tight_layout()

	def plot_eras(self, alpha, cap_on=True, font_size=8, abbreviate=False):
		for era in self.df['Era'].unique():

			# Color lookup
			rec_color = self.df.loc[self.df['Era'] == era]['EraColor'].unique()[0]

			# Y axis settings
			y0 = self.heights['Base']
			y1 = self.heights['Era'] 
			height = y1 - y0

			# X axis settings
			x0 = self.df.loc[self.df['Era'] == era]['End'].min()
			x1 = self.df.loc[self.df['Era'] == era]['Begin'].max()

			self.filter_rectangles(x0, x1, y0, height, rec_color, era, cap_on, font_size, abbreviate, alpha)

	def plot_periods(self, alpha, cap_on=True, font_size=8, abbreviate=False):
		for period in self.df['Period'].unique():

			# Color lookup
			rec_color = self.df.loc[self.df['Period'] == period]['PeriodColor'].unique()[0]

			# Y axis settings
			y0 = self.heights['Era']
			y1 = self.heights['Period'] 
			height = y1 - y0

			# X axis settings
			x0 = self.df.loc[self.df['Period'] == period]['End'].min()
			x1 = self.df.loc[self.df['Period'] == period]['Begin'].max()

			self.filter_rectangles(x0, x1, y0, height, rec_color, period, cap_on, font_size, abbreviate, alpha)

	def plot_epochs(self, alpha, cap_on=True, font_size=8, abbreviate=False):

		for period in self.df['Period'].unique():
			for epoch in self.df.loc[self.df['Period'] == period]['Epoch'].unique():

				# Color lookup
				rec_color = self.df.loc[(self.df['Period'] == period) & (self.df['Epoch'] == epoch)]['EpochColor'].unique()[0]

				# Y axis settings
				y0 = self.heights['Period']
				y1 = self.heights['Epoch'] 
				height = y1 - y0

				# X axis settings
				x0 = self.df.loc[(self.df['Period'] == period) & (self.df['Epoch'] == epoch)]['End'].min()
				x1 = self.df.loc[(self.df['Period'] == period) & (self.df['Epoch'] == epoch)]['Begin'].max()

				self.filter_rectangles(x0, x1, y0, height, rec_color, epoch, cap_on, font_size, abbreviate, alpha)

	def plot_ages(self, alpha, cap_on=True, font_size=8, abbreviate=False):
		for age in self.df['Age'].unique():

			# Color lookup
			rec_color = self.df.loc[self.df['Age'] == age]['AgeColor'].unique()[0]

			# Y axis settings
			y0 = self.heights['Epoch']
			y1 = self.heights['Age'] 
			height = y1 - y0

			# X axis settings
			x0 = self.df.loc[self.df['Age'] == age]['End'].min()
			x1 = self.df.loc[self.df['Age'] == age]['Begin'].max()

			self.filter_rectangles(x0, x1, y0, height, rec_color, age, cap_on, font_size, abbreviate, alpha)

	def filter_rectangles(self, x0, x1, y0, height, rec_color, caption, cap_on, font_size, abbreviate, alpha):

			# Include part of the time interval if it overlaps with the time slice at the end (towards the present)
			if x0 <= self.t0 and x0 <= self.t1 and x1 >= self.t0 and x1 <= self.t1:

				width = x1 - self.t0

				self.plot_rectangle(self.t0, y0, width, height, rec_color, caption, cap_on, font_size, abbreviate, alpha)

			# Include the time interval if it is inside the time slice
			elif x0 >= self.t0 and x0 <= self.t1 and x1 >= self.t0 and x1 <= self.t1:

				width = x1 - x0

				self.plot_rectangle(x0, y0, width, height, rec_color, caption, cap_on, font_size, abbreviate, alpha)

			# Include part of the time interval if it overlaps with the time slice at the beginning (towards the past)
			elif x0 >= self.t0 and x0 <= self.t1 and x1 >= self.t0 and x1 >= self.t1:

				width = self.t1 - x0

				self.plot_rectangle(x0, y0, width, height, rec_color, caption, cap_on, font_size, abbreviate, alpha)

	def plot_rectangle(self, x, y, w, h, rec_color, caption, cap_on, font_size, abbreviate, alpha, font_color='black', line_color='black', line_width=0.5):

		# matplotlib.patches.Rectangle((xy), width, height, angle=0.0, **kwargs)
		rectangle = mpatch.Rectangle((x,y), w, h, facecolor=rec_color, edgecolor=line_color, linewidth=line_width, alpha=alpha, clip_on=False)

		# Add rectangle
		self.ax.add_artist(rectangle)

		if cap_on:
			# Add label
			cap_x = x + w / 2
			cap_y = y + h / 2

			# Create abbreviation
			if abbreviate:
				caption = caption[:3]

			self.ax.annotate(caption, (cap_x, cap_y), color=font_color, weight='normal', fontsize=font_size, ha='center', va='center')
