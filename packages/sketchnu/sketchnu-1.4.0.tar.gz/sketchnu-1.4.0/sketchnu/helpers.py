"""
Sketchnu has Numba implementations of sketch algorithms and other useful functions 
that utilize hash functions.

Copyright (C) 2022 Matthew Hendrey

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Helper functions to aid in parallelizating the creation of sketches using Python's
:code:`multiprocessing`.
"""
from datetime import datetime
import gc
import logging
from multiprocessing import get_context, Queue
import numpy as np
import psutil
from time import sleep
from typing import Callable, Dict, Generator, Iterable, List, Tuple, Union

from sketchnu.countmin import CountMin, CountMinLinear
from sketchnu.heavyhitters import HeavyHitters
from sketchnu.hyperloglog import HyperLogLog


def attach_shared_memory(sketch_type: str, sketch_args: Dict, shm_name: str):
    """
    Create a new sketch and attach it to the shared memory block. Sketch is created by
    passing sketch_args to either CountMin(), HeavyHitters() or HyperLogLog().

    Parameters
    ----------
    sketch_type : str
        Specify the type of sketch to create. Must be "cms" | "hh" | "hll".
    sketch_args : Dict
        The associated arguments to instantiante a new sketch.
    shm_name : str
        Name of a shared memory block that already exist. The new sketch will
        attach to this block.

    Returns
    -------
    local_sketch : CountMinLinear | CountMinLog16 | CountMinLog8 | HeavyHitters | HyperLogLog
        A local sketch, relative to this process, that is attached to the shared memory
        block of an existing sketch that has shared_memory = True
    """
    if sketch_type == "cms":
        local_sketch = CountMin(**sketch_args)
    elif sketch_type == "hh":
        local_sketch = HeavyHitters(**sketch_args)
    elif sketch_type == "hll":
        local_sketch = HyperLogLog(**sketch_args)
    else:
        raise TypeError(f"{sketch_type=:} is not handled")

    local_sketch.attach_existing_shm(shm_name)

    return local_sketch


def _fill_queue(
    queue: Queue, items: Iterable, n_workers: int, log_queue: Queue
) -> None:
    """
    Places the items onto the queue and adds poison pill of None for each worker
    """
    for i, item in enumerate(items):
        queue.put(item)
        try:
            item_str = str(item)
        except:
            item_str = str(i + i)
        log_queue.put({"level": "DEBUG", "text": f"{item_str} placed on the queue"})

    for _ in range(n_workers):
        queue.put(None)
    log_queue.put({"level": "INFO", "text": f"All {i+1} items placed on the queue"})

    return None


def _log_worker(log_queue: Queue):
    """
    Worker that will log statements placed onto the log_queue

    Parameters
    ----------
    log_queue : multiprocessing.Queue

    Returns
    -------
    None
    """
    logger = logging.getLogger(__name__)
    while True:
        q_item = log_queue.get()
        # Process log message
        if q_item is not None:
            try:
                level = q_item.pop("level")
                text = q_item.pop("text")
            except Exception as e:
                logger.error(f"Failed to get level|text from log msg, {q_item}. {e}")
                continue
            if level == "DEBUG":
                logger.debug(text)
            elif level == "INFO":
                logger.info(text)
            elif level == "WARNING":
                logger.warning(text)
            elif level == "CRITICAL":
                logger.critical(text)
            elif level == "ERROR":
                logger.error(text)
            elif level == "FATAL":
                logger.fatal(text)
        else:
            return None


