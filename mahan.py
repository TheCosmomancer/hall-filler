class Person:
    def __init__(self, id, health, interest, Authority_Role, mobility):
        self.id = id
        self.health = health  # healthy, sick, COVID suspect    
        self.interest = interest  # math, AI, art, economey
        self.Authority_Role = Authority_Role  # True, False
        self.mobility = mobility  # 0, 1, 2 (integers)

class Seat:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_occupied = False
        self.person = None  # Fixed: was "personerson"

def score_seat(person, row, col, hall):
    # Check bounds first
    if row < 0 or row >= NUM_ROWS or col < 0 or col >= NUM_COLS:
        return -1000
    
    # Check if seat is already occupied
    if hall[row][col].is_occupied:
        return -1000
    
    score = 0

    # Rule 1: Only applies if the person being placed is sick or COVID suspect
    if person.health in ['sick', 'COVID suspect']:
        # Check all seats around this position within a larger area
        for dr in range(-4, 5):  # Expanded range to be extra safe
            for dc in range(-4, 5):
                if dr == 0 and dc == 0:
                    continue  # skip the current seat itself
                
                r = row + dr
                c = col + dc
                
                # Check bounds
                if r < 0 or r >= NUM_ROWS or c < 0 or c >= NUM_COLS:
                    continue
                
                # Calculate Manhattan distance (horizontal + vertical steps)
                manhattan_distance = abs(dr) + abs(dc)
                neighbor_seat = hall[r][c]

                if neighbor_seat.is_occupied:
                    neighbor = neighbor_seat.person
                    
                    # Rule 1.a: Sick person must be 3+ Manhattan distance from authority OR mobility=0
                    if neighbor.Authority_Role or neighbor.mobility == 0:
                        if manhattan_distance < 3:
                            return -1000  # INVALID - too close to authority/low mobility
                    
                    # Rule 1.b: Sick person must be 2+ Manhattan distance from ALL other people
                    else:
                        if manhattan_distance < 2:
                            return -1000  # INVALID - too close to regular person

    # Rule 2: Authority-role prefer front rows and aisles.
    if person.Authority_Role:
        if row <= 2:
            score += 10
        if col == 0 or col == NUM_COLS - 1:
            score += 5
    
    # Rule 3: Low mobility - prefer edges.
    if person.mobility == 0:
        if row in [0, NUM_ROWS - 1] or col in [0, NUM_COLS - 1]:
            score += 10

    # Rule 4: interest - prefer sitting near same interest field.
    score += calculate_interest_bonus(person, row, col, hall)

    return score

def find_best_seat(person, hall):
    """Find the best seat for a person using smarter algorithm"""
    best_score = -float('inf')
    best_seat = None
    
    # Try all possible seats and calculate scores
    seat_options = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if not hall[row][col].is_occupied:
                seat_score = score_seat(person, row, col, hall)
                if seat_score > -1000:  # Only consider valid seats
                    seat_options.append((seat_score, row, col))
    
    # Sort by score (highest first) and return best option
    if seat_options:
        seat_options.sort(reverse=True)
        best_score, best_row, best_col = seat_options[0]
        return (best_row, best_col), best_score
    
    return None, -1000

def assign_seat(person, hall):
    """Assign a person to the best available seat"""
    best_seat, best_score = find_best_seat(person, hall)
    
    if best_seat and best_score > -1000:
        row, col = best_seat
        hall[row][col].is_occupied = True
        hall[row][col].person = person
        health_status = f"[{person.health}]"
        authority_status = "[AUTH]" if person.Authority_Role else ""
        mobility_status = f"[M{person.mobility}]" if person.mobility == 0 else ""
        print(f"Person {person.id} {health_status}{authority_status}{mobility_status} ({person.interest}) → seat ({row}, {col}) [score: {best_score}]")
        return True
    else:
        print(f"❌ Person {person.id} [{person.health}] - NO VALID SEAT FOUND (health constraints too strict)")
        return False

