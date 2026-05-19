import _vtune_utils as vt



variants: list[tuple[vt.VariantName, vt.OMPSchedule, vt.OMPChunkSize, vt.BlockSize, int]] = [
  # ("k1", None, None, None, 1), # git
  ("k2", "dynamic", 1000, None, 2), # git
  ("k3", None, None, 1024 * 1024, 20),
  ("k4", "guided", 1, None, 10), # git
  ("k4a", "guided", 1, None, 10), # git
  ("k5", "guided", 1, 128 * 1024, 20), # git
]

trials: int = 5

vt.print_csv_row("variant", "range", "schedule", "chunk_size", "block_size", "primes", "avg_time", "std_dev", "times")
for name, schedule, chunk_size, block_size, times in variants:
    for test_range in vt.ranges:

      clocks = []
      primes = None
      for i in range(trials):
        print(f"Running {i}. iter. for {name} with schedule={schedule}, chunk_size={chunk_size}, block_size={block_size}...")

        clock, prime_count = vt.measure(
          vt.create_normal_command(name, test_range, times, block_size), 
          vt.create_python_env(schedule, chunk_size)
        )

        clocks.append(clock)
        primes = prime_count

      avg, deviation = vt.avg_deviation(clocks)
      vt.print_csv_row(name, test_range, schedule, chunk_size, block_size, primes, avg, deviation, times)