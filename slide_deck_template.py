#!/usr/bin/env python
# coding: utf-8

# # (Presentation Title)
# ## by (your name here)

# ## Investigation Overview
# 
# > Describe the overall goals of your presentation here.
# 
# ## Dataset Overview
# 
# > Provide a brief overview of the dataset to be presented here.

# In[ ]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

get_ipython().run_line_magic('matplotlib', 'inline')

# suppress warnings from final output
import warnings
warnings.simplefilter("ignore")


# In[ ]:


# load in the dataset into a pandas dataframe
loans = pd.read_csv('engineered_loans_data.csv')


# > Note that the above cells have been set as "Skip"-type slides. That means
# that when the notebook is rendered as http slides, those cells won't show up.

# ## (Visualization 1)
# 
# > Write a comment about your visualization here. The visualization should be in
# the next cell, as a sub-slide type. Make sure your visualizations are polished!

# In[ ]:





# ## (Visualization 2)
# 
# > You should have at least three visualizations in your presentation,
# but feel free to add more if you'd like!

# In[ ]:

#facet bar plot with prosperscore and loanstatus

# Convert the "LoanStatus" column from a plain object type into an ordered categorical type
statuses = list(loans.LoanStatus.value_counts().index)
loan_statuses = pd.api.types.CategoricalDtype(ordered=False, categories=statuses)
loans['LoanStatus'] = loans['LoanStatus'].astype(loan_statuses)
score_order = list(loans.ProsperScore.value_counts().sort_index().index)

# Plot the Seaborn's FacetGrid
g = sns.FacetGrid(data = loans, col = 'LoanStatus', col_wrap=4, margin_titles = True)
g.map(sns.countplot, "ProsperScore", order=score_order);



# ## (Visualization 3)
# 
# 

# In[ ]:


g = sns.FacetGrid(data = loans.query('DebtToIncomeRatio < 1.67'), col = 'ProsperScore', col_wrap=4, margin_titles=True)
g.map(sns.regplot, 'DebtToIncomeRatio', 'ActualLossRate');


# > Once you're ready to finish your presentation, check your output by using
# nbconvert to export the notebook and set up a server for the slides. From the
# terminal or command line, use the following expression:
# > > `jupyter nbconvert <file_name>.ipynb --to slides --post serve --template output_toggle`
# 
# > This should open a tab in your web browser where you can scroll through your
# presentation. Sub-slides can be accessed by pressing 'down' when viewing its parent
# slide. Make sure you remove all of the quote-formatted guide notes like this one
# before you finish your presentation!

# In[ ]:




