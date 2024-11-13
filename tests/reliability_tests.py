import random
import time

failure_times = []
recovery_times = []

def simulate_failure():
    start_time = time.time()
    # Simulate a random time before a failure occurs
    time.sleep(random.uniform(1, 5))
    failure_time = time.time() - start_time
    failure_times.append(failure_time)
    print(f"Failure occurred after {failure_time:.2f} seconds.")

def simulate_recovery():
    start_time = time.time()
    # Simulate a random time for recovery
    time.sleep(random.uniform(1, 3))
    recovery_time = time.time() - start_time
    recovery_times.append(recovery_time)
    print(f"Recovered in {recovery_time:.2f} seconds.")

for _ in range(5):  # Simulate 5 cycles
    simulate_failure()
    simulate_recovery()

# Calculate MTBF and MTTR
MTBF = sum(failure_times) / len(failure_times)
MTTR = sum(recovery_times) / len(recovery_times)
availability = MTBF / (MTBF + MTTR)

print(f"MTBF: {MTBF:.2f} seconds")
print(f"MTTR: {MTTR:.2f} seconds")
print(f"Availability: {availability * 100:.2f}%")
