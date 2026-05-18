import _vtune_utils as vt
import math

variant: vt.VariantName = "k4"
# vt.print_title(variant)
# print("Testowanie podziałów pracy")
# print("Średnia z 3 pomiarów")

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

times: int = 10
for schedule, chunk_size in tests:
  label = f" {schedule}-{chunk_size}"

  results = [ vt.measure(
    vt.create_normal_command(variant, "min_max", times),
    vt.create_python_env(schedule, chunk_size)
  ) for _ in range(3) ]

  avg, deviations = vt.avg_deviation(results)

  vt.print_csv_row(schedule, chunk_size, avg, deviations)