#!/usr/bin/env python
# coding: utf-8

# # (Prosper Loan Exploration Title)
# ## by Veris Pflueger-Prasarntree
# 
# ## Preliminary Wrangling
# 
# > Briefly introduce your dataset here. This dataset contains data regarding loans made by Propser, a peer-to-peer lending marketplace in the United States. Since then, Prosper has facilitated more than 18 billion in loans to more than 1,080,000 people. TBorrowers apply online for a fixed-rate, fixed-term loan between 2,000 and 40,000. Individuals and institutions can invest in the loans and earn attractive returns. Prosper handles all loan servicing on behalf of the matched borrowers and investors. 

# In[2]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# > Load in your dataset and describe its properties through the questions below.
# Try and motivate your exploration goals through this section.

# In[3]:


loans = pd.read_csv('prosperLoanData.csv')

loans.sample(5)


# In[4]:


loans.info()


# In[5]:


loans.describe().iloc[:,:20]


# In[6]:


loans.describe().iloc[:,20:40]


# In[7]:


loans.describe().iloc[:,40:61]


# In[8]:


loans.shape


# In[9]:


loans.ListingNumber.value_counts()


# In[10]:


len(loans.ListingKey.value_counts())


# ### What is the structure of your dataset?
# 
# > There are approximately 113,937 rows of data and 81 columns. After checking the length of a list unique Listing Number, it would appear there are 113,066 unique records, as some Listing Numbers have multiple records.
# 
# ### What is/are the main feature(s) of interest in your dataset?
# 
# > ProsperScore, ProsperRating, LoanCurrentDaysDeliquent, EstimatedLoss, and the income related columns, IncomeRange
# IncomeVerifiable, StatedMonthlyIncome
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# 
# > LoanStatus will definitely be of assistance as it will help divide the data in those who were able to pay off the loan and those who could not pay off the loan.

# ## Univariate Exploration
# 
# > In this section, investigate distributions of individual variables. If
# you see unusual points or outliers, take a deeper look to clean things up
# and prepare yourself to look at relationships between variables.

# What is the distribution of PercentFunded just to give an idea of how effective Prosper is.

# In[11]:


loans.PercentFunded.describe()


# Assuming that 1 means 100 percent funded, most seem to be funded given that the 25 percentile is already at 1 and the average percent funded is 99.86 percent.

# In[12]:


plt.hist(data=loans, x='PercentFunded')


# What about the upper and lower range of the credit scores of those who apply for loans via Prosper?

# In[13]:


loans.CreditScoreRangeLower.describe()


# In[14]:


loans.CreditScoreRangeUpper.describe()
#np.arange(0, 1, .1)


# In[15]:


bins = np.arange(0, 900, 20)
plt.hist(data=loans, x='CreditScoreRangeLower', bins=bins, alpha=0.5, label='Lower Range', color='orange')
plt.hist(data=loans, x='CreditScoreRangeUpper', bins=bins, alpha=0.5, label='Upper Range', color='blue')
ticks = np.arange(0, 900, 50)
labels = ['{}'.format(x) for x in ticks]
plt.xticks(ticks, labels, rotation=70);


# Reviewing statistical descriptions of the upper and lower range credit scores, and plotting both on a histogram, we can see that with the exception of a lower range of nearly zero, it would appear the lower range of most credit scores is somewhere in the 700, which is still high in general. And that the distributions between both are almost identical.

# In[16]:


print(loans.Investors.describe(np.arange(0,1,.1)))
plt.hist(data=loans, x='Investors')
plt.yscale('log')
plt.xlabel('Investors')
plt.minorticks_off()


# The average amount of investors of 80, however that likely skews due to certain listings that end up several hundred investors. The 50 percent cut off is 44 investors and over 30 percent of investors have fewer than 10 investors and even upward of 80 percent have fewer than 200.

# In[78]:


#DebtToIncomeRatio

#print(np.log10(loans.DebtToIncomeRatio.describe()))
#print(loans.DebtToIncomeRatio.describe(np.arange(.9,1, .01)))

debt_bins = 10 ** np.arange(-1, 1, .3)
#print(debt_bins)

debt_ticks = [.1, .2, .5, 1, 2, 5, 11]
debt_labels = ['{}'.format(v) for v in debt_ticks]

