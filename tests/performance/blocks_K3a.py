import _vtune_utils as vt
import math

variant: vt.VariantName = "k3a"
# vt.print_title(variant)
# print("Testowanie rozmiaru bloku...")
# print("Średnia z 3 pomiarów")

tests: list[int] = [
  12 * 1024,
  24 * 1024,
  48 * 1024,
  64 * 1024,
  128 * 1024,
  256 * 1024,
  512 * 1024,
  1024 * 1024,
  2048 * 1024,
  4096 * 1024,
]

times: int = 20
trials = 5

vt.print_csv_row("variant","block_size", "range", "primes", "avg_time", "std_dev", "times", "trials")
for block_size in tests:
  for test_range in vt.ranges:

    clock = []
    primes = None
    for _ in range(trials):
      time, prime_count = vt.measure(
        vt.create_normal_command(variant, test_range, times, block_size),
      )

      if prime_count is None: raise RuntimeError("Failed to get prime count from the executable output.")

      clock.append(time)
      primes = prime_count * times

    avg, deviations = vt.avg_deviation(clock)

    vt.print_csv_row(variant, block_size, test_range, primes, avg, deviations, times, trials)