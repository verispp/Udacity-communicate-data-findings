# Exploring the Prosper Loan Dataset
## by Veris Pflüger-Prasarntree


## Dataset

This dataset contains data regarding loans made by Propser, a peer-to-peer lending marketplace in the United States. Since then, Prosper has facilitated more than 18 billion in loans to more than 1,080,000 people. Borrowers apply online for a fixed-rate, fixed-term loan between 2,000 and 40,000. Individuals and institutions can invest in the loans and earn attractive returns. Prosper handles all loan servicing on behalf of the matched borrowers and investors. 

There is approximately 113937 rows of loan records, with 113066 unique listings, and 81 columns of various datapoints for each loan.


## Summary of Findings

> Summarize all of your findings from your exploration here, whether you plan on bringing them into your explanatory presentation or not.

Nearly all loans seem to be funded given that the 25 percentile for the column PercentFunded is already at 1 and the average percent funded is 99.86 percent.

Reviewing statistical descriptions of the upper and lower range credit scores, and plotting both on a histogram, we can see that with the exception of a lower range of nearly zero, it would appear the lower range of most credit scores is somewhere in the 700, which is still high in general. And that the distributions between both are almost identical.

The average amount of investors of 80, however that likely skews due to certain listings that end up several hundred investors. The 50 percent cut off is 44 investors and over 30 percent of investors have fewer than 10 investors and even upward of 80 percent have fewer than 200.

Debt to Income ratio tended not to be very high. Its distribution skews to the right. By checking the values of where the 99th percentile of the ratio starts, filtering the loans data for all debt ratios above the 99th percentile and then looking at a quick description of that data, we can see that half of the top one percent is still only at a ratio of 1.6 where the max is 10. **DebtToIncomeRatio will likely be a relevant factor in our explanatory analysis of looking at what factors may be reliable to determine reliability of loan repayment.**

The distribution for Prosper Scores, scored from 1 to 10 (1 being most risky, 10 being lowest risk) seems to have normal distribution roughly divided in half. **ProsperScores, as a custom measure of risk, will also be relevant factor in our explanatory analysis.**

The distribtuion for EstimatedLoss skews right, with the mean (.08) only being slightly greater than the median (.07). **EstimatedLoss will be relevant to explanatory analysis of factors relevant to loan repayment.**




## Key Insights for Presentation

> Select one or two main threads from your exploration to polish up for your presentation. Note any changes in design from your exploration step here.
