from enum import IntEnum
from typing import (
    List,
    Text,
    Tuple,
    Dict,
    Any,
    Callable,
    Coroutine)
import asyncio
import functools
import sys
from dataclasses import dataclass, field

VERSION = sys.version_info

# every coroutine


async def pause(sleep, *args, **kwargs):
    await asyncio.sleep(sleep)
    return [sleep, *args], kwargs


# from collections.abc import (Coroutine, Awaitable, Callable)
# from mypy_extensions import Expand

# ArgsInput = List[Any]
# KwargsInput = Dict[str, Any]
# ArgsOutput = List[Any]
# KwargsOutput = Dict[str, Any]
# AllInput = Tuple[]
# ResultOutput = Tuple[ArgsOutput, KwargsOutput]
# AwaitableResult = Awaitable[]
# CoroutineFunctionInput = Callable[[Expand[ArgsInput],
#                                    Expand[KwargsInput]], ]]


async def coromask(
        coro,
        args,
        kwargs,
        fargs):
    """
    A coroutine that mask another coroutine  callback with args, and a
    function callbacks who manage input/output of corotine callback

    :param coro: is a coroutine object defined by the developer
    :param args: the list of arguments to run on the corotine *coro*
    :param fargs: the function that process the input and create an output
    related with the coro result

    :returns: a result, is a list of the elements for future argument
    """
    msg = ""
    try:
        _in = args
        msg = f"Coromask args {args}, kwargs {kwargs}, in coro {coro}"
        obtained = await coro(*args, **kwargs)
        result = fargs(_in, obtained)
        return result
    except asyncio.TimeoutError as te:
        raise te
    except asyncio.CancelledError as ce:
        raise ce


def renew(task, coro, fargs, *args, **kwargs):
    """
    A simple function who manages the scheduled task and set the
    renew of the task

    :param task: is a Future initialized coroutine but not executed yet
    :param coro: is the corutine to renew when the first is finished
    :param fargs: the function to process input/output
    :param args: the unpacked list of extra arguments
    """
    if not task.cancelled():
        try:
            result = task.result()
            result_args, result_kwargs = result
            loop = asyncio.get_event_loop()
            stop = result_kwargs.get('stop')
            if not stop:
                task = loop.create_task(
                    coromask(coro, result_args, result_kwargs, fargs), )
                task.add_done_callback(
                    functools.partial(renew, task, coro, fargs))
            else:
                return "STOPPED"
        except asyncio.InvalidStateError as ie:
            msg = f"Coro {coro} args {args} kargs {kwargs}"
            raise ie
        except Exception as e:
            msg = f"Resultado  cancelled {task.cancelled()}, {task}, coro {coro}, fargs {fargs}"
            raise e
    else:
        try:
            result = task.result()
            return result
        except Exception as e:
            raise e


