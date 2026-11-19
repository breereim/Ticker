# Locked Changed-Input Record — complete without AI before the run


## Before the run — commit and push this section first

Decision date and time:11/19/26 1:26pm
Base app version / GitHub commit:https://github.com/breereim/Ticker/commit/5af0f53e3a8b294636eb15d911fc61feee596e6e
Exact input to change, from → to:Annual fund fee (basis points): 10 -> 20
My AI-off prediction of weights, net estimate, volatility, and mandate verdict: I think the weights will increase, the net estimate will go down, the volatility will stay the same, and the mandate verdict may change to yes.
My reasoning: I think the weights will increase because now they are worth more, the net estimate will be less because you are paying higher fees on them, I think the volatility stays the same because fees don't affect volatility, and the mandate verdict may change because you earn more on the investments.
Prediction commit permalink (add after push, before the run):


## After the run — add in a later commit

Run date and time: 11/19/26 1:54pm
Actual weights, net estimate, volatility, and mandate verdict: The actual weights stayed the same for everything other than the constrained lowest volatility portfolio. The BIL and IEF funds stayed the same however the LQD decreased by 5% and the SPY increased by 5%. The net estimates decreased for the equal weight baseline and inverse volatility baseline and increased for the constrained lowest volatility portfolio. Volatility changed for the constrained lowest volatility portfolio but stayed the same for the others. The mandates all stayed the same.
Difference from prediction and explanation: My prediction was partly right. The equal weight and inverse volatility portfolios kept the same weights, their net estimates decreased, and their volatility stayed the same. The constrained portfolio changed. It shifted 5 points from LQD to SPY, and its volatility changed. Its net estimate increased, despite the higher fund fee, because the optimizer selected a different mix of assets. That mix changed the portfolio’s estimated return and risk enough to offset the fee increase in the displayed estimate. None of the portfolios’ mandate verdicts changed.
