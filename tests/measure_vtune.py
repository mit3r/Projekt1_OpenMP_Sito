import subprocess
import os
from typing import Literal
from colorama import Fore, Style

# my_env = os.environ.copy()
# my_env["PATH"] = f"/usr/sbin:/sbin:{my_env['PATH']}"
# subprocess.Popen(my_command, env=my_env)


type VariantName = Literal["k1", "k2", "k3", "k3a", "k4", "k4a", "k5"]
type AnalisisType = Literal["performance-snapshot", "hotspots", "memory-access", "uarch-exploration"]
type RangeName = Literal["min_max", "half_max", "min_half"]
type OMPSchedule = Literal["static", "dynamic", "guided", "auto"]
type OMPChunkSize = int

variants: dict[VariantName, str] = {
  "k1": "./x64/Release/Projekt1_1_Dzielenie_sekwencyjne.exe",
  "k2": "./x64/Release/Projekt1_2_Dzielenie_równoległe.exe",
}

output_dir = "./vtune_output"

ranges: dict[RangeName, tuple[int, int]] = {
  "min_max" : (2, int(1e8)),
  "half_max": (int(1e8 // 2), int(1e8)),
  "min_half": (2, int(1e8 // 2)),
}

analysis_types: list[AnalisisType] = [ "performance-snapshot", "hotspots", "memory-access", "uarch-exploration" ]

os.makedirs(output_dir, exist_ok=True)

def create_vtune(
    variant: VariantName,
    range_name: RangeName,
    type: AnalisisType,
    postfix: str = "",
) -> str:
  m, n = ranges[range_name]
  name = f'{variant}_{range_name}_{type}_{postfix}'
  return " ".join([
    "vtune", "-collect", type,
    "-r", f"{output_dir}/{name}", variants[variant], "-m", str(m), "-n", str(n),
    "-t", "2",
    "--",
  ])

def create_env(
    omp_schedule: OMPSchedule,
    omp_chunk_size: OMPChunkSize = 1,
) -> str:
  return f"set OMP_SCHEDULE={omp_schedule}:{omp_chunk_size}"

variant: VariantName = "k1"
print(f"For variant: {Fore.GREEN}{variant}{Style.RESET_ALL}")  
for range_name in ranges:
  print(create_vtune(variant, range_name, "performance-snapshot"))
  print(create_vtune(variant, range_name, "hotspots"))


variant: VariantName = "k2"
print(f"For variant: {Fore.GREEN}{variant}{Style.RESET_ALL}")
for range_name in ranges:
  print("$env:OMP_SCHEDULE='static,1';", create_vtune(variant, range_name, "performance-snapshot", "static-1"))
  print("$env:OMP_SCHEDULE='static,12';", create_vtune(variant, range_name, "performance-snapshot", "static-12"))
  print("$env:OMP_SCHEDULE='static,24';", create_vtune(variant, range_name, "performance-snapshot", "static-24"))
  print("$env:OMP_SCHEDULE='dynamic';", create_vtune(variant, range_name, "performance-snapshot", "dynamic"))
  