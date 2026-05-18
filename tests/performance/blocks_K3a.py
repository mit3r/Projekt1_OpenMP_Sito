import _vtune_utils as vt
import math

variant: vt.VariantName = "k3a"
# vt.print_title(variant)
# print("Testowanie rozmiaru bloku...")
# print("Średnia z 3 pomiarów")

tests: list[int] = [
  # 12 * 1024,
  # 24 * 1024,
  # 48 * 1024,
  # 64 * 1024,
  # 128 * 1024,
  # 256 * 1024,
  512 * 1024,
  1024 * 1024,
  2048 * 1024,
  4096 * 1024,
]

times: int = 20
for block_size in tests:

  results = [ vt.measure(
    vt.create_normal_command(variant, "min_max", times, block_size),
  ) for _ in range(3) ]

  avg, deviations = vt.avg_deviation(results)

  vt.print_csv_row(block_size, avg, deviations)