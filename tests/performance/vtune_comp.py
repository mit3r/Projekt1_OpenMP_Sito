import _vtune_utils as vt
import subprocess
import os
import sys
import csv

variants: list[tuple[vt.VariantName, vt.OMPSchedule, vt.OMPChunkSize, vt.BlockSize, int]] = [
  ("k1", None, None, None, 1), # git
  ("k2", "dynamic", 5000, None, 1), # git
  ("k3", None, None, None, 20),
  ("k3a", None, None, 48 * 1024, 20), # git
  ("k4", "dynamic", 1, None, 10), # git
  ("k4a", "dynamic", 1, None, 10), # git
  ("k5", "dynamic", 1, 64 * 1024, 50), # git
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

    for name, schedule, chunk_size, block_size, loops in variants:
        for test_range in vt.ranges:
            
            print(f"Running VTune for variant: {name}, range: {test_range}", file=sys.stderr)

            print("uarch-exploration", file=sys.stderr)
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