plt.hist(data=loans, x='DebtToIncomeRatio', bins=debt_bins)
plt.xscale('log')
plt.yscale('log')
plt.minorticks_off()
plt.yticks([100, 1000, 10000], [100, 1000, 10000])
plt.xticks(debt_ticks, debt_labels);
#plt.yticks(debt_ticks, debt_labels);


# In[76]:


print(loans.DebtToIncomeRatio.describe())
loans.query('DebtToIncomeRatio > .86')[['DebtToIncomeRatio']].describe()


# Debt to Income ratio tended not to be very high and is also oddly bimodal. 
# 
# Without any kind of transfomation on the y axis, the chart skews heavily. 
# 
# After applying logarithmic transformations on both axes, the distribution still skews to the right. By checking the values of where the 99th percentile of the dataset starts, filtering the loans data for all debt ratios above the 99th percentile and then looking at a quick description of that data, we can see that half of the top one percent is still only at a ratio of 1.6 where the max is 10.

# In[18]:


plt.hist(data=loans, x='ProsperScore');
loans.ProsperScore.describe()


# The distribution for Prosper Scores, scored from 1 to 10 (1 being most risky, 10 being lowest risk) seems to have normal distribution roughly divided in half.

# In[19]:


plt.hist(data=loans, x='EstimatedLoss')
loans.EstimatedLoss.describe()


# Definitely a right skew on the distribution, with the mean (.08) only being slightly greater than the median (.07).

# In[91]:


unpaid.query('PercentFunded < 1')[['PercentFunded','LP_CustomerPayments','LP_CustomerPrincipalPayments','LP_GrossPrincipalLoss','LoanOriginalAmount','LoanStatus']].sample(10)

# LoanOriginalAmount * PercentFunded - LP_CustomerPrincipalPayments = LP_GrossPrincipalLoss
# Actual Loss = LP_GrossPrincipalLoss / LoanOriginalAmount


# It may be useful to have a row indicating actual loss to be able to compare with estimated loss, among other variables. This column can be populated by dividing LP Gross Principal Loss by Loan Original Amount for every loan that has a Loan Status of ChargedOff or Defaulted. Due to definitions of Past Due, loans that are past due do not have a listed LP Gross Principal Loss.

# In[97]:


loans['ActualLossRate'] = loans.apply(lambda x: x['LP_GrossPrincipalLoss']/x['LoanOriginalAmount'] 
                                      if x['LoanStatus'] in ['Chargedoff','Defaulted'] else np.nan, axis=1)

loans.query('LoanStatus == "Defaulted" or LoanStatus == "Chargedoff"')[['ActualLossRate']].sample(5)


# In[20]:


#IncomeRange
#IncomeVerifiable
#StatedMonthlyIncome

loans.IncomeRange.describe()
print(loans.IncomeRange.value_counts())
order=['Not displayed','Not employed', '$0','$1-24,999','$25,000-49,999', '$50,000-74,999','$75,000-99,999',
       '$100,000+']
base_c = sns.color_palette()[0]
sns.countplot(data=loans, x="IncomeRange", order=order, color=base_c)
plt.xticks(rotation=45, ha='right')
("")


# A good majority of the income range of borrowers is below 74,999 dollars while there is still a substantial number who have incomes above 100,000.

# In[21]:


loans.IncomeVerifiable.value_counts()


# Though some of the Incomes are verifiable and therefore it may be useful to sceen for loans whose borrowers had verifiable income.

# In[22]:


loans.StatedMonthlyIncome.describe().round(3)


# In[23]:


sns.histplot(data=loans, x='StatedMonthlyIncome');


# There is likely a large skew here due to high incomes. Removing the highest incomes will likely give a better idea of the distribution of stated monthly income.

# In[24]:


upper_percentile = loans.StatedMonthlyIncome.describe(np.arange(0,1,.01)).round(3).loc['99%']

no_one_percenters = loans[loans['StatedMonthlyIncome'] < upper_percentile]

print(np.log10(no_one_percenters.StatedMonthlyIncome.describe()))

plt.figure(figsize=(12,8))
bins = 10 ** np.arange(0, 4.3+0.1, 0.1)
sns.histplot(data=no_one_percenters, x='StatedMonthlyIncome', bins=bins)

