import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Interact():
	'''
	 Data class for interactive plotting comparative data.
	'''

	def __init__(self):
		'''
		Initializes the Data class.
		'''

	def boxplot(self, df):
		'''
		Creates a boxplot for comparative data.

		Args:
			df (pandas data frame): pandas data frame containing numeric (int, float) data.
		'''

		# Setup figure
		subplot_cols = len(df.columns)
		fig = make_subplots(rows=1, cols=subplot_cols)

		for i, col in enumerate(df):
			fig.add_trace(go.Box(
				y=df[col].values,
				name=col,
				boxpoints='outliers',
				text=df.index.values,
				hovertemplate=
				"<b>%{text}</b><br>" +
				"%{x}: %{y:,}" +
				"<extra></extra>",
				),
				row=1, col=i+1
				)

		# format the layout
		fig.update_layout(
			xaxis={'showgrid':False, 'zeroline':False},
			yaxis={ "gridcolor":'white', "zeroline":False},
			paper_bgcolor='white',
			plot_bgcolor='white',
			title_text='Box Plots for Continuous Traits',
			showlegend=True,
		)
		# Hide x-axis
		fig.update_xaxes(showticklabels=False)

		return fig


