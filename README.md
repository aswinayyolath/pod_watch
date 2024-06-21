# Kubernetes Pod Status Watcher

This Python script monitors the status of pods in a Kubernetes namespace using `kubectl` and displays them with color-coded statuses in the terminal using curses.

## Requirements

- Python 3.x
- `kubectl` configured and available in the system PATH
- Terminal with color support (for proper display of color-coded statuses)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/aswinayyolath/pod_watch.git
   cd pod_watch
   ```
2. Install dependencies:

  ```sh
    pip install kubernetes
  ```

## Usage
Run the script with the following command:

  ```sh
  python3 pod_watch.py -n <namespace> -t <refresh_time>
  ```

- <namespace>: Specify the Kubernetes namespace to monitor.
- <refresh_time>: Refresh interval in seconds (default is 10 seconds).

## Example
Monitor pods in the myproject1 namespace with a refresh time of 5 seconds

   ```sh
   python3 pod_watch.py -n myproject1 -t 5
   ```
### Color Legend

- Green: Running and ready (all containers ready).
- Yellow: Pending, Unknown, ContainerCreating, PodInitializing, Init.
- Red: Failed, Terminating, CrashLoopBackOff, ErrImagePull, and other error states.

![pod_watch (1)](https://github.com/aswinayyolath/pod_watch/assets/55191821/00d4c822-1cdb-4747-9b8f-2697cf7886a7)

