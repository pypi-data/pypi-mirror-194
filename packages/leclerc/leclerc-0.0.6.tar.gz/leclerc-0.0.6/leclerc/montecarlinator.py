# Heavily derived from https://towardsdatascience.com/python-scenario-analysis-modeling-expert-estimates-with-the-beta-pert-distribution-22a5e90cfa79

from leclerc.pert import pertm_gen
from scipy.stats import qmc    # quasi-Monte Carlo for latin hypercube sampling
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show

N = 10000
plots = []

class PERT:
	def __init__(self, min, mode, max, label, lmb=4):
		self.min = min
		self.mode = mode
		self.max = max
		self.lmb = lmb
		self.label = label
		# instantiate a PERT object and print stats
		self.pertm = pertm_gen(name="pertm")
		self.rvP = self.pertm(min,mode,max,lmb)
		self.statsP = self.rvP.stats("mvsk")

	def print_stats(self):
		# Get properties of PERT distribution and print.
		moments = [np.ndarray.item(v) for v in self.statsP]
		moment_names = ["mean", "var", "skew", "kurt"]
		dict_moments = dict(zip(moment_names, moments))
		_ = [print(k,":",f'{v:.2f}') for k,v in dict_moments.items()]
	
	def generate_random_samples(self, num_samples):
		# Generate N random samples and print. 
		sampler01 = qmc.LatinHypercube(d=1, seed=42)    # d = dimension
		sample01 = sampler01.random(n=num_samples)
		# Generate array of random samples from the distribution
		randP = self.rvP.ppf(sample01)
		return randP
	
	# THIS FOR EACH PERT
	def create_pdf_plot(self):
		# Show probability density function
		TOOLTIPS = [("x", "$x"), ("y", "$y")]
		p = figure(width=400, height=400, toolbar_location=None, title=self.label, tooltips=TOOLTIPS)
		curdoc().theme = 'light_minimal'
		x = np.linspace(self.rvP.ppf(0.000001), self.rvP.ppf(0.999999), 100)
		p.line(x, self.rvP.pdf(x), line_width=2, line_color="orange", legend_label="PERT random samples")
		p.xaxis.axis_label = self.label
		p.yaxis.axis_label = "PDF"
		plots.append(p)
	
def create_histogram(calculation, name, result):
	# Show a histogram of the distribution
	TOOLTIPS = [("x", "$x"), ("y", "$y")]
	title = ("Distribution of " + calculation + " Samples")
	p = figure(width=800, height=800, toolbar_location=None, title=title, tooltips=TOOLTIPS)
	bins = np.linspace(min(result), max(result), 100)
	curdoc().theme = 'light_minimal'
	hist, edges = np.histogram(result, bins=bins)
	p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
			fill_color="orange", line_color="white",
			legend_label="Sample")
	p.yaxis.axis_label = "Frequency"
	p.xaxis.axis_label = name
	plots.append(p)

	
def pert_monte_carlo(func):
	def wrapper_pert_monte_carlo(*args, **kwargs):
		dists = []
		calculation = args[0]
		name = args[1]
		j = 0
		for a in args:
			if isinstance(a, PERT):
				# a.print_stats()
				samples = a.generate_random_samples(N)
				dists.append(samples)
				a.create_pdf_plot()
				j+=1
			else:
				dists.append([[a] for i in range(N)])
			
		# For every set of Monte Carlo picks, run the original function
		results = []
		for i in range(N):
			new_args = [d[i][0] for d in dists]
			result = func(*new_args)
			results.append(result)
		create_histogram(calculation, name, results)
		show(gridplot([plots], toolbar_location="below"))
		return results
	return wrapper_pert_monte_carlo
