# Seminar Hall Seating System

A Python application that intelligently assigns seats to guests in a 10x10 seminar hall based on health status, interests, speaker roles, and mobility needs. Written for Discrete mathematics class assignment.

## Features

- **Health-based distancing**: Automatically maintains safe distances between sick/suspect individuals and healthy guests
- **Interest grouping**: Seats people with similar interests (math, AI, art, economy) near each other
- **Speaker priority**: Places speakers in optimal front/aisle positions
- **Mobility accommodation**: Prioritizes edge seats for guests with mobility aids
- **GUI Interface**: Interactive Tkinter-based interface for adding guests and viewing seating arrangements

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Usage

Run the main application:
```bash
python final.py
```

Or run the console simulation:
```bash
python mahan.py
```

### Input Parameters

- **Name**: Guest identifier
- **Health Status**: `healthy`, `suspect`, or `sick`
- **Interest**: `math`, `ai`, `art`, or `economy`
- **Speaker**: `yes` or `no`
- **Mobility**: `0` (none), `1` (cane), or `2` (wheelchair)

## Algorithm

The seating algorithm uses a scoring system that considers:
1. Health safety (maintaining Manhattan distance from sick guests)
2. Interest matching (adjacent seating for similar interests)
3. Role-based positioning (speakers near front/aisles)
4. Accessibility (mobility-restricted guests near edges)

---

*readme writtrn with AI.*
