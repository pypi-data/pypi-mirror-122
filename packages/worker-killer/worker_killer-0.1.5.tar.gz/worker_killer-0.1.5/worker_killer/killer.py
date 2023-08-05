import subprocess
import time
from datetime import datetime, timedelta

from psutil import Process, STATUS_RUNNING, STATUS_SLEEPING, STATUS_WAKING

from worker_killer.settings import INTERVAL, MAX_STUCK_TIME, KILL_CHILD_PROCESSES


def save_process_pid(redis_connection, pid, logger):
    try:
        redis_connection.set(str(pid), str(pid))
        return True
    except Exception as e:
        logger.error(f'Error occurred while trying to save pid into redis: {e}')


def get_pid_list(redis_connection, logger):
    try:
        processes_ids = list(redis_connection.keys())
        return [int(process_id) for process_id in processes_ids if isinstance(process_id, int)]
    except Exception as e:
        logger.error(f'Error occurred while trying to get data from redis: {e}')


def remove_process_pid(redis_connection, pid, logger):
    try:
        redis_connection.remove(str(pid))
        return True
    except Exception as e:
        logger.error(f'Error occurred while trying to remove pid from redis: {e}')


def run(redis_connection, logger):
    while True:
        try:
            for pid in get_pid_list(redis_connection, logger):
                try:
                    proc = Process(pid)
                except Exception as e:
                    logger.error(f'Error occurred while trying to get process by PID = {pid}: {e}')
                    remove_process_pid(redis_connection, pid, logger)
                    continue

                current_status = proc.status()
                life_time = datetime.now() - datetime.fromtimestamp(proc.create_time())
                if current_status not in (STATUS_RUNNING, STATUS_WAKING, STATUS_SLEEPING) or (
                        current_status == STATUS_SLEEPING and life_time > timedelta(seconds=MAX_STUCK_TIME)):
                    if KILL_CHILD_PROCESSES:
                        for child in proc.children(recursive=True):
                            try:
                                subprocess.run(["sudo", "kill", "-9", str(child.pid)])
                            except Exception as e:
                                logger.error(f'Could not kill the process with PID = {child.pid}: {e}')
                                continue
                    try:
                        subprocess.run(["sudo", "kill", "-9", str(proc.pid)])
                    except Exception as e:
                        logger.error(f'Could not kill the process with PID = {pid}: {e}')
                remove_process_pid(redis_connection, pid, logger)
        except Exception as e:
            logger.error(f"Error in (run) function module killer. {e}")
        time.sleep(INTERVAL)
