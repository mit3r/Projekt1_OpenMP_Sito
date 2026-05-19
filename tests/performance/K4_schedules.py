import _vtune_utils as vt

variant: vt.VariantName = "k4"

tests: list[tuple[vt.OMPSchedule, vt.OMPChunkSize]] = [
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

loops: int = 50
trials = 5

vt.print_test_header()
for schedule, chunk_size in tests:

  results = [vt.measure(
    vt.create_normal_command(variant, "min_max", loops),
    vt.create_python_env(schedule, chunk_size),
  ) for _ in range(trials)]

  avg_time, std_dev = vt.avg_deviation(results)

  vt.print_test_row(variant, schedule, chunk_size, None, "min_max", avg_time, std_dev, loops, trials)