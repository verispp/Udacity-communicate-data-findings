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

Lookng at the BorrowerRate across the various Prosper Scores, we can see as the Prosper Score goes up, the skewing shifts initially from a left skew to a rightward skew, indicating generally that the lower scores have higher Borrower Rates, suggesting higher risk, and high prosper scores have lower Borrower Rates, suggesting lower risk. 

When looking at Prosper Scores against the Loan Status though, the distribution appears normal and it does not seem like any one or range of ProsperScores is more represented in Past Due or Defaulted loans.

In looking at scatter plots to see how Debt To Income Ratio correlates to Estimated Loss broken out by Loan Status (essentially to see how well the debt to income ratio affected estimated loss and how each loan subsequently fared), the scatter plots are quite large, as the ratio goes out to 10. Recalling from the univariate analysis of Debt to Income Ratio, we saw that even the upper 99% of .86 and that even half of the top 1% was only 1.67. We can exclude the outliers beyond 1.67 percent and perhaps see a more reasonable plot. After removing outlier debt to income ratios, the scatter plots are more clear and the actual correlations are clearly not significant and that the debt to income ratio has no strong correlations despite the borrower's ability to pay off the loan. We do not see much difference between the debt to income ratio and the estimated loss for charged off or defaulted loans versus current or nearly paid off loans in terms correlation between the two variables.

A negative correlation betwen Stated Monthly Income and Estimated Loss is reasonable as the higher the Stated Monthly Income, the more likely the borrower has the capability to pay the loan and the lower the Estimated Loss. It is also reasonable that this correlation is simlar despite the actual disposition of the loan, suggesting that the Stated Monthly Income and the Estimated Loss is not necessarily indicators of whether a loan may be repaid.

Here rather than see the estimated loss, we can look at the Actual Loss Rate and compare it to the Debt to Income Ratio for each level of Prosper Score, a custom risk score. One aspect that can be immediately observed is that the correlation between the Debt to Income Ratio and the Actual Loss Rate goes from neutral with lower Propser Scores and turns negative with the high end of Prosper Scores, from 8 onward. This suggests the Prosper Score has viability in determining whether the loan may be paid back.

For Prosper Scores 8 to 10, even as the Debt to Income Ratio increased, the Actual Loss Rate did not increase. Unlike the Prosper Scores 1 to 3, where even with low Debt to Income Ratios, the Actual Loss Rates are generally still high. Though the correlation is neutral, we can see the concentration of data points is focused in high Actual Loss Rates even for low Debt to Income Ratios. As the Prosper Score increases, we see more data points in the low end of Actual Loss Rates, even as the correlation stays neutral.

In looking at the Actual Loss Rate for Estimated Loss, it's clear there's no correlation at all. Regardless of the income, the estimated loss had no bearing on the actual loss.
