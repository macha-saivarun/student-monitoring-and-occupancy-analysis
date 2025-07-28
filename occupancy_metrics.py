# occupancy_metrics.py

def calculate_metrics(people_by_zone, zones):
    summary = {}

    for zone_name, people in people_by_zone.items():
        zone = zones[zone_name]
        capacity = zone["capacity"]
        area = zone["area"]

        headcount = len(people)
        occupancy_pct = (headcount / capacity) * 100 if capacity else 0

        total_area_occupied = sum([w * h for (_, _, w, h) in people])
        area_occupied_pct = (total_area_occupied / area) * 100 if area else 0

        summary[zone_name] = {
            "headcount": headcount,
            "occupancy_pct": round(occupancy_pct, 2),
            "area_occupied_pct": round(area_occupied_pct, 2),
        }

    return summary
