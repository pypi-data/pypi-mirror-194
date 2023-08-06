import os
import time
from datetime import datetime
import shutil
import logging
import pandas as pd

def maintain_request_per_minute(num_requests: int, time_begin: float, max_requests_per_min: int, task_idx: int) -> float:
    request_per_minute = get_request_per_minute(num_requests, time_begin)
    logging.info("\n")
    while request_per_minute > max_requests_per_min:
        logging.info(
            f"Task {task_idx} > Sleeping! (Requests/minute = {request_per_minute:.2f} > {max_requests_per_min:.2f})")
        time.sleep(1)
        request_per_minute = get_request_per_minute(
            num_requests, time_begin)
    return request_per_minute

def get_request_per_minute(num_request: int, begin_time: float) -> float:
    elapsed_time = time.time() - begin_time
    request_per_minute = (num_request / elapsed_time) * 60
    return request_per_minute


def load_cache(output_file_path: str):
    """We don't want to query codex repeatedly for the same input. If an output file exists, this
    function creates a "cache" of the results.
    The cache is implemented as a hashmap keyed by `input_prompt`, and maps to the
    entire output entry

    Args:
        output_file_path (str): _description_
    """
    if not os.path.exists(output_file_path):
        return {}
    else:
        # make a backup of the file already there
        shutil.copyfile(output_file_path, output_file_path + "_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.copy(output_file_path, output_file_path + ".bak")
        cache_data = pd.read_json(
            output_file_path, orient='records', lines=True)
        cache = {row['input_prompt']: row.to_dict()
                 for _, row in cache_data.iterrows()}
        return cache
