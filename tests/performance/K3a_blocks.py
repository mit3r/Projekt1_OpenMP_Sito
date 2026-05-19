import _vtune_utils as vt

variant: vt.VariantName = "k3a"
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

loops: int = 20
trials = 5

vt.print_test_header()
for block_size in tests:
  for range_name in vt.ranges:

    results = [vt.measure(
      vt.create_normal_command(variant, range_name, loops, block_size),
    ) for _ in range(trials)]

    avg, deviations = vt.avg_deviation(results)

    vt.print_test_row(variant, None, None, block_size, range_name, avg, deviations, loops, trials)