def get_spn_by_points(points):
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    
    min_lon = min(lons)
    max_lon = max(lons)
    min_lat = min(lats)
    max_lat = max(lats)
    
    center = ((min_lon + max_lon) / 2, (min_lat + max_lat) / 2)
    
    spn_lon = abs(max_lon - min_lon) * 1.5
    spn_lat = abs(max_lat - min_lat) * 1.5
    
    if spn_lon < 0.001:
        spn_lon = 0.001
    if spn_lat < 0.001:
        spn_lat = 0.001
    
    return center, (spn_lon, spn_lat)