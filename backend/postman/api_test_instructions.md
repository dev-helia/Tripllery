
# Tripllery API Test Instructions

## POST /recommend

**Purpose**: Generate 5 Tinder-style recommended POI cards.

**Request**:
- Method: POST
- URL: {{base_url}}/recommend
- Content-Type: application/json

**Example Body**:

```json
{
  "departure_city": "Boston",
  "destination": "New York",
  "start_datetime": "2025-07-01T14:00",
  "end_datetime": "2025-07-06T18:00",
  "travelers": 2,
  "budget": "mid",
  "transportation": "have_car",
  "trip_preferences": "Art, cozy cafes, less crowded places",
  "stopovers": ["New Haven"],
  "round_trip": true,
  "include_hotels": false
}
```

**Expected Output**:
- 5 POI cards (each with id, name, lat, lng, rating, description, highlight_tags, image_url, source)

---

## POST /plan

**Purpose**: Split accepted POIs into rough day-by-day plan.

**Request**:
- Method: POST
- URL: {{base_url}}/plan
- Content-Type: application/json

**Example Body**:

```json
{
  "accepted_pois": [],
  "transportation": "have_car",
  "start_datetime": "2025-07-01T14:00",
  "end_datetime": "2025-07-06T18:00"
}
```

**Expected Output**:
- Rough plan mapping days to POIs:
  ```json
  {
    "Day 1": [...],
    "Day 2": [...]
  }
  ```

---

## POST /preview

**Purpose**: Generate full day schedule with meals, transportation, free time.

**Request**:
- Method: POST
- URL: {{base_url}}/preview
- Content-Type: application/json

**Example Body**:

```json
{
  "plan": {},
  "options": {
    "start_time_of_day": "09:00",
    "avg_poi_duration": 90,
    "avg_transport_time": 20,
    "lunch_time": "12:30",
    "flexible_block": 60,
    "transportation": "have_car",
    "start_datetime": "2025-07-01T14:00",
    "end_datetime": "2025-07-06T18:00"
  }
}
```

**Expected Output**:
- List of timeline blocks (Sightseeing, Meal, Transportation, Flexible, Return)

