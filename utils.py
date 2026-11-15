

def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)):
            intersect_x = ((xj - xi) * (y - yi) / (yj - yi) + xi)
            if x < intersect_x:
                inside = not inside
        j = i
    return inside

def rect_hits_polygon(rect, polygon):
    # 1. Is any corner of the player inside the polygon?
    corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]

    for corner in corners:
        if point_in_polygon(corner, polygon):
            return True

    # 2. Is any polygon point inside the player?
    for point in polygon:
        if rect.collidepoint(point):
            return True

    # 3. Does any polygon edge cross the player's rectangle?
    for i in range(len(polygon)):
        start = polygon[i]
        end = polygon[(i + 1) % len(polygon)]

        if rect.clipline(start, end):
            return True

    return False
