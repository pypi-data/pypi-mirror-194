# Trucker Haul Cost Per Load = (((([Minutes of Travel] x 2) x [Car:Truck Ratio])
# + [Minutes to Load] + [Minutes to Unload])/60) x [Trucker Hourly Rate])
# Trucker Haul Cost per Ton = [Trucker Haul Cost per Load] / [Estimated Haul Capacity]
# Customer Haul Price per Load = [Haul Cost per Load] / (1 - [Gross Profit Margin])
# Customer Haul Price per Ton = [Customer Haul Price per Load] / [Estimated Haul Capacity]

def format_datetime(x):
    """
    :param x:
    :return: DATE FROM DATETIME OBJECT
    """
    return x.strftime('%Y-%m-%d') if x else None

class PriceVar:

    def __init__(self, query_result):
        self.result = query_result


    def list_all(self):
        data = []
        for row in self.result:
            data.append({'id': row.id,
                         'hourly_rate': row.hourly_rate,
                         'gross_profit': row.gross_profit,
                         'car_truck_ratio': row.conv_ratio,
                         'truck_capacity': row.haul_capacity,
                         'trips': row.trips,
                         'loading_time': row.loading_time,
                         'unloading_time': row.unloading_time,
                         'start_date': format_datetime(row.start_date),
                         'end_date': format_datetime(row.end_date),
                         'created': row.created,
                         'created_by': row.created_by,
                         'updated': row.updated,
                         'updated_by': row.updated_by})
        return data

    def trucker_haul_cost_per_load(self, travel_time):
        var = self.list_all()
        calc = ((((travel_time * var[0]['trips']) * var[0]['car_truck_ratio']) +
                 var[0]['loading_time'] + var[0]['unloading_time']) / 60) * var[0]['hourly_rate']
        return round(calc, 2)

    def trucker_haul_cost_per_ton(self, travel_time):
        var = self.list_all()
        calc = self.trucker_haul_cost_per_load(travel_time) / var[0]['truck_capacity']
        return calc

    def trucker_haul_cost_rate(self, date_created):
        var = self.list_all(date_created)
        return var[0]['hourly_rate']

    def customer_haul_price_per_load(self):
        pass

    def customer_haul_price_per_ton(self):
        pass



