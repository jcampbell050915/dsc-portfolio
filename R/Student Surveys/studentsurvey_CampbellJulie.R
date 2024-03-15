# Assignment: Exercise 7.2 Exercise 7
# Name: Campbell, Julie
# Date: 2022-10-11

## Load the ggplot2 package
library(ggplot2)
library(qqplotr)
library(ggm)
theme_set(theme_minimal())



# covariance of survey variables
# measure of the relationship between variables
# Positive covariance indicates that the two variables deviate in the same direction
# TimeTV & Happiness, TimeTV & Gender, Happiness & Gender
# Negative covariance indicates that the two variables deviate in different directions
# TimeTV & Time Reading, TimeReading & Happiness, TimeReading & Gender

cov(student_df)


# What measurement is being used? How would it change covariance calculation
#TimeTV and Happiness 1-100
#Time Reading Hours
#Gender 0, 1 (Female & Male)
#covariance is not a standardized measure, cannot compare in an objective way, both data sets need to be measure in the same units

# Choose correlation test, explain why, predict (positive or negative)
# Pearson's correlation coefficient
cor(student_df)

ggplot(student_df, aes(sample = TimeReading)) + 
  stat_qq_point(size = 2,color = "red") + 
  stat_qq_line(color="green")

# Correlation analysis of:
# All variables
cor(student_df, method = "pearson")
# As single correlation between two a pair of variables
cor.test(student_df$TimeTV, student_df$TimeReading, method = "pearson")
# Repeat your correlation test in step 2 but set the confident at 99%
cor.test(student_df$TimeTV, student_df$TimeReading, method = "pearson", conf.level = 0.99)
# Describe the relationship


# Calculate correlation coefficient and coefficient of determination
cor(student_df)^2

# Does more TV cause less reading? Explain
# Yes, they have a negative relationship

# Pick three variables and perform a partial correlation, documenting which variable 
# you are “controlling”. Explain how this changes your interpretation and 
# explanation of the results.

pcor(c("TimeTV","TimeReading","Gender"), var(student_df))