# Generate the x-ticks you want to apply
ticks = [1, 100, 500, 1000, 2500, 5000, 10000, 21000]
# Convert ticks into string values, to be displaye dlong the x-axis
labels = ['{}'.format(v) for v in ticks]

plt.xscale('log')
plt.minorticks_off()
plt.xticks(ticks, labels, rotation=40)
("")


# This gives us a better distribution and which stated monthly income is the average, after excluding the top 1 percent.

# Let's take an initial look at the LoanStatus column, which contains the current status of the loan: Cancelled,  Chargedoff, Completed, Current, Defaulted, FinalPaymentInProgress, PastDue (The PastDue status will be accompanied by a delinquency bucket) in terms of relative frequencies, to see the distribution of the different statuses. 

# In[25]:


#bar chart of LoanStatus
status_counts = loans.LoanStatus.value_counts()
n_status = status_counts.sum()

max_status = status_counts[0]

max_prop = max_status / n_status

tick_props = np.arange(0, max_prop, 0.02)
tick_names = ['{:0.2f}'.format(v) for v in tick_props]

base_color = sns.color_palette()[0]
status_order = status_counts.index

sns.countplot(data=loans, y='LoanStatus', color=base_color, order=status_order);

# Change the tick locations and labels
plt.xticks(tick_props * n_status, tick_names, rotation=35)
plt.xlabel('proportion')

for i in range (status_counts.shape[0]):
    # Remember, type_counts contains the frequency of unique values in the `type` column in decreasing order.
    count = status_counts[i]
    # Convert count into a percentage, and then into string
    pct_string = '{:0.1f}'.format(100*count/n_status)
    # Print the string value on the bar. 
    # Read more about the arguments of text() function [here](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.text.html)
    plt.text(count+1, i, pct_string, va='center');


# As indicated in the variable definitions, Past Due rows are separated out and binned. It will likely be useful to collapse those into one variable and move the bins to a separate column. This is to get a sense of how many are Past Due without regard to how overdue they are. 

# In[26]:


status_counts = loans.LoanStatus.value_counts()
past_due = 0

for i, v in status_counts.iteritems():
    if 'Past Due' in i:
        past_due += v

status_counts['Past Due'] = past_due
new_status_counts = status_counts[['Cancelled', 'Chargedoff', 'Completed', 'Current', 'Defaulted', 'FinalPaymentInProgress', 'Past Due']]

total = new_status_counts.sum()
n_status = new_status_counts

prop_status_counts = new_status_counts.apply(lambda x: round(x/total, 3))
prop_status_counts.sort_values(ascending=False, inplace=True)

base_color = sns.color_palette()[0]

plt.figure(figsize=(11,8))
sns.barplot(x = prop_status_counts.values, y = prop_status_counts.index, order=prop_status_counts.index,
            color=base_color)

for i in range (prop_status_counts.shape[0]):
    # Remember, type_counts contains the frequency of unique values in the `type` column in decreasing order.
    count = prop_status_counts[i]
    # Convert count into a percentage, and then into string
    pct_string = '{:0.2f}'.format(count)
    # Print the string value on the bar. 
    # Read more about the arguments of text() function [here](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.text.html)
    plt.text(count+0.0005, i, pct_string, va='top');


# This bar plot of the proportions of each loan status shows that half the loans as of the dataset date are outstanding, a third were paid off, while the rest are are defaulted, charged off, or past due (all of which are non-payments of the loan). While the bottom two percentages are zero, this is due to rounding to two decimal places, e.g., the Cancelled rate is seen at five decimal places.
# 
# For further explanatory analysis, we can likely separate the loans data into three dataframes for Current, Completed / Final Payment In Progress, and Charged Off / Defaulted / Past Due

# In[27]:


loans.LoanStatus.value_counts()


# In[28]:


completed = loans.query("LoanStatus == 'Completed' or LoanStatus == 'FinalPaymentInProgress'")
current = loans[loans['LoanStatus'] == 'Current']
unpaid = loans.query("LoanStatus.str.contains('Past Due') or LoanStatus == 'Defaulted' or LoanStatus == 'Chargedoff'", 
                     engine='python')


# After creating the three separate dataframes, a quick spot check to ensure each are correct.

# In[29]:


unpaid.sample(10)


# In[30]:


unpaid.shape


# In[31]:


current.head()


# In[32]:


current.shape


# In[33]:


completed.sample(7)


