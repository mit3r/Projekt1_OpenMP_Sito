import math
import subprocess
import os
import re
from time import time
from typing import Callable, Literal
from unittest import result
import sys
from datetime import datetime


type VariantName = Literal["k1", "k2", "k3", "k3a", "k4", "k4a", "k5"]
type AnalisisType = Literal["performance-snapshot", "hotspots", "memory-access", "uarch-exploration"]
type RangeName = Literal["min_max", "half_max", "min_half"]
type OMPSchedule = Literal["static", "dynamic", "guided", "auto"] | None
type OMPChunkSize = int | None
type BlockSize = int | None

variants: dict[VariantName, str] = {
  "k1": "./x64/Release/K1_Dzielenie_sekwencyjne.exe",
  "k2": "./x64/Release/K2_Dzielenie_równoległe.exe",
  "k3": "./x64/Release/K3_Sito_sekwencyjne_bez_lokalności.exe",
  "k3a": "./x64/Release/K3a_Sito_sekwencyjne_z_lokalnoscia.exe",
  "k4": "./x64/Release/K4_Sito_równoległe_funkcyjne_zapis.exe",
  "k4a": "./x64/Release/K4a_Sito_równoległe_funkcyjne_odczyt_zapis.exe",
  "k5": "./x64/Release/K5_Sito_równoległe_domenowe.exe"
}

output_dir = "./Projekt1_OpenMP_vtune"

ranges: dict[RangeName, tuple[int, int]] = {
  "min_max" : (2, int(1e8)),
  "half_max": (int(1e8 // 2), int(1e8)),
  "min_half": (2, int(1e8 // 2)),
}

analysis_types: list[AnalisisType] = [
  "performance-snapshot",
  "hotspots",
  "memory-access",
  "uarch-exploration"
]

os.makedirs(output_dir, exist_ok=True)

def create_vtune_command(
    variant: VariantName,
    range_name: RangeName,
    type: AnalisisType,
    times: int = 2,
    postfix: str = "",
) -> list[str]:
  m, n = ranges[range_name]
  name = f'{variant}_{range_name}_{type}_{times}_{postfix}'
  exe_path = os.path.abspath(variants[variant])
  output_path = os.path.abspath(os.path.join(output_dir, name))
  return [
    "vtune", "-collect", type,
    "-r", output_path, exe_path, "-m", str(m), "-n", str(n),
    "-t", str(times),
  ]

def create_normal_command(
    variant: VariantName,
    range_name: RangeName,
    times: int = 2,
    block_size: BlockSize = 48 * 1024,
) -> list[str]:
  m, n = ranges[range_name]
  exe_path = os.path.abspath(variants[variant])
  return [exe_path, "-m", str(m), "-n", str(n), "-t", str(times), "-b", str(block_size) ]

def create_python_env(
    omp_schedule: OMPSchedule,
    omp_chunk_size: OMPChunkSize = 1,
) -> dict[str, str]:
  return {"OMP_SCHEDULE": f"{omp_schedule},{omp_chunk_size}"}

def create_normal_env(
    omp_schedule: OMPSchedule,
    omp_chunk_size: OMPChunkSize = 1,
) -> str:
  if omp_chunk_size is None:
    return f"$env:OMP_SCHEDULE='{omp_schedule}'"
  
  return f"$env:OMP_SCHEDULE='{omp_schedule},{omp_chunk_size}';"

def measure(command: list[str], env_vars: dict[str, str] | None = None) -> tuple[float, int]:

  result = None
  my_env = os.environ.copy()
  if env_vars: my_env.update(env_vars)

  start_time: float = time()
  try:
    result = subprocess.run(
      command,
      check=False,
      env=my_env,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
    )
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
  end_time: float = time()

  if result is None: raise RuntimeError("Failed to execute the command.")

  primes = int(result.stdout.strip())
  return round(end_time - start_time, ndigits=3), primes

def avg_deviation(results: list[float]) -> tuple[float, float]:
  avg = sum(results) / len(results)
  deviations = math.sqrt(sum((result - avg) ** 2 for result in results) / len(results))
  return round(avg, ndigits=3), round(deviations, ndigits=3)

def print_title(variant: VariantName) -> None:
  print(f"Testing variant: {variant}")

def print_csv_row(*args: None | str | int | float) -> None:
  print("; ".join(str(arg) for arg in args))

def print_date_time() -> None:
  now = datetime.now()
  print(f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}")