# zone_mapping.py

def point_in_zone(x, y, zone):
    zx, zy, zw, zh = zone['x'], zone['y'], zone['w'], zone['h']
    return zx <= x <= zx + zw and zy <= y <= zy + zh

def get_zone(x, y, zones):
    """
    Determine which zone a point belongs to.
    Returns zone name if found, else None.
    """
    for name, zone in zones.items():
        if point_in_zone(x, y, zone):
            return name
    return None
