import subprocess
from os import environ
import argparse
import math
from socket import gethostname


def tcpb_spawn():
    argp = argparse.ArgumentParser(
        epilog="Start TCPB Grain specialized worker based on current machine's GPU resources"
    )
    argp.add_argument(
        "-n",
        "--ngpu",
        type=int,
        default=math.inf,
        help="Maximum number of GPUs to take (default: all of the available ones)",
    )
    args = argp.parse_args()
    _tcpb_spawn(args)


def _tcpb_spawn(args):
    def _run(cmd):
        return subprocess.run(
            cmd, shell=True, check=True, stdout=subprocess.PIPE
        ).stdout.decode()

    total = int(_run("nvidia-smi -L | wc -l").strip())
    nv_smi = iter(_run("nvidia-smi").split("\n"))
    for l in nv_smi:
        if "Processes" in l:
            break
    next(nv_smi)
    next(nv_smi)
    next(nv_smi)
    occupied = set()
    for l in nv_smi:
        if "---" in l or "No" in l:
            break
        occupied.add(int(l.split()[1]))

    l = list(set(range(total)) - occupied)
    l = l[: min(len(l), args.ngpu)]
    print(
        f"{total-len(occupied)} out of {total} GPU(s) are available; taking {len(l)} GPU(s)"
    )
    host = gethostname()
    for i in l:
        tmplog = f"tcpb-grain-{host}-device{i}.log"
        p = subprocess.Popen(
            f"grain up &> {tmplog} && rm -f {tmplog}",
            shell=True,
            env=environ | dict(CUDA_VISIBLE_DEVICES=str(i)),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
