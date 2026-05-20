import _vtune_utils as vt

variants: list[tuple[vt.VariantName, vt.OMPSchedule, vt.OMPChunkSize, vt.BlockSize, int]] = [
  ("k1", None, None, None, 1), # git
  ("k2", "guided", 1, None, 1), # git
  ("k3", None, None, None, 20),
  ("k3a", None, None, 512 * 1024, 20), # git
  ("k4", "dynamic", 1, None, 10), # git
  ("k4a", "dynamic", 1, None, 10), # git
  ("k5", "guided", 1, 64 * 1024, 50), # git
]

trials: int = 5

vt.print_test_header()
for name, schedule, chunk_size, block_size, loops in variants:
    for test_range in vt.ranges:
      results = [vt.measure(
        vt.create_normal_command(name, test_range, loops, block_size), 
        vt.create_python_env(schedule, chunk_size)
      ) for _ in range(trials)]

      avg, deviations = vt.avg_deviation(results)

      vt.print_test_row(name, schedule, chunk_size, block_size, test_range, avg, deviations, loops, trials)