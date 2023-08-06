# pypi-packages
Python util functions


Use `sh update.sh` in order to upload to https://pypi.org

Package URL - https://pypi.org/project/aggdirect-price-calculator/


`pip3 install aggdirect-price-calculator` to install packages

## Usage

```
from aggdirect-price-calculator import PriceVar

```

Post Request should include these additional parameters
1. date_created : the date at which a route is created
2. unit : Quanity type i.e Ton, Load, Hourly
3. travel_time: Computed Travel time from Mapbox

```
query = "select * from price_variables where '%s' between start_date and end_date" % date_created
query_result = engine.execute(query)

if unit == "Ton":
    var = PriceVar(query_result).trucker_haul_cost_per_ton(travel_time)
elif unit == "Load":
    var = PriceVar(query_result).trucker_haul_cost_per_load(travel_time)
else:
    var = PriceVar(query_result).trucker_haul_cost_rate()
```

Output of above code will be stored in the db