import requests
from core import exceptions 
from settings import settings as st


class StockTimeSeries:

    def __init__(self):
        self.base_url = st.BASE_URL
        self.api_key =  st.APIKEY

    def _build_url(self, path):
        return f"{self.base_url}?{path}&apikey={self.api_key}"
    
    def _make_request(self, url):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                st.log.info("Success to get data from api")
            elif resp.status_code == 400:
                raise exceptions.Response404CodeError
            elif resp.status_code == 500:
                raise exceptions.Response500CodeError
            else:
                raise exceptions.ResponseGenericCodeError
        except exceptions.Response404CodeError as error:
            st.log.error(f"Error 400 :  {error}")
        except exceptions.Response500CodeError as error:
            st.log.error(f"Error 500 : {error}")
        except exceptions.ResponseGenericCodeError as error:
            st.log.error(f"Error generic : {error}")


        return resp.json()
            

    def _do_api_call_(self, **kwargs):
        
        
        interval_field = kwargs.get("interval")
        if (interval_field  and interval_field != "1min" and interval_field != "5min" and interval_field != "15min" and interval_field != "30min"  and interval_field != "60min"):
            raise exceptions.InvalidIntervalError
        
        arguments = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{'&'.join(arguments)}"
        url = self._build_url(path)
        
        response =   self._make_request(url)

        return response



    
       
    def intraday_series(self, function="TIME_SERIES_INTRADAY", symbol="IBM", interval="1min", **kwargs):
        """ 
        This API returns intraday time series of the equity specified, covering extended trading hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market).
        The intraday data is derived from the Securities Information Processor (SIP) market-aggregated data.
        You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint.
        This API returns the most recent 1-2 months of intraday data and is best suited for short-term/medium-term charting and trading strategy development.
        
         Parameters
         ----------
            ❚ Required: function

            The time series of your choice. In this case, function=TIME_SERIES_INTRADAY

            ❚ Required: symbol

            The name of the equity of your choice. For example: symbol=IBM

            ❚ Required: interval

            Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

            ❚ Optional: adjusted

            By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values.

            ❚ Optional: outputsize

            By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call.

            ❚ Optional: datatype

            By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

        Default behavior
        ----------
        https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=1min
        
        """
        st.log.debug(f"Executing intraday series endpoint")
        return self._do_api_call_(function=function,symbol=symbol,interval=interval,**kwargs)

    def intraday_series_extend_history(self, function="TIME_SERIES_INTRADAY", symbol="IBM", interval="1min",slice="year1month1", **kwargs):
        """
        The time series of your choice. In this case, function=TIME_SERIES_INTRADAY_EXTENDED

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Required: interval

        Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

        ❚ Required: slice

        Two years of minute-level intraday data contains over 2 million data points, which can take up to Gigabytes of memory. To ensure optimal API response speed, the trailing 2 years of intraday data is evenly divided into 24 "slices" - year1month1, year1month2, year1month3, ..., year1month11, year1month12, year2month1, year2month2, year2month3, ..., year2month11, year2month12. Each slice is a 30-day window, with year1month1 being the most recent and year2month12 being the farthest from today. By default, slice=year1month1.

        ❚ Optional: adjusted

        By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values.
        """
        return self._do_api_call_(function=function,symbol=symbol,interval=interval,slice=slice,**kwargs)


    def daily_series(self, function="TIME_SERIES_DAILY", symbol="IBM", **kwargs):
        """
        This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, 
        covering 20+ years of historical data. 
        If you are also interested in split/dividend-adjusted historical data, please use the Daily Adjusted API,
        which covers adjusted close values and historical split and dividend events.  

        ❚ Required: function

        The time series of your choice. In this case, function=TIME_SERIES_DAILY

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Optional: outputsize

        By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call.

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)

    def daily_adjusted_series(self, function="TIME_SERIES_DAILY_ADJUSTED", symbol="IBM", **kwargs):
        """ 
        This API returns raw (as-traded) daily open/high/low/close/volume values, 
        daily adjusted close values, and historical split/dividend events of the global equity specified, 
        covering 20+ years of historical data.

        ❚ Required: function

        The time series of your choice. In this case, function=TIME_SERIES_DAILY_ADJUSTED

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Optional: outputsize

        By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call.

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
                
        
        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)

    def weekly_series(self, function="TIME_SERIES_WEEKLY", **kwargs):
        """
       This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the global equity specified,
       covering 20+ years of historical data. 
            
        
        ❚ Required: function

        The time series of your choice. In this case, function=TIME_SERIES_WEEKLY

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
            
       """
        return self._do_api_call_(function=function,**kwargs)

    def weekly_adjusted_series(self, function="TIME_SERIES_WEEKLY_ADJUSTED", symbol="IBM", **kwargs):
        """
        This API returns weekly adjusted time series (last trading day of each week, weekly open, weekly high, 
        weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend) of the global equity specified,
        covering 20+ years of historical data.
        
        ❚ Required: function

        The time series of your choice. In this case, function=TIME_SERIES_WEEKLY_ADJUSTED

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
                
        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)

    def monthly_series(self, function="TIME_SERIES_MONTHLY", symbol="IBM", **kwargs):
        """
        This API returns monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume)
        of the global equity specified, 
        covering 20+ years of historical data.  
        
        ❚ Required: function

        The time series of your choice. In this case, function=TIME_SERIES_MONTHLY

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the monthly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
            
        
        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)

    def monthly_adjusted_series(self, function="TIME_SERIES_MONTHLY_ADJUSTED", symbol="IBM", **kwargs):
        """
         This API returns monthly adjusted time series (last trading day of each month, monthly open,
         monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified,
         covering 20+ years of historical data.  
        
        ❚ Required: function

        The time series of your choice. In this case, function=TIME_SERIES_MONTHLY_ADJUSTED

        ❚ Required: symbol

        The name of the equity of your choice. For example: symbol=IBM

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the monthly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
                
        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)
    
    def quote_series(self, function, symbol="IBM", **kwargs):
        """
        A lightweight alternative to the time series APIs,
        this service returns the price and volume information for a security of your choice.
                
        ❚ Required: function

        The API function of your choice.

        ❚ Required: symbol

        The symbol of the global security of your choice. For example: symbol=IBM.

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the quote data in JSON format; csv returns the quote data as a CSV (comma separated value) file.

        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)
    
    def search_series(self, keyword, function="TIME_SERIES_DAILY",symbol="IBM",  **kwargs):
        """
        The Search Endpoint returns the best-matching symbols and market information based on keywords of your choice.
        The search results also contain match scores that provide you with the full flexibility to develop your own search and filtering logic.
        ❚ Required: function

        The API function of your choice. In this case, function=SYMBOL_SEARCH

        ❚ Required: keywords

        A text string of your choice. For example: keywords=microsoft.

        ❚ Optional: datatype

        By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file.

        """
        return self._do_api_call_(function=function,symbol=symbol,**kwargs)


        
