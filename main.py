#FOR TESTING PURPOSES
from summary_agent import summarize
from analysis_agent import analyze


query = input("What can I help you with?")

# Step 1: Summarize
summary_result = summarize(query)
print("SUMMARY:", summary_result.summary)

# Step 2: Analyze
analysis_result = analyze(summary_result.summary)
print("INSIGHTS:", analysis_result.insights)
