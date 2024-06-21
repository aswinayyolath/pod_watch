import sys
import time
import subprocess
import argparse
import curses

# Define colors using curses color constants
FG_DEF = curses.COLOR_WHITE
FG_RED = curses.COLOR_RED
FG_GREEN = curses.COLOR_GREEN
FG_YELLOW = curses.COLOR_YELLOW

def get_pods(namespace):
    """Get the list of pods in the given namespace using kubectl."""
    cmd = ["kubectl", "get", "pods"]
    if namespace:
        cmd.extend(["-n", namespace])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parse_pod_status(line):
    """Parse the pod status from the kubectl get pods output."""
    parts = line.split()
    if len(parts) >= 4:
        name = parts[0]
        ready = parts[1]
        status = parts[2]
        restarts = parts[3]
        age = parts[-1]
        return name, ready, status, restarts, age
    return None, None, None, None, None

def main(stdscr, namespace, refresh_time):
    curses.curs_set(0)
    curses.init_pair(1, FG_RED, curses.COLOR_BLACK)
    curses.init_pair(2, FG_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, FG_YELLOW, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        pods_output = get_pods(namespace)
        lines = pods_output.splitlines()

        if not lines:
            stdscr.addstr(0, 0, "No pods found in the namespace")
        else:
            # Print headers
            headers = lines[0]
            stdscr.addstr(0, 0, headers)

            for i, line in enumerate(lines[1:], start=1):
                name, ready, status, restarts, age = parse_pod_status(line)
                if status:
                    if status in ["Failed", "Terminating", "CrashLoopBackOff", "ErrImagePull"]:
                        color = curses.color_pair(1)
                    elif status in ["Pending", "Unknown", "ContainerCreating", "PodInitializing", "Init"]:
                        color = curses.color_pair(3)
                    elif status in ["Running", "Succeeded"] and ready.split('/')[0] == ready.split('/')[1]:
                        color = curses.color_pair(2)
                    else:
                        color = curses.color_pair(1)
                else:
                    color = curses.color_pair(1) 

                stdscr.addstr(i, 0, line, color)

        stdscr.refresh()
        time.sleep(refresh_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch Kubernetes pods and highlight not ready ones.")
    parser.add_argument('-n', '--namespace', type=str, help='Kubernetes namespace to watch')
    parser.add_argument('-t', '--time', type=int, default=10, help='Refresh time in seconds')

    args = parser.parse_args()
    curses.wrapper(main, args.namespace, args.time)
