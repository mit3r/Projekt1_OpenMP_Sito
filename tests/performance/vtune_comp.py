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

def run_vtune_and_parse(cmd: list[str], output_path: str, env: dict[str, str], variant_name: str) -> dict[str, str]:
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
    
    metrics = {
        "Elapsed Time": "",
        "Instructions Retired": "",
        "Clockticks": "",
        "Retiring": "",
        "Front-End Bound": "",
        "Back-End Bound": "",
        "Memory Bound": "",
        "Core Bound": "",
        "Effective Physical Core Utilization": ""
    }
    
    if os.path.exists(report_csv_path):
        with open(report_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row: continue
                line_lower = row[0].lower().strip()
                # Basic matching strategy: if the row's first column contains the metric name, grab the second column (or last)
                if "elapsed time" in line_lower and not metrics["Elapsed Time"]:
                    metrics["Elapsed Time"] = row[1] if len(row) > 1 else ""
                elif "instructions retired" in line_lower and not metrics["Instructions Retired"]:
                    metrics["Instructions Retired"] = row[1] if len(row) > 1 else ""
                elif "clockticks" in line_lower and not metrics["Clockticks"]:
                    metrics["Clockticks"] = row[1] if len(row) > 1 else ""
                elif "retiring" == line_lower or "retiring:" in line_lower:
                    if not metrics["Retiring"]:
                        metrics["Retiring"] = row[1] if len(row) > 1 else ""
                elif "front-end bound" in line_lower and not metrics["Front-End Bound"]:
                    metrics["Front-End Bound"] = row[1] if len(row) > 1 else ""
                elif "back-end bound" in line_lower and not metrics["Back-End Bound"]:
                    metrics["Back-End Bound"] = row[1] if len(row) > 1 else ""
                elif "memory bound" in line_lower and not metrics["Memory Bound"]:
                    metrics["Memory Bound"] = row[1] if len(row) > 1 else ""
                elif "core bound" in line_lower and not metrics["Core Bound"]:
                    metrics["Core Bound"] = row[1] if len(row) > 1 else ""
                elif "effective physical core utilization" in line_lower and not metrics["Effective Physical Core Utilization"]:
                    metrics["Effective Physical Core Utilization"] = row[1] if len(row) > 1 else ""

    return metrics

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
            metrics = run_vtune_and_parse(cmd, output_path, env, variant_full_name)
            
            vt.print_csv_row(
                name, schedule, chunk_size, block_size, test_range,
                metrics["Elapsed Time"], metrics["Instructions Retired"], 
                metrics["Clockticks"], metrics["Retiring"], metrics["Front-End Bound"],
                metrics["Back-End Bound"], metrics["Memory Bound"], metrics["Core Bound"],
                metrics["Effective Physical Core Utilization"]
            )

if __name__ == "__main__":
    main()