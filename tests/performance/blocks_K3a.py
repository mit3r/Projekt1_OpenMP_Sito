import _vtune_utils as vt

variant: vt.VariantName = "k3a"
vt.print_title(variant)
print("Testowanie podziałów pracy")

tests: list[int] = [
  64,
  1024,
  12*1024,
  24*1024,
  36*1024,
  48*1024,
  64*1024,
  128*1024,
  256*1024,
]

times = 100
for block_size in tests:
  label = f" {block_size}"
  results = [vt.measure(
    vt.create_normal_command(variant, "min_max", times),
    vt.create_python_env("static", block_size)
  )]

  avg, deviations = vt.avg_deviation(results)

  vt.print_csv_row(label, avg, deviations)

# python.exe .\tests\performance\schedules_K2.py > outputs/schedules_K2_t1_min_max.csv