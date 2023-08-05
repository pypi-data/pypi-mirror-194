import asyncio
import functools
from functools import reduce
from .taskloop import coromask, renew, simple_fargs, simple_fargs_out
from .scheduler import TaskScheduler
from .taskloop import TaskLoop
from .tools import timestamp, now


def get_free_ico(icos):
    ico_list = [key for key, v in icos.items() if not v]
    ico = None
    if ico_list:
        ico = ico_list.pop()
    return ico


class TaskAssignator:
    """
    Manage the tasks assigned to a TaskScheduler instance

    :param scheduler: A TaskScheduler instance
    :param queue_tasks: a queue
    :param sta_assigned: a dict managed for multiprocessing
    :param dt_status: a string that select the kind of group {GROUP, ALL}
    :param dt_group: a list of the group selected
    :param args: some extra args
    :param kwargs: some extra keyword args

    """

    def __init__(self, scheduler, queue_tasks, queue_answer, sta_assigned,
                 dt_status, dt_group, locker, *args, **kwargs):
        self.scheduler = scheduler
        self.queue_tasks = queue_tasks
        self.queue_ans = queue_answer
        self.sta_assigned = sta_assigned
        self.dt_status = dt_status
        self.dt_group = dt_group
        self.ts = 5
        self.locker = locker
        self.code_filter = kwargs.get('code_filter', 'code')
        self.counter = 0
        if 'ts' in kwargs:
            self.ts = kwargs.get('ts', 3)

    async def new_process(self, queue_tasks, *args, **kwargs):
        """
        This coroutine activate a process with new station task
        Check every \ts\ seconds the queue_tasks if there are new
        stations or tasksto add.

        Works on a async wheel

        :param queue_tasks: a queue to put task ids

        """
        await asyncio.sleep(self.ts)
        scheduler = self.scheduler
        assigned_ids = scheduler.assigned_ids
        dt_status = self.dt_status
        dt_group = self.dt_group
        msg_in = []
        try:
            tasks = []
            W = 0
            if not queue_tasks.empty():
                for i in range(queue_tasks.qsize()):
                    # receive ids code
                    ids = queue_tasks.get()
                    code = scheduler.stations.get(ids).get(
                        self.code_filter)
                    scheduler.status_tasks[ids] = True
                    scheduler.sta_init[ids] = True
                    ipt, available = scheduler.pick_one()
                    if available:
                        respuesta = {
                            'station': ids,
                            'core': ipt,
                        }
                        icos = scheduler.add_task(ids, ipt)
                        ico = get_free_ico(icos)

                        if dt_status == 'GROUP':
                            if code in dt_group:
                                scheduler.set_init(ids)
                                self.locker.acquire()
                                self.scheduler.add_sta_assigned(
                                    ipt, ico, ids)
                                self.locker.release()
                                ans = f"TASK {ids} ADDED TO {ipt}, code {code}"
                                respuesta.update({'added': True})
                                element = scheduler.stations.get(
                                    ids).get(self.code_filter)
                                msg = "Adding new station to sta" +\
                                    f"assigned ipt {ipt} -> ico {ico} ->" +\
                                    f"ids {ids}"
                                level = 20
                                await scheduler.send_log("Assignator", level, msg, [])
                                dt_group.remove(element)

                        elif dt_status == 'ALL':
                            scheduler.set_init(ids)
                            qr = {ico: ids}
                            self.counter += 1
                            ans = "TASK %s ADDED TO %s, de un total de:%d" % (
                                ids, ipt, self.counter)
                            assigned_ids.add(ids)
                            self.locker.acquire()
                            msg = "Adding new station to sta" +\
                                f"assigned ipt {ipt} -> ico {ico} ->" +\
                                f"ids {ids}"
                            level = 20
                            await scheduler.send_log("Assignator", level, msg, [])
                            self.scheduler.add_sta_assigned(
                                ipt, ico, ids)
                            self.locker.release()
                            respuesta.update({'added':
                                              True})
                        self.queue_ans.put(respuesta)
                    else:
                        msg = f"All slots are " +\
                              f"used, can't add the station {code} ids {ids}"

                        await scheduler.send_log("Assignator", level, msg, [])

                queue_tasks.task_done()
            else:
                pass
                # self.queue_ans.put({'added': False})
            return [queue_tasks, *args], kwargs
        except Exception as ex:
            print("Error en asignación de tareas a procesador: %s" % ex)
            raise ex

    def new_process_task(self):
        """
        This function allows the system to call the coroutine that add
        a new_process in an asynchronous loop *the wheel*
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            args = [self.queue_tasks]
            task = TaskLoop(self.new_process, args, {},
                            {"name": "task_assignator"})
            task.create()
            if not loop.is_running():
                loop.run_forever()
        except Exception as ex:
            print("Error en levantar corrutina %s" % ex)
            raise ex
