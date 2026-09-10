
""" 
Configuration of ticker symbols that we want to combine pairs 
to find and identitfy cointegrated pairs """

TICKERS = {
    "technology": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
    
    "financials": ["JPM", "BAC", "GS", "MS"],
    
    "energy": ["XOM", "CVX", "COP", "SLB"],
    
    "consumer": ["KO", "PEP", "WMT", "COST", "MCD"],
    
    "healthcare": ["JNJ", "UNH", "PFE", "MRK"],
    
    "international_etfs": ["EWA", "EWC"],
    
    "broad_market_etfs": ["SPY", "QQQ"]
}

WINDOW = 20
CORRELATION_THRESHOLD = 0.7 
COINTEGRATION_THRESHOLD = 0.05 