def _worker(
    worker_id: int,
    sketch: Tuple,
    process_q_item: Callable[..., int],
    in_queue: Queue,
    log_queue: Queue,
    **kwargs,
):
    """
    Worker takes an item from the queue, uses the function process_q_item()
    to return the list of keys to be added to the cms.

    If sketch is a tuple, then this worker is updating both a cms and hll.

    Parameters
    ----------
    worker_id : int
        Simple integer id for the worker to aid logging
    sketch : Tuple
        How to instantiated sketch(s) using shared memory. Each element is itself
        a tuple with (sketch_type, sketch_args, shm_name) where sketch_type is
        "hll" | "cms", sketch_args are dictionary of arguments to give to HyperLogLog
        or CountMin, and shm_name is the name of the shared memory block to attach the
        instantiated sketch to.
    process_q_item : Callable[..., int]
        User defined function whose arguments are (q_item, \*sketches, \*\*kwargs) that
        takes the q_item, adds elements to the sketch(es) and returns the number of
        records that were processed. \*sketches must be in alphabetic order since that is
        how they will be passed by `parallel_add`.
    in_queue : Queue
        Queue containing items to be processed by the workers
    log_queue : Queue
        Queue to send logging statements to
    \*\*kwargs :
        Keyword arguments passed to process_q_item(q_item, \*\*kwargs)

    Returns
    -------
    None

    """
    log_queue.put({"level": "INFO", "text": f"WORKER {worker_id:02} is starting"})
    n_records = 0

    # Need to attach shared memory appropriately
    local_sketches = []
    for s in sketch:
        sk = attach_shared_memory(*s)
        local_sketches.append(sk)

    start = datetime.now()
    while True:
        q_item = in_queue.get()
        # Process a queue_item
        if q_item is not None:
            try:
                n_recs = process_q_item(q_item, *local_sketches, **kwargs)
            except Exception as exc:
                n_recs = 0
                msg = f"WORKER {worker_id:02} threw exception on {q_item}: {exc}"
                log_queue.put(
                    {
                        "level": "ERROR",
                        "text": msg,
                    }
                )
            n_records += n_recs

            end = datetime.now()
            speed = n_records / (end - start).total_seconds()
            log_queue.put(
                {
                    "level": "DEBUG",
                    "text": f"WORKER {worker_id:02} has processed "
                    + f"{n_records:,} records at {speed:.3f} records/sec",
                }
            )

        # Poison pill received
        else:
            # Finished processing
            for local_sketch in local_sketches:
                try:
                    # Only the CMS & HH has n_records. Fails if HLL, but we don't care
                    local_sketch.n_added_records[1] += np.uint64(n_records)
                except:
                    pass
                # This should cleanly unattach the shared memory
                del local_sketch

            end = datetime.now()
            speed = n_records / (end - start).total_seconds()
            log_queue.put(
                {
                    "level": "INFO",
                    "text": f"WORKER {worker_id:02} finished "
                    + f"{n_records:,} records at {speed:.3f} records/sec",
                }
            )
            return None


