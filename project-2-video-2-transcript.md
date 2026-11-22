# Project 2 Video 2 — Transcript

Source: `Project 2 Video 2.mp4`. Automated speech-to-text draft; verify against the recording before submission.

**[00:00–00:09]** So the way my code works is it starts with the README file, and that has the setup and the run instructions, and then the requirements.

**[00:09–00:19]** TXT lists the package that the app needs, and then the project also includes the price data so it doesn't need to download market data when it starts.

**[00:19–00:27]** The main app is the app.py and this is where I set the default inputs and built the Streamlit page.

**[00:27–00:39]** The sidebar controls let someone adjust the estimation window, SPY return assumption, annual fund fee, trading cost, reserve minimum, and turnover limit.

**[00:39–00:54]** When an input changes, the app recalculates the portfolio results and the tab organizes the comparison, stress cases, monitoring triggers, point in time signal, and explanation of the method.

**[00:55–01:12]** The data calculations start in the portfolio.py and it reads the price file and checks that the dates and prices are usable and then it calculates the monthly returns and it uses those to estimate the annualized returns, volatility, and correlations.

**[01:12–01:16]** And then those estimates are passed to the next part of the code.

**[01:16–01:28]** That part is the engine.py and it calculates each portfolio's estimated return after fees and trading cost, volatility, reserve share, liquidity, and turnover.

**[01:28–01:33]** And then it checks each mix against the rules the app can measure.

**[01:33–01:46]** So for the constrained portfolio, the optimizer searches possible long only mixes in 5% point steps and chooses the lowest volatility mix that meets the modeled requirements.

**[01:46–01:55]** And then since actual starting holdings weren't provided, the turnover is measured against the 60/40 benchmark as a proxy.

**[01:56–02:03]** And the BAA yield signal is included in the app with its data card, but it doesn't affect the portfolio weights.

**[02:03–02:12]** So I kept it separate from the optimizer because the data doesn't support a full point in time back test.

**[02:12–02:24]** And then decision_report.py prints a summary of the portfolio results and stress cases, and I included the output in the repository so someone can review the main results.

**[02:25–02:35]** Without starting the app and then the test checks parts of the calculations and whether the app responds to changes in it or in its controls.

**[02:35–02:40]** And one important limit is that the code doesn't verify everything in the mandate.

**[02:40–02:46]** Actual holdings, issuer look-through, and the CIO's annual loss rule are still unresolved.

**[02:46–02:55]** So when a modeled portfolio passes the checks the app can measure, the committee recommendation remains at 0% live allocation.