def simple_fargs(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return _in

    :_in: the input list
    :param obtained: the object that came from the result of coroutine
    execution

    :returns: _in
    """
    return _in


def simple_fargs_out(_in, obtained):
    """
    Simple function who can be used in callback on coromask, the
    inputs are /_in/ and /obtained/ value from the coroutine executed.
    Return obtained

    :param _in: the input list
    :param obtained: the object that came from the result of coroutine
    execution

    :returns: obtained
    """
    return obtained


class Steps(IntEnum):
    START = 0
    CONTINUE = 1
    PAUSE = 2
    STOP = 3
    CANCEL = 4


class TaskLoop:
    """
    Esta clase encapsula corrutinas que serán definidas
    para ejecutarse en loop

    Ofrese las siguientes acciones:

    - pause : entra a una pausa hasta que un controlador le diga continuar
    - task_continue : hace continuar la tarea si se ha pausado
    - stop : detiene definitivamente la tarea
    - close : cancela definitivamente la tarea

    Parámetros necesario:

    - coro: la corrtina a ejecutarse, debe aceptar *args,**kwargs para operar
      correctamente

    Parámetros alternativos:

    - coro_args :: lista o secuencia de entradas ordenadas
    - coro_kwargs :: diccionario con parámetros extra

    Parámetros adicionales alternativos:

    - fargs :: la funcion de operacion de las salidas
    - time_pause :: cantidad de tiempo en pause por cada iteración de loop

    """

    def __init__(
            self,
            coro: Coroutine,
            coro_args: List[Any] = [],
            coro_kwargs: Dict[str, Any] = {},
            control: Steps = Steps.START,
            fargs: Callable = simple_fargs_out,
            loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
            name: str = "taskloop",
            time_pause: float = 0.1):
        self.coro = coro
        self.coro_args = coro_args
        self.coro_kwargs = coro_kwargs
        self.control = control
        self.fargs = fargs
        self.loop = loop
        self._name = name
        self.time_pause = time_pause
        self.coro_kwargs['taskloop'] = self

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return f'''Taskloop {self.name}, coro {self.coro}'''

    def __repr__(self):
        return f"Taskloop({self.coro},{self.name})"

    def stop(self):
        self.control = Steps.STOP

    def pause(self):
        self.control = Steps.PAUSE

    def task_continue(self):
        self.control = Steps.CONTINUE

    def cancel(self):
        self.control = Steps.STOP
        return self.active_task.cancel()

    def finish(self):
        self.stop()

    def result(self):
        try:
            return self.active_task.result()
        except asyncio.CancelledError as ce:
            raise ce
        except asyncio.InvalidStateError as ie:
            raise ie

    def __await__(self):
        async def closure():
            return self.active_task
        return closure().__await__()

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def create(self):
        if VERSION.major == 3 and VERSION.minor >= 8:
            task = self.loop.create_task(
                coromask(
                    self.coro,
                    self.coro_args,
                    self.coro_kwargs,
                    self.fargs))
            self.done_callback = functools.partial(
                self.renew, task,
                self.coro,
                self.fargs)
            task.add_done_callback(self.done_callback)
            self.active_task = task
            return task
        if VERSION.major == 3 and VERSION.minor == 7:
            task = self.loop.create_task(
                coromask(
                    self.coro,
                    self.coro_args,
                    self.coro_kwargs,
                    self.fargs))

            self.done_callback = functools.partial(
                self.renew, task,
                self.coro,
                self.fargs)
            task.add_done_callback(self.done_callback)
            self.active_task = task
            return task

    def renew(self, task, coro, fargs, *args, **kwargs):
        """
        A simple function who manages the scheduled task and set the
        renew of the task

        :param task: is a Future initialized coroutine but not executed yet
        :param coro: is the corutine to renew when the first is finished
        :param fargs: the function to process input/output
        :param args: the unpacked list of extra arguments
        """
        result_kwargs = {}
        if not task.cancelled():
            try:
                result = task.result()
                result_args, result_kwargs = result
                loop = asyncio.get_event_loop()
                exception = result_kwargs.get("exception")
                if exception:
                    raise exception
                if self.control == Steps.STOP:
                    task.remove_done_callback(self.done_callback)
                    self.active_task = task
                    return "STOPPED"
                elif self.control in {Steps.START, Steps.CONTINUE}:
                    if self.control == Steps.CONTINUE:
                        coro = self.coro
                    task = None
                    if VERSION.major == 3 and VERSION.minor >= 8:
                        task = loop.create_task(
                            coromask(coro, result_args,
                                     result_kwargs, fargs), name=self._name)
                    if VERSION.major == 3 and VERSION.minor == 7:
                        task = loop.create_task(
                            coromask(coro, result_args,
                                     result_kwargs, fargs))
                    task.add_done_callback(
                        functools.partial(self.renew, task, coro,
                                          fargs))
                    self.active_task = task

                elif self.control == Steps.PAUSE:
                    pause_args = [self.time_pause]
                    pause_kwargs = {}
                    task = None
                    if VERSION.major == 3 and VERSION.minor >= 8:
                        task = loop.create_task(
                            coromask(pause, pause_args,
                                     pause_kwargs, fargs),
                            name=self._name)
                        self.active_task = task
                    if VERSION.major == 3 and VERSION.minor == 7:
                        task = loop.create_task(
                            coromask(pause, pause_args,
                                     pause_kwargs, fargs))
                    task.add_done_callback(
                        functools.partial(self.renew, task, pause,
                                          fargs))
                    self.active_task = task

            except asyncio.CancelledError as ce:
                print(f"Error de cancelación fargs {fargs}")
                raise ce
            except asyncio.IncompleteReadError as incomplete_read:
                print("IncompleteReadError {incomplete_read}")
                print("Result incomplete: {incomplete_read.partial}")
                raise incomplete_read
            except asyncio.InvalidStateError as ie:
                print("Invalid State Error", ie, "Coro", coro, "args", args,
                      "kargs", kwargs)
                raise ie
            except Exception as e:
                log = None
                if result_kwargs:
                    log = result_kwargs.get('log')
                msg = f"""TaskLoop. Result cancelled {task.cancelled()},
                    task {task},
                    coro {coro},
                    fargs {fargs}"""
                if task.done():
                    msg_done = f"TaskLoop exception, Task done {task}"
                    if log:
                        log.exception(msg_done)
                if log:
                    log.exception(msg)
                raise e
        else:
            # task is cancelled
            self.control = Steps.STOP
            task.remove_done_callback(self.done_callback)
            self.active_task = task
            return "STOPPED"
