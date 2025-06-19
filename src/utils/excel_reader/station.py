import random
class Station:
    def __init__(self, station_no, operation, station_name, is_available, cost_per_minute):
        self.station_no = station_no
        self.operation = operation
        self.station_name = station_name
        self.is_available = is_available
        self.cost_per_minute = cost_per_minute
