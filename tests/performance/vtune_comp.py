import _vtune_utils as vt
import subprocess
import os
import sys
import csv

variants: list[tuple[vt.VariantName, vt.OMPSchedule, vt.OMPChunkSize, vt.BlockSize, int]] = [
  ("k1", None, None, None, 1),
  ("k2", "dynamic", 1000, None, 2),
  ("k3", None, None, 1024 * 1024, 20),
  ("k4", "guided", 1, None, 1000),
  ("k4a", "guided", 1, None, 1000),
  ("k5", "guided", 1, 128 * 1024, 100),
]

def run_vtune(cmd: list[str], output_path: str, env: dict[str, str], variant_name: str):
    my_env = os.environ.copy()
    my_env.update(env)
    print(f"Running VTune collection: {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, env=my_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    
    reports_dir = os.path.join(os.path.dirname(output_path), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_csv_path = os.path.join(reports_dir, f"{variant_name}_summary.csv")
    
    report_cmd = ["vtune", "-report", "summary", "-r", output_path, "-format", "csv", "-csv-delimiter", "comma", "-report-output", report_csv_path]
    print(f"Generating report: {' '.join(report_cmd)}", file=sys.stderr)
    subprocess.run(report_cmd, capture_output=True, text=True, check=False)

def main():
    vt.print_csv_row("variant", "schedule", "chunk_size", "block_size", "range_name", 
                     "Elapsed Time", "Instructions Retired", "Clockticks", "Retiring", 
                     "Front-End Bound", "Back-End Bound", "Memory Bound", "Core Bound", 
                     "Effective Physical Core Utilization")

    for name, schedule, chunk_size, block_size, loops in variants:
        for test_range in vt.ranges:
            cmd, output_path = vt.create_vtune_command(
                variant=name, 
                range_name=test_range, 
                type="uarch-exploration", 
                times=loops, 
                postfix="comp",
                block_size=block_size
            )
            env = vt.create_python_env(schedule, chunk_size)
            variant_full_name = f"{name}_{test_range}"
            run_vtune(cmd, output_path, env, variant_full_name)

if __name__ == "__main__":
    main()