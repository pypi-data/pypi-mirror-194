from multiprocessing import Process, Manager, Lock, Value
from utils.logger import error_logger, app_logger
import os
import threading
import signal
import time

manager = Manager()
lock = Lock()
process_pool = manager.dict()
_gc_process_id = Value("i", 0)


class MultiProcThread:
    """
    Module handler class to return instance of required module.
    """

    def __init__(self, stop_func):
        self.process_pool = process_pool
        self.process_lock = lock
        self.clean_process_pool(
            cleaner_func=self.cleaner_loop,
            process_pool=self.process_pool,
            process_lock=self.process_lock,
            _gc_process_id=_gc_process_id,
            stop_func=stop_func,
        )

    def __del__(self):
        error_logger.error(f"INVOKED FROM DESTRUCTION, {self.process_pool}")
        if _gc_process_id.value:
            os.kill(_gc_process_id.value, signal.SIGKILL)
        self.clean_pool_on_dest(self.process_pool, self.process_lock, None, None)

    def clean_process_pool(self, cleaner_func, process_pool, process_lock, _gc_process_id, stop_func):
        app_logger.info(f"CREATING CLEANING PROCESS {self.process_pool}")
        p = Process(
            target=self.process_gc, args=(cleaner_func, process_pool, process_lock, _gc_process_id, stop_func)
        )
        p.start()

    def process_gc(self, cleaner_func, process_pool, process_lock, _gc_process_id, stop_func):
        with process_lock:
            _gc_process_id.value = os.getpid()
        app_logger.info(f"_gc_process_id {_gc_process_id.value} PID::{os.getpid()}")
        th = threading.Thread(target=cleaner_func, args=(process_pool, process_lock, _gc_process_id, stop_func))
        th.daemon = True
        th.start()
        th.join()

    def clean_pool_on_dest(self, process_pool, process_lock, _gc_process_id, stop_func):
        try:
            if process_pool:
                error_logger.error("INVOKED FROM DESTRUCTION")
                proc_ids = list(process_pool.items())
                for proc in proc_ids:
                    self.stop_process(proc[0], process_lock)
        except Exception as error:
            error_logger.error(
                f"ERROR WHILE CLEANING PROCESS POOL ON `MultiProcThread` class desctruction :: {error.__str__()}"
            )

    def cleaner_loop(self, process_pool, process_lock, _gc_process_id, stop_func):
        try:
            while True:
                app_logger.info(f"CLEANER LOOP PID: {os.getpid()} & process_pool: {process_pool}")
                if process_pool:
                    proc_ids = list(process_pool.items())
                    app_logger.info(f"cleaner loop -> process_pool:: {proc_ids} & length::{len(process_pool)}")
                    for proc in proc_ids:
                        listening = stop_func(proc[0])
                        app_logger.info(f"LISTENING::{listening}")
                        if not listening[0]:
                            self.stop_process(proc[0], process_lock)
                time.sleep(20)
        except Exception as error:
            if _gc_process_id.value:
                app_logger.info(f"Removing gc process in gc cleaner_loop")
                os.kill(_gc_process_id.value, signal.SIGKILL)
            error_logger.error(f"ERROR IN PROCESS'S GARBAGE REMOVER- :: {error}")

    def if_process_exists(self, id: str):
        app_logger.info(f"IN if_process_exists: {len(self.process_pool)}, {str(self.process_pool)}")
        if id in self.process_pool:
            return True
        return False

    def create_start_process(self, id: str, code_to_execuded, args_of_code_to_execuded, stop_func):
        if self.if_process_exists(id):
            app_logger.info(f"PROCESS EXISTS {id}")
            self.stop_daemon(id, code_to_execuded, args_of_code_to_execuded, self.process_lock, stop_func)
        else:
            app_logger.info(f"CREATE PROCESS {id}")
            self.process_pool[id] = ""
            process = Process(
                name=id,
                target=self.create_daemon,
                args=(id, code_to_execuded, args_of_code_to_execuded, self.process_pool, self.process_lock, stop_func),
            )

            # self.process_pool[id]["process_ref"] = process
            app_logger.info(f"self.process_pool===> {self.process_pool}")
            # process_list.append(process)
            app_logger.info(f"Going to start process===> {process}")
            process.start()

    def stop_process(self, id: str, process_lock):  # pragma: no cover
        app_logger.info(
            f"TRYING TO STOP (def stop_process): Processes: {len(self.process_pool)}, {str(self.process_pool)}"
        )
        with process_lock:
            try:
                if id in self.process_pool and self.process_pool[id]:
                    pid = self.process_pool[id]
                    app_logger.info(f"PROCESS ID: {pid} || STOP SIGNAL: {signal.SIGKILL}")
                    os.kill(pid, signal.SIGKILL)
                    app_logger.info(f"Terminated Process: {pid}")
            except Exception as error:
                app_logger.info(f"STOP PROCESS ERROR :: {error}")
            self.remove_stopped_processes(id)

    def remove_stopped_processes(self, id):
        app_logger.info("remove_stopped_process")
        if id in self.process_pool:
            app_logger.info(f"Removed Process: {self.process_pool[id]}")
            del self.process_pool[id]
        app_logger.info(
            f"Number of Processes after removing stopped ones: {len(self.process_pool)}, {str(self.process_pool)}"
        )

    def stop_daemon(self, id: str, code_to_execuded, args_of_code_to_execuded, process_lock, stop_func):
        app_logger.info(f"STOPPING DAEMON: {id}")
        self.stop_process(id, process_lock)
        self.create_start_process(id, code_to_execuded, args_of_code_to_execuded, stop_func)

    def create_daemon(self, id: str, code_to_execuded, args_of_code_to_execuded, process_pool, process_lock, stop_func):
        with process_lock:
            process_pool[id] = os.getpid()
        t = threading.Thread(target=code_to_execuded, name=id, args=args_of_code_to_execuded)
        t.daemon = True
        t.start()
        t.join()