# In[34]:


completed.shape


# Let's start on the unpaid dataset to get an idea of people who default on their loans.

# In[35]:


unpaid[["ListingKey", "AmountDelinquent", "CreditScoreRangeLower", "CreditScoreRangeUpper", "DebtToIncomeRatio"]]


# Feature engineering to clean up the LoanStatus column so that all Past Due loans are now under one value. The past due day bins are moved to a second column.

# In[36]:


#backing up loans dataset
loans_c = loans.copy()

#putting the past due bin day groups into a separate column in case the value is later needed
loans['PastDueBin'] = loans['LoanStatus'].apply(lambda x: x.split("(")[1][:-1] if len(x.split("(")) > 1 else np.nan)

#removing the past due bin day groups from the LoanStatus column
loans['LoanStatus'] = loans['LoanStatus'].apply(lambda x: x.split("(")[0].strip())

loans.LoanStatus.value_counts()


# > Make sure that, after every plot or related series of plots, that you
# include a Markdown cell with comments about what you observed, and what
# you plan on investigating next.

# ### Discuss the distribution(s) of your variable(s) of interest. Were there any unusual points? Did you need to perform any transformations?
# 
# The income ranges and even higher level incomes of people who used Prosper was surprising, although the actual income range was consistent between the two variables. When looking at StatedMonthlyIncome, it was useful to transform the income amount to provide a more even view of the distribution.
# 
# ### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?
# 
# The DebtToIncome ratio was oddly bimodal and was either very high or very low. While minimal feature engineering was performed, it may be necessary on the LoanStatus column to have all Past Due rows counted together.
# 
# Thinking it would be useful to see how accurate the Esitimated Loss was, I determined Actual Loss by dividing LP_GrossPrincipalLoss by LoanOriginalAmount for all entries where the status was Defaulted or Charged Off.

# ## Bivariate Exploration
# 
# > In this section, investigate relationships between pairs of variables in your
# data. Make sure the variables that you cover here have been introduced in some
# fashion in the previous section (univariate exploration).

# In[37]:


print(np.log10(loans.StatedMonthlyIncome.describe()))


# In[38]:


# apply Loanstatus (categorical) to StatedMonthlyIncome(discrete numerical)

plt.figure(figsize = [14, 5])

plt.subplot(1, 2, 1)
sns.violinplot(data=loans, x='LoanStatus', y='StatedMonthlyIncome', color=base_c, inner='quartile')
plt.xticks(rotation=35)
plt.yscale('log')

plt.subplot(1, 2, 2)
sns.boxplot(data=loans, x='LoanStatus', y='StatedMonthlyIncome', color=base_c)
plt.xticks(rotation=35)
plt.yscale('log');


# Here we can se that the median and first and third percentiles of StatedMonthlyIncome for the various loan statuses do not vary significantly excepf for those with the Final Payment in Progress. Indeed the StatedMonthlyIncome for those who completed their loans and those who are past due or defaulted are almost the same.

# In[39]:


loans.EstimatedLoss.describe()


# In[40]:


#violin plot of Estimated Loss and Loan Status

sns.violinplot(data=loans, x='LoanStatus', y='EstimatedLoss', color=base_c, innter='quartile')
plt.xticks(rotation=35, ha='right');


# Estimated Loss was a bit higher in the unpaid loans versus the completed or about to be completed loans.

# Here I compare estimated loss (Estimated loss is the estimated principal loss on charge-offs)  and the Actual Loss Rate (calculated by LP_GrossPrincipalLoss by LoanOriginal amount). Using a scatterplot comparing Estimated Loss by Net Principal Loss (The principal that remains uncollected after any recoveries) isn't as clear as the Net Principal Loss could vary depending on the actual Loan Original Amount.

# In[99]:


#scatter plot and regression line for Estimated Loss and Actual Loss Rate
plt.figure(figsize = [7, 5])
sns.regplot(data=loans, x='EstimatedLoss', y="ActualLossRate");


# In[101]:


loans.query("ActualLossRate > .8").ActualLossRate.describe()


# While the comparison to Estimated Loss to Actual Loss is positive, the amount of high actual loss seems incredibly high across a range of Estiamted Loss. 

# In[43]:


#scatter plot debttoincomeratio and estimated loss

