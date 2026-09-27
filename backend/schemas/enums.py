from enum import Enum


class ComplaintCategory(str, Enum):
    roads = "Roads & Infrastructure"
    water = "Water & Sanitation"
    electricity = "Electricity"
    waste = "Waste Management"
    safety = "Public Safety"
    parks = "Parks & Recreation"
    noise = "Noise Pollution"
    other = "Other"


class ComplaintStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"


class Priority(str, Enum):
    high = "high"
    normal = "normal"
    low = "low"
