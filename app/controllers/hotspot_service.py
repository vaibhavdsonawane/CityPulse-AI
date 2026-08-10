import math
from collections import defaultdict

class CivicHotspotEngine:
    """
    Spatial Analytics Engine for detecting urban complaint clusters (Hotspots).
    Uses Haversine distance formulas to group spatial coordinates within a radial threshold.
    """
    def __init__(self, radius_meters: float = 350.0):
        self.radius_meters = radius_meters

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates Great-Circle distance between two GPS points in meters.
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c
        """
        R = 6371000.0  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return R * c

    def analyze_hotspots(self, complaints):
        """
        Groups complaints into spatial hotspot clusters and computes category breakdowns and risk levels.
        """
        valid_reports = [c for c in complaints if c.latitude is not None and c.longitude is not None]
        if not valid_reports:
            return []

        clusters = []
        visited = set()

        for report in valid_reports:
            if report.id in visited:
                continue

            cluster_members = [report]
            visited.add(report.id)

            for neighbor in valid_reports:
                if neighbor.id in visited:
                    continue

                dist = self.haversine_distance(
                    report.latitude, report.longitude,
                    neighbor.latitude, neighbor.longitude
                )

                if dist <= self.radius_meters:
                    cluster_members.append(neighbor)
                    visited.add(neighbor.id)

            total_count = len(cluster_members)
            avg_lat = sum(m.latitude for m in cluster_members) / total_count
            avg_lng = sum(m.longitude for m in cluster_members) / total_count

            # Calculate Category Distribution inside Cluster
            cat_counts = defaultdict(int)
            total_priority = 0
            for m in cluster_members:
                cat_counts[m.category] += 1
                score = m.ai_prediction.priority_score if m.ai_prediction else 30
                total_priority += score

            avg_priority = total_priority / total_count

            # Determine Risk Level & Visual Indicators
            if avg_priority >= 75 or total_count >= 4:
                risk_level = 'CRITICAL'
                risk_color = '#dc3545'
                risk_badge = '🔴 CRITICAL HOTSPOT'
            elif avg_priority >= 50 or total_count >= 2:
                risk_level = 'HIGH'
                risk_color = '#fd7e14'
                risk_badge = '🟠 HIGH RISK HOTSPOT'
            else:
                risk_level = 'MEDIUM'
                risk_color = '#ffc107'
                risk_badge = '🟡 MODERATE HOTSPOT'

            top_category = max(cat_counts, key=cat_counts.get) if cat_counts else "Civic"
            zone_letter = chr(65 + (len(clusters) % 26))
            zone_name = f"Zone {zone_letter} ({top_category} Corridor)"

            clusters.append({
                'zone_id': f"ZONE-{len(clusters)+1:02d}",
                'zone_name': zone_name,
                'center_lat': round(avg_lat, 6),
                'center_lng': round(avg_lng, 6),
                'total_complaints': total_count,
                'avg_priority_score': round(avg_priority, 1),
                'risk_level': risk_level,
                'risk_color': risk_color,
                'risk_badge': risk_badge,
                'category_breakdown': dict(cat_counts),
                'radius_meters': self.radius_meters
            })

        # Sort hotspots by density and priority
        clusters.sort(key=lambda x: (x['total_complaints'], x['avg_priority_score']), reverse=True)
        return clusters

# Export singleton instance
hotspot_engine = CivicHotspotEngine()