plt.figure(figsize = [7, 5])
sns.regplot(data=loans, x='DebtToIncomeRatio', y='EstimatedLoss')
plt.xlim(right=11)


# While there is a positive correlation between Estimated Loss and the Debt to Income ratio, it does not seem impressively strong. Indeed we can see that there were both high and low estimated loss rate with a low debt to income ratio. Similarly there are low to mid levels of estimated loss at the highest debt to income ratio. While it appears interesting that there is no high estimated loss once the debt to income ratio passes 3, it is also good to know that there are not many loans with that high a ratio.

# In[105]:


#scatter plot of stated monthly income and estimated loss

plt.figure(figsize = [8,5])
sns.regplot(data=no_one_percenters, x='StatedMonthlyIncome', y='EstimatedLoss')
#plt.xlim(right=.4);


# The chart is very sparse and that is likely due to the outlier of the very high income. By removing the top 1 percent of StatedMonthlyIncome we see a much larger chart.

# The regression line is almost lost among the data points, but it shows a slight negative correlation, which stands to reason that the higher one's Started Monthly Income, the lower the Estimated Loss.

# Given that there are also datapoints of high Estimated Loss among the higher Stated Monthly Income, it seems almost certain that there are other factors besides income that are used to estimate loss.

#clustered bar chart with prosperscore and borrower rate
# average rate per prosperscore?
# or hist plot with prosperscore

print(loans.BorrowerRate.describe())

#step 2 chart initial to see if log transformation of borrower rate makes sense

g = sns.FacetGrid(data = loans, col = 'ProsperScore', col_wrap=4, margin_titles=True)
g.map(plt.hist, "BorrowerRate");

# We can see as the Prosper Score goes up, the skewing shifts initially from a left skew to a rightward skew, indicating generally that the lower scores have higher Borrower Rates, suggesting higher risk, and high prosper scores have lower Borrower Rates, suggesting lower risk.
g = sns.FacetGrid(data = loans, col = 'ProsperScore', col_wrap=4, margin_titles=True)
g.map(plt.hist, "EstimatedLoss");

g = sns.FacetGrid(data = loans, col = 'ProsperScore', col_wrap=4, margin_titles=True)
g.map(plt.hist, "ActualLossRate");

list(loans.LoanStatus.value_counts().index)

score_order = list(loans.ProsperScore.value_counts().sort_index().index)

#facet bar plot with prosperscore and loanstatus

# Convert the "LoanStatus" column from a plain object type into an ordered categorical type
statuses = list(loans.LoanStatus.value_counts().index)
loan_statuses = pd.api.types.CategoricalDtype(ordered=False, categories=statuses)
loans['LoanStatus'] = loans['LoanStatus'].astype(loan_statuses);

# Plot the Seaborn's FacetGrid
g = sns.FacetGrid(data = loans, col = 'LoanStatus', col_wrap=4, margin_titles = True)
g.map(sns.countplot, "ProsperScore", order=score_order);

"""(x = prop_status_counts.values, y = prop_status_counts.index, order=prop_status_counts.index,
            color=base_color)"""

'''g.map(sns.barplot, 'interval', 'value', order=times)'''

g = sns.FacetGrid(data = loans.query('DebtToIncomeRatio < 1.67'), col = 'ProsperScore', col_wrap=4, margin_titles=True)
g.map(plt.hist, "DebtToIncomeRatio");

# When looking at the PropserScore across each Loan type, the distribution appears normal and it does not seem like any one or range of ProsperScores is more represented in Past Due or Defaulted loans.

# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# 
# > Your answer here!
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# > Your answer here!

# ## Multivariate Exploration
# 
# > Create plots of three or more variables to investigate your data even
# further. Make sure that your investigations are justified, and follow from
# your work in the previous sections.

#variables used above:

#Numerical

    '''Actual Loss Rate
    Estimated Loss
    Stated Monthly Income
    Borrower Rate
    Debt to Income Ratio

Qualitative

    Loan Status
    Prosper Score
    Income Range

Possible ideas for visualizations: scatter plot debttoincomeratio and estimated loss with loan status category borrower rate hist plot divided by prosperscore with estimated loss?

As Actual Loss Rate only exists for loans that have defaulted, it should not be used with LoanStatus to ensure no empty graphs'''

# debttoincomeratio, estimated loss numerical

# loan status category 