def parallel_add(
    items: Iterable,
    process_q_item: Callable[..., int],
    n_workers: int = None,
    cms_args: Dict = None,
    hh_args: Dict = None,
    hll_args: Dict = None,
    **kwargs,
):
    """
    Places `items` onto a queue to be processed by `n_workers` independent spawned
    processes.

    The user defined function, `process_q_item`, takes the arguments
    (q_item, \*sketches, \*\*kwargs). This function is given a single `item` from the
    queue and then should add elements to the sketch(es) as desired. The function
    should return the number of records processed. If `process_q_item` will add
    elements to multiple sketches, then they must be listed in alphabetic order since
    that is how `parallel_add` will pass them to `process_q_item`.

    The \*\*kwargs are passed along to `process_q_item` to allow for any needed
    additional parameters.

    Once all `items` have been processed, the `n_workers` sketch(s) are merged with the
    final result(s) returned.

    You must provide at least `cms_args` | `hh_args` | `hll_args`. If you provide more
    than one, then the requested sketches will be processed at the same time while
    going over the data just once.

    **Note:** If your data has duplicate keys within a `item`, you will likely see
    better performance if `process_q_item` does ```yield Counter(keys), n_records```
    instead of just ```yield keys, n_records```


    Parameters
    ----------
    items : Iterable
        A generator or list of items that will be placed onto a queue and then worked
        by one of the workers in a separate spawned process.
    process_q_item : Callable[..., int]
        User defined function whose arguments are (q_item, \*sketches, \*\*kwargs) that
        takes the q_item, adds elements to the sketch(es) and returns the number of
        records that were processed. \*sketches must be in alphabetic order since that is
        how they will be passed by `parallel_add`.
    n_workers : int, optional
        Number of workers to use. Each will update their own sketches which will then
        get merged together to achieve the final sketch(s). If None (default), then set
        to psutil.cpu_count(logical=False)
    cms_args : Dict, optional
        Dictionary containing arguments to instantiate a CountMin.  If None (default)
        then don't create a sketch of this type.
    hh_args : Dict, optional
        Dictionary containing arguments to instantiate a HeavyHitters. If None (default)
        then don't create a sketch of this type.
    hll_args : Dict, optional
        Dictionary containing arguments to instantiate a HyperLogLog. If None (default)
        then don't create a sketch of this type.
    \*\*kwargs :
        Keyword arguments that get passed to `process_q_item` generator function

    Returns
    -------
    The final sketch(s). If doing more than one sketch, then they are returned as a
    tuple in alphabetical order: cms, hh, hll
    """
    if (cms_args is None) and (hh_args is None) and (hll_args is None):
        raise ValueError("You forgot to provide any sketch arguments")
    if n_workers is None:
        n_workers = max(1, psutil.cpu_count(logical=False))

    ctx = get_context("spawn")
    queue = ctx.Queue(3 * n_workers)
    log_queue = ctx.Queue()

    # Set up logging
    log_process = ctx.Process(
        target=_log_worker,
        args=(log_queue,),
    )
    log_process.start()

    # Start process to fill the queue
    fill_queue_process = ctx.Process(
        target=_fill_queue, args=(queue, items, n_workers, log_queue)
    )
    fill_queue_process.start()

    # Create shared memory sketches
    log_queue.put(
        {"level": "INFO", "text": f"parallel_add: Starting {n_workers} workers"}
    )
    cms_array = []
    hll_array = []
    hh_array = []
    workers = []
    for i in range(n_workers):
        sketch = []
        if cms_args:
            cms_array.append(CountMin(**cms_args, shared_memory=True))
            # Send sketch type, its args, and shared memory block name
            sketch.append(("cms", cms_array[i].args, cms_array[i].shm.name))
        if hh_args:
            hh_array.append(HeavyHitters(**hh_args, shared_memory=True))
            # Send sketch type, its args, and shared memory block name
            sketch.append(("hh", hh_array[i].args, hh_array[i].shm.name))
        if hll_args:
            hll_array.append(HyperLogLog(**hll_args, shared_memory=True))
            # Send sketch type, its args, and shared memory block name
            sketch.append(("hll", hll_array[i].args, hll_array[i].shm.name))
        sketch = tuple(sketch)
        workers.append(
            ctx.Process(
                target=_worker,
                args=(i, sketch, process_q_item, queue, log_queue),
                kwargs=kwargs,
            )
        )
        workers[i].start()

    # Monitor for workers that exit badly
    any_none = True
    while any_none:
        sleep(1)
        any_none = False
        for i, p in enumerate(workers):
            # Still running
            if p.exitcode is None:
                any_none = True
            # Finished but with non-zero exit code, which is bad
            elif p.exitcode != 0:
                msg = f"Worker {i:02} exited badly. {p.exitcode=:}."
                msg = msg + " Possible OOM error"
                for worker in workers:
                    worker.kill()
                if fill_queue_process.exitcode is None:
                    fill_queue_process.kill()
                # Kill the log worker because it is still going
                log_process.kill()
                # Now close all the queues
                queue.close()
                log_queue.close()

    # Wait until the queue is finished being populated
    fill_queue_process.join()

    # Wait for the workers to finish
    for p in workers:
        p.join()

    if cms_args:
        log_queue.put(
            {
                "level": "INFO",
                "text": "parallel_add: Starting successive rounds of merging cms",
            }
        )
        cms_final = parallel_merging(cms_array, log_queue)
    if hh_args:
        log_queue.put(
            {
                "level": "INFO",
                "text": "parallel_add: Starting successive rounds of merging hh",
            }
        )
        hh_final = parallel_merging(hh_array, log_queue)
    if hll_args:
        log_queue.put(
            {
                "level": "INFO",
                "text": "parallel_add: Starting successive rounds of merging hll",
            }
        )
        hll_final = parallel_merging(hll_array, log_queue)

    # Send poison pill to the log_process
    log_queue.put(None)
    # Wait for the log process to finish
    log_process.join()

    if cms_args and hh_args and hll_args:
        return cms_final, hh_final, hll_final
    elif cms_args and hh_args:
        return cms_final, hh_final
    elif cms_args and hll_args:
        return cms_final, hll_final
    elif hh_args and hll_args:
        return hh_final, hll_final
    elif cms_args:
        return cms_final
    elif hh_args:
        return hh_final
    elif hll_args:
        return hll_final


