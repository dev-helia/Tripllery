"""
constants.py · Global Default Time Configurations

This module defines all default time values used in preview planning,
including default meal times, durations, and fallback durations for POIs,
transportation, and flexible time slots.

These constants are referenced throughout the preview builder and timeline
generation modules to ensure consistent fallback behavior and timeline composition.

Main Use Case:
--------------
Used by:
- `/preview` timeline scheduling
- `build_full_schedule`, `insert_*` helpers
- Fallback logic in Directions/POI planning

Author: Tripllery AI Backend
"""

# =============================
# 📅 DEFAULT TIME OF DAY SLOTS
# =============================

# What time the day starts if not overridden
DEFAULT_START_TIME_OF_DAY = "09:00"

# When to try inserting lunch or dinner
DEFAULT_LUNCH_TIME = "12:30"
DEFAULT_DINNER_TIME = "18:00"

# Latest return-to-hotel fallback
DEFAULT_DAY_END_TIME = "21:00"

# =============================
# 🕐 DEFAULT DURATIONS (minutes)
# =============================

# Average time spent at a POI
DEFAULT_POI_DURATION = 90

# Default travel time estimates (used if Directions API is not called)
DEFAULT_TRANSPORT_TIME_CAR = 20
DEFAULT_TRANSPORT_TIME_NO_CAR = 45

# Duration of flexible/free time slots (e.g., walking, resting)
DEFAULT_FLEXIBLE_BLOCK = 60

# =============================
# 🍽️ MEAL BLOCK DURATIONS
# =============================

BREAKFAST_DURATION = 30
LUNCH_DURATION = 60
DINNER_DURATION = 60

# =============================
# 🛣️ DIRECTIONS API FALLBACK VALUES
# =============================

# If routing fails, fallback travel estimates (per hop)
FALLBACK_TRANSPORT_MINUTES_CAR = 10
FALLBACK_TRANSPORT_MINUTES_NO_CAR = 15

# =============================
# 🚗 TRANSPORTATION MODES
# =============================

TRANSPORT_MODE_HAVE_CAR = "have_car"
TRANSPORT_MODE_NO_CAR = "no_car"
