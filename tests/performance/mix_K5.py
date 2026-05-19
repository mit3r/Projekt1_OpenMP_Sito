import _vtune_utils as vt

# Pomiar prędkości przetwarzania dla końcowo wybranych wariantów


variant = "k5"

times = 20

block_sizes: list[vt.BlockSize] = [
  48 * 1024,
  64 * 1024,
  128 * 1024,
  256 * 1024,
  512 * 1024,
  1024 * 1024,
]

schedulers: list[tuple[vt.OMPSchedule, vt.OMPChunkSize]] = [
  ("static", None),
  ("static", 1),
  ("static", 10),
  ("static", 100),
  ("static", 1000),
  ("static", 5000),
  ("dynamic", None),
  ("dynamic", 1),
  ("dynamic", 10),
  ("dynamic", 100),
  ("dynamic", 1000),
  ("dynamic", 5000),
  ("guided", None),
  ("guided", 1),
  ("guided", 10),
  ("guided", 100),
  ("guided", 1000),
  ("guided", 5000),
]

times: int = 10
trials = 5

vt.print_csv_row("variant", "schedule", "chunk", "blocksize", "primes", "avg_time", "std_dev", "times", "trials")
for block_size in block_sizes:
  for schedule, chunk_size in schedulers:

      clocks = []
      primes = None
      for _ in range(trials):
        clock, prime_count = vt.measure(
          vt.create_normal_command(variant, "min_max", times, block_size), 
          vt.create_python_env(schedule, chunk_size)
        )

        clocks.append(clock)
        primes = prime_count

      avg, deviation = vt.avg_deviation(clocks)

      vt.print_csv_row(variant, schedule, chunk_size, block_size, primes, avg, deviation, times, trials)