# two numerical variables and a category means we can use a facet grid with scatter plots

g = sns.FacetGrid(data = loans, col = 'LoanStatus', col_wrap=4, margin_titles=True)

g.map(sns.regplot, 'DebtToIncomeRatio', 'EstimatedLoss');

#In looking at scatter plots to see How Debt To Income Ratio correlates to Estimated Loss broken out by Loan Status (essentially to see how well the debt to income ratio affected estimated loss and how each loan subsequently fared), the scatter plots are quite large, as the ratio goes out to 10. Recalling from the univariate analysis of Debt to Income Ratio, we saw that even the upper 99% of .86 and that even half of the top 1% was only 1.67. We can exclude the outliers beyond 1.67 percent and perhaps see a more reasonable plot.

g = sns.FacetGrid(data = loans.query('DebtToIncomeRatio < 1.67'), col = 'LoanStatus', col_wrap=4, margin_titles=True)

g.map(sns.regplot, 'DebtToIncomeRatio', 'EstimatedLoss');

#After removing outlier debt to income ratios, the scatter plots are more clear and the actual correlations are clearly not significant and that the debt to income ratio has no strong correlations despite the borrower's ability to pay off the loan. We do not see much difference between the debt to income ratio and the estimated loss for charged off or defaulted loans versus current or nearly paid off loans in terms correlation between the two variables.

g = sns.FacetGrid(data = no_one_percenters, col = 'LoanStatus', col_wrap=4, margin_titles=True)

g.map(sns.regplot, 'StatedMonthlyIncome', 'EstimatedLoss');

#A negative correlation betwen Stated Monthly Income and Estimated Loss is reasonable as the higher the Stated Monthly Income, the more likely the borrower has the capability to pay the loan and the lower the Estimated Loss. It is also reasonable that this correlation is simlar despite the actual disposition of the loan, suggesting that the Stated Monthly Income and the Estimated Loss is not necessarily indicators of whether a loan may be repaid.

g = sns.FacetGrid(data = loans.query('DebtToIncomeRatio < 1.67'), col = 'ProsperScore', col_wrap=4, margin_titles=True)

g.map(sns.regplot, 'DebtToIncomeRatio', 'ActualLossRate');

#Here rather than see the estimated loss, we can look at the Actual Loss Rate and compare it to the Debt to Income Ratio for each level of Prosper Score, a custom risk score. One aspect that can be immediately observed is that the correlation between the Debt to Income Ratio and the Actual Loss Rate goes from neutral with lower Propser Scores and turns negative with the high end of Prosper Scores, from 8 onward. This suggests the Prosper Score has viability in determining whether the loan may be paid back.

#For Prosper Scores 8 to 10, even as the Debt to Income Ratio increased, the Actual Loss Rate did not increase. Unlike the Prosper Scores 1 to 3, where even with low Debt to Income Ratios, the Actual Loss Rates are generally still high. Though the correlation is neutral, we can see the concentration of data points is focused in high Actual Loss Rates even for low Debt to Income Ratios. As the Prosper Score increases, we see more data points in the low end of Actual Loss Rates, even as the correlation stays neutral.

# income range with estimated loss rate and actual loss rate

g = sns.FacetGrid(data = no_one_percenters, col = 'IncomeRange', col_wrap=4, margin_titles=True)

g.map(sns.regplot, 'ActualLossRate', 'EstimatedLoss');

#In looking at the Actual Loss Rate for Estimated Loss, it's clear there's no correlation at all. Regardless of the income, the estimated loss had no bearing on the 
#actual loss.
#Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your 
#feature(s) of interest?

#Very little. Prosper Score was the only factor that bore an interesting correlation that could be best seen in a multi-variate analysis comparing against Debt to 
#Income Ratio and Actual Loss Rate. Many other factors that would potentially be relevant turned out not to be relevant at all.
#Were there any interesting or surprising interactions between features?

#What could be considered surprising is how irrelevant factors like Debt to Income Ratio or income was to determine someone's ability to pay off loans.

# > At the end of your report, make sure that you export the notebook as an
# html file from the `File > Download as... > HTML` menu. Make sure you keep
# track of where the exported file goes, so you can put it in the same folder
# as this notebook for project submission. Also, make sure you remove all of
# the quote-formatted guide notes like this one before you finish your report!

# In[ ]:




