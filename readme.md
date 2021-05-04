# Exploring the Prosper Loan Dataset
## by Veris Pflüger-Prasarntree


## Dataset

This dataset contains data regarding loans made by Propser, a peer-to-peer lending marketplace in the United States. Since then, Prosper has facilitated more than 18 billion in loans to more than 1,080,000 people. Borrowers apply online for a fixed-rate, fixed-term loan between 2,000 and 40,000. Individuals and institutions can invest in the loans and earn attractive returns. Prosper handles all loan servicing on behalf of the matched borrowers and investors. 

There is approximately 113937 rows of loan records, with 113066 unique listings, and 81 columns of various datapoints for each loan.


## Summary of Findings

Nearly all loans seem to be funded given that the 25 percentile for the column PercentFunded is already at 1 and the average percent funded is 99.86 percent.

Reviewing statistical descriptions of the upper and lower range credit scores, and plotting both on a histogram, we can see that with the exception of a lower range of nearly zero, it would appear the lower range of most credit scores is somewhere in the 700, which is still high in general. And that the distributions between both are almost identical.

The average amount of investors of 80, however that likely skews due to certain listings that end up several hundred investors. The 50 percent cut off is 44 investors and over 30 percent of investors have fewer than 10 investors and even upward of 80 percent have fewer than 200.

Debt to Income ratio tended not to be very high. Its distribution skews to the right. By checking the values of where the 99th percentile of the ratio starts, filtering the loans data for all debt ratios above the 99th percentile and then looking at a quick description of that data, we can see that half of the top one percent is still only at a ratio of 1.6 where the max is 10. **DebtToIncomeRatio will likely be a relevant factor in our explanatory analysis of looking at what factors may be reliable to determine reliability of loan repayment.**

The distribution for Prosper Scores, scored from 1 to 10 (1 being most risky, 10 being lowest risk) seems to have normal distribution roughly divided in half. **ProsperScores, as a custom measure of risk, will also be relevant factor in our explanatory analysis.**

The distribtuion for EstimatedLoss skews right, with the mean (.08) only being slightly greater than the median (.07). **EstimatedLoss will be relevant to explanatory analysis of factors relevant to loan repayment.**

A good majority of the income range of borrowers is below 74,999 dollars while there is still a substantial number who have incomes above 100,000. **While this is an interesting facet, Income Range will likely play a minimal role in our explanatory evaluation.**

When looking at the proportions of each loan status, half the loans as of the dataset date are outstanding but current, a third were paid off, while the rest are are defaulted, charged off, or past due (all of which are non-payments of the loan). Cancelled and loans on Final Payment are near zero, e.g., the Cancelled rate is seen at five decimal places. **Loan Status will certainly play a significant role in how we drill into the dataset, letting us look at loans that are not current or loans that are defaulted/charged off.**

The income ranges and even higher level incomes of people who used Prosper was surprising, although the actual income range was consistent between the two variables. When looking at StatedMonthlyIncome, it was useful to transform the income amount to provide a more even view of the distribution.

The distribution of the DebtToIncomeRatio was oddly bimodal and was either very high or very low. While minimal feature engineering was performed, it may be necessary on the LoanStatus column to have all Past Due rows counted together.

Thinking it would be useful to see how accurate the Esitimated Loss was, I determined Actual Loss by dividing LP_GrossPrincipalLoss by LoanOriginalAmount for all entries where the status was Defaulted or Charged Off.

When looking at box and violin plots of StatedMonthlyIncome broken out by LoanStatus, the median and first and third percentiles of StatedMonthlyIncome for the various LoanStatus do not vary significantly excepf for those with the Final Payment in Progress. Indeed the StatedMonthlyIncome for those who completed their loans and those who are past due or defaulted are very similar.

Looking at EstimatedLoss by LoanStatus, EstimatedLoss was a bit higher in the unpaid loans versus the completed or about to be completed loans.

Here I compare estimated loss (Estimated loss is the estimated principal loss on charge-offs) and the Actual Loss Rate (calculated by LP_GrossPrincipalLoss by LoanOriginal amount). Using a scatterplot comparing Estimated Loss by Net Principal Loss (The principal that remains uncollected after any recoveries) isn't as clear as the Net Principal Loss could vary depending on the actual Loan Original Amount. While the comparison to Estimated Loss to Actual Loss is positive, the amount of high actual loss seems incredibly high across a range of Estimated Loss. 

While there is a positive correlation between Estimated Loss and the Debt to Income ratio, it does not seem impressively strong. Indeed we can see that there were both high and low estimated loss rate with a low debt to income ratio. Similarly there are low to mid levels of estimated loss at the highest debt to income ratio. While it appears interesting that there is no high estimated loss once the debt to income ratio passes 3, it is also good to know that there are not many loans with that high a ratio. Regardless of debt to income ratio, there does not seem to be an affect on the actual loss rate. The ability to pay off a loan is not strongly correlated to high debt, though for paid off debts, they tend to be lower on the debt range and there are more points of higher losses in high debts ratios.

When looking at StatedMonthlyIncome against EstimatedLoss, there is a very slight negative correlation, which stands to reason that the higher one's Started Monthly Income, the lower the Estimated Loss. Given that there are also datapoints of high Estimated Loss among the higher Stated Monthly Income, it seems almost certain that there are other factors besides income that are used to estimate loss.





## Key Insights for Presentation

> Select one or two main threads from your exploration to polish up for your presentation. Note any changes in design from your exploration step here.