def get_seating_statistics(hall):
    """Generate statistics about current seating"""
    total_occupied = sum(1 for row in hall for seat in row if seat.is_occupied)
    health_stats = {'healthy': 0, 'sick': 0, 'COVID suspect': 0}
    interest_groups = {}
    authority_count = 0
    mobility_stats = {0: 0, 1: 0, 2: 0}
    
    for row in hall:
        for seat in row:
            if seat.is_occupied:
                person = seat.person
                health_stats[person.health] += 1
                interest_groups[person.interest] = interest_groups.get(person.interest, 0) + 1
                if person.Authority_Role:
                    authority_count += 1
                mobility_stats[person.mobility] += 1
    
    print(f"\n=== SEATING STATISTICS ===")
    print(f"Total occupied seats: {total_occupied}/{NUM_ROWS * NUM_COLS}")
    print(f"Health distribution: {health_stats}")
    print(f"Interest groups: {interest_groups}")
    print(f"Authority figures: {authority_count}")
    print(f"Mobility levels: {mobility_stats}")

def calculate_interest_bonus(person, row, col, hall):
    """Calculate bonus score for sitting near people with same interest"""
    bonus = 0
    # Check all 4 adjacent seats (up, down, left, right)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            neighbor_seat = hall[r][c]
            if neighbor_seat.is_occupied and neighbor_seat.person.interest == person.interest:
                bonus += 5
    
    # Also check diagonal neighbors for additional small bonus
    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
            neighbor_seat = hall[r][c]
            if neighbor_seat.is_occupied and neighbor_seat.person.interest == person.interest:
                bonus += 2
    
    return bonus

def print_hall_status(hall):
    """Print current hall occupancy"""
    print("\nHall Status (Person IDs):")
    print("   ", end="")
    for c in range(NUM_COLS):
        print(f"{c:3}", end="")
    print()
    
    for r in range(NUM_ROWS):
        print(f"{r:2} ", end="")
        for c in range(NUM_COLS):
            if hall[r][c].is_occupied:
                print(f"{hall[r][c].person.id:3}", end="")
            else:
                print("  .", end="")
        print()

# The hall with 100 seats
NUM_ROWS = 10
NUM_COLS = 10

hall = [[Seat(r, c) for c in range(NUM_COLS)] for r in range(NUM_ROWS)]

# Test cases based on PDF requirements
test_people = [
    # Authority figures with different health status
    Person(1, 'healthy', 'AI', True, 2),
    Person(2, 'sick', 'math', True, 1),
    
    # Low mobility people
    Person(3, 'healthy', 'art', False, 0),
    Person(4, 'COVID suspect', 'economey', False, 0),
    
    # Regular people with same interests (should sit together)
    Person(5, 'healthy', 'AI', False, 2),
    Person(6, 'healthy', 'AI', False, 1),
    Person(7, 'healthy', 'math', False, 2),
    Person(8, 'healthy', 'math', False, 1),
    
    # More sick people to test distancing
    Person(9, 'sick', 'art', False, 1),
    Person(10, 'COVID suspect', 'economey', False, 2),
    
    # Mix of authority and regular
    Person(11, 'healthy', 'art', True, 2),
    Person(12, 'healthy', 'economey', False, 2),
]

def run_seating_simulation():
    """Run the complete seating simulation"""
    print("=" * 60)
    print("INTELLIGENT SEMINAR HALL SEATING SYSTEM")
    print("Based on Discrete Mathematics Project Requirements")
    print("=" * 60)
    
    # Reset hall
    global hall
    hall = [[Seat(r, c) for c in range(NUM_COLS)] for r in range(NUM_ROWS)]
    
    print(f"\nProcessing {len(test_people)} people for {NUM_ROWS}x{NUM_COLS} seminar hall...")
    
    # Assign seats with HEALTH as first priority
    sorted_people = sorted(test_people, key=lambda p: (
        0 if p.health in ['sick', 'COVID suspect'] else 2,  # Sick people FIRST
        0 if p.Authority_Role else 1,  # Then authority
        p.mobility  # Then mobility level
    ))
    
    successful_assignments = 0
    for person in sorted_people:
        if assign_seat(person, hall):
            successful_assignments += 1
    
    print(f"\n{successful_assignments}/{len(test_people)} people successfully seated")
    
    print_hall_status(hall)
    get_seating_statistics(hall)
    
    return successful_assignments == len(test_people)