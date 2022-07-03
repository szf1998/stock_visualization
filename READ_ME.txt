Please do not mofify, move or delete F-F_Research_Data_Factors_daily.csv and F-F_Research_Data_5_Factors_2x3_daily.csv 
cause they are the required data of the executable file test3.exe.  Please make sure the two csv files and test3.exe are in the same directory.
Double click test3.exe, and input the four required parameter: 
1: For Risky Asset please input stock code of the insteresting stock, like 'AAPL', 'MSFT' and 'AMZN', 
2: For Market Benchmark please input the stock code of a popular market index, like '^GSPC'
3: For Start Date please input the specified start date in the format of yyyy-m-d
4: For End Date please input the specified end date in the format of yyyy-m-d

There are three button below the four input parameter.
1: Download data. After clicking it, there will be stock_data_MarketBenchmark.jpg and stock_data_RiskyAsset.jpg automatically downloaded 
in the same directory of test3.exe with stock price and trading volumn.

2. Run CAPM. After clicking it, the buttom will show the expected investing return rate of the input Risky Asset under the given input
MarketBenchmark, StartDate and EndDate. There will be CAPM model bar chart.jpg that visualize the risk free rate, market rate
and the CAPM model return rate prediction of the specified Risky asset, sharpe ratio visualization.jpg that visualizes the sharpe ratio 
of the input Risky asset and the market benchmark and Volatility Visualization.jpg that visualize the volatility during the input StartDate 
and EndDate for the input Risky asset and Market benchmark in the same directory of test3.exe

3. Run Fama French 3 factor and 5 factor model. After clicking it, the buttom will show the calculation result of the coefficient of 
Market minus Risk free,SMB and HML factor of Fama French 3 factor models as well as the coefficient of Market minus Risk free,SMB, HML,
RMW and CMA factor of Fama French 5 factor models. There will be FF3&5fm_return.jpg that visualize the real return rate, Fama French
3 factor model predicted return rate and Fama French 5 factor model predicted return rate, FF3fm_coefficient_value.jpg that visualize the
calculation result of coefficient value of Fama French 3 factor model and FF5fm_coefficient_value.jpg that visualize the calculation result 
of coefficient value of Fama French 5 factor model.

There is one more buttom above the four input parameter that says 'Reset'. After clicking it, the input parameters and three function buttoms
will be reset, you can change another interested paramaters to input and get the relevant result.