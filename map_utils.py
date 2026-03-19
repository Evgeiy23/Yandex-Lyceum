def get_spn(lower_lon, lower_lat, upper_lon, upper_lat):
    spn_lon = abs(upper_lon - lower_lon)
    spn_lat = abs(upper_lat - lower_lat)
    
    if spn_lon < 0.0001:
        spn_lon = 0.0001
    if spn_lat < 0.0001:
        spn_lat = 0.0001
    
    return spn_lon * 1.5, spn_lat * 1.5