def _merge_worker(sketch1: Tuple[str, Dict, str], sketch2: Tuple[str, Dict, str]):
    """
    Merge sketch2 into sketch1 when sketch1 & sketch2 are in shared memory

    Parameters
    ----------
    sketch1 : Tuple
        (sketch_type, sketch_args, shm_name) that specifies the type of sketch
        "hll" | "cms", the arguments to instantiate a new sketch using HyperLogLog() or
        CountMin(), and the name of the shared memory block that the new sketch will
        attach to.
    sketch2 : Tuple
        (sketch_type, sketch_args, shm_name) that specifies the type of sketch
        "hll" | "cms", the arguments to instantiate a new sketch using HyperLogLog() or
        CountMin(), and the name of the shared memory block that the new sketch will
        attach to.

    Returns
    -------
    None
        Side-effect causes sketch2 to merge into sketch1
    """
    # Attach existing shared memory blocks to local sketches
    s1 = attach_shared_memory(*sketch1)
    s2 = attach_shared_memory(*sketch2)

    s1.merge(s2)

    # Clean up
    del s1
    del s2
    gc.collect()

    return None


def parallel_merging(sketch_array: List, log_queue: Queue):
    """
    Merge an array of sketches in successive rounds of pairing. This will use
    at most len(sketch_array) // 2 processes. After merging, the final sketch
    is returned.

    Parameters
    ----------
    sketch_array : List
        Array containing sketches to be merged together
    log_queue : Queue
        Log statements to a log Queue

    Returns
    -------
    CountMinLinear | CountMinLog16 | CountMinLog8 | HyperLogLog
        The final sketch resulting from merging all of the sketches in the
        sketch_array.

    """
    # CountMinLinear is the parent class so all are instances of it
    if isinstance(sketch_array[0], CountMinLinear):
        sketch_type = "cms"
        sketch_args = sketch_array[0].args
    elif isinstance(sketch_array[0], HeavyHitters):
        sketch_type = "hh"
        sketch_args = sketch_array[0].args
    elif isinstance(sketch_array[0], HyperLogLog):
        sketch_type = "hll"
        sketch_args = sketch_array[0].args
    else:
        raise TypeError("sketch_array[0] is not a HyperLogLog or Count-min sketch")

    for i in range(1, len(sketch_array)):
        if sketch_args != sketch_array[i].args:
            raise TypeError(
                f"{i}th sketch has arguments that are not the same as 0th sketch"
            )

    ctx = get_context("spawn")
    n_to_merge = len(sketch_array)
    while n_to_merge > 1:
        mergers = []
        for i in range(n_to_merge // 2):
            sketch1 = (sketch_type, sketch_args, sketch_array[i * 2].shm.name)
            sketch2 = (sketch_type, sketch_args, sketch_array[i * 2 + 1].shm.name)
            mergers.append(ctx.Process(target=_merge_worker, args=(sketch1, sketch2)))
            mergers[-1].start()

        # Wait for this round of merging to finish
        for p in mergers:
            p.join()
            if p.exitcode < 0:
                raise RuntimeError(f"A _merge_worker had bad {p.exitcode=:}")

        new_sketch_array = []
        for i in range(0, n_to_merge, 2):
            new_sketch_array.append(sketch_array[i])
            # Try to free up memory as we go
            if i + 1 < len(sketch_array):
                sketch_array[i + 1] = None
                gc.collect()

        sketch_array = new_sketch_array
        n_to_merge = len(sketch_array)
        log_queue.put(
            {
                "level": "DEBUG",
                "text": f"parallel_merging: Finished round of merging. {n_to_merge} remaining",
            }
        )

    return sketch_array[0]
