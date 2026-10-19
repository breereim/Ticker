# Video 2 - Code Validation Transcript

Timestamped transcript of the recorded audio. Obvious model terms are corrected to match the project materials: JNJ, FCFF, WACC, SEC, and diluted shares.

**00:01-00:06** For this video, I'm going to explain how my Johnson & Johnson model worked and how I checked the calculations.

**00:06-00:13** So, to do it, I used a Python model connected to a dashboard, and I used my AI learning partner to help me create that.

**00:14-00:25** The dashboard lets me change assumptions without editing the code, and it includes boundary controls, a base reset, five-year financial statements, valuation results, and visible checks.

**00:26-00:45** And so the model starts with J&J's 2025 fiscal-year financial information. It includes revenue growth, margins, research spending, capital spending, and working capital, which are used to make all the predictions, and these assumptions connect to the income statement, balance sheet, and cash-flow statement.

**00:46-01:09** The operating forecast produces free cash flow to the firm, or FCFF, and I discounted the cash flows using the WACC and then estimated the terminal value and then add excess cash and subtract the debt. And then I also divided the equity value by the diluted shares, which gave me the estimated value per share.

**01:10-01:21** And then I checked the financial statements to make sure they added up correctly and that the starting numbers matched what J&J had in their financial reports that were filed through the SEC.

**01:21-01:38** I also tested whether the model responds as expected, so if there is a higher return or if there is a lower estimated value, and if that corresponded with the inputs that I put in.

**01:38-01:45** And then I used the dashboard to test a lower revenue growth by around 1% for the forecast next years while keeping everything else unchanged.

**01:45-02:07** And this output was that in the 2030 fiscal year, the FCFF decreased from $29.5 billion to $28.6 billion, and then the enterprise value decreased from $944.3 billion to $917 billion, and the estimated value per share fell from $372 to $361.

**02:07-02:21** And then after I reset all those assumptions, the enterprise value and value per share returned to what they were originally, and that showed me that the adjustments could be reversed without changing the settings and that my model was working well.
