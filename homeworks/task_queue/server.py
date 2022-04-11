import argparse
import os
import pickle
import socketserver
import time
from dataclasses import dataclass, field
from enum import Enum


class State(Enum):
    created = "created"
    running = "running"
    finished = "finished"


@dataclass
class Task:
    task_id: str
    data_length: str
    data: str
    taken_at: float = 0.0
    state: State = State.created.value


@dataclass
class Queue:
    max_id: int = 0
    task_list: list[Task] = field(default_factory=list)


class TaskQueueTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        received_data = b""
        while True:
            chunk = self.request.recv(4096)
            received_data += chunk
            if len(chunk) < 4096:
                break
        if len(received_data) == 0:
            return
        received_data = received_data.decode("utf-8").split(" ")
        command = received_data[0]

        match command:
            case "ADD":
                self.add_command(*received_data[1:])
            case "GET":
                self.get_command(*received_data[1:])
            case "ACK":
                self.ack_command(*received_data[1:])
            case "IN":
                self.in_command(*received_data[1:])
            case "SAVE":
                self.save_command()
            case _:
                self.request.sendall(b"ERROR")

    def add_command(self, queue, length, task_data):
        if queue in server.task_queue_data:
            server.task_queue_data[queue].max_id += 1
        else:
            server.task_queue_data[queue] = Queue()

        task_id = str(server.task_queue_data[queue].max_id)
        task = Task(task_id=task_id, data_length=length, data=task_data)
        server.task_queue_data[queue].task_list.append(task)
        response = bytes(str(task_id), "ascii")
        self.request.sendall(response)

    def revert_state(self, queue):
        current_time = time.time()
        for i in server.task_queue_data[queue].task_list:
            if (
                current_time - i.taken_at >= server.timeout
                and i.state == State.running.value
            ):
                i.state = State.created.value

    def get_command(self, queue):
        if queue in server.task_queue_data:
            self.revert_state(queue)
            for i in server.task_queue_data[queue].task_list:
                if i.state == State.created.value:
                    i.state = State.running.value
                    i.taken_at = time.time()
                    self.request.sendall(
                        bytes(f"{i.task_id} {i.data_length} {i.data}", "ascii")
                    )
                    break
        else:
            self.request.sendall(b"NONE")

    def ack_command(self, queue, task_id):
        found = False
        if queue in server.task_queue_data:
            for i in server.task_queue_data[queue].task_list:
                if i.task_id == task_id and i.state != State.finished.value:
                    i.state = State.finished.value
                    found = True
                    break
        if found is False:
            self.request.sendall(b"NO")
        else:
            self.request.sendall(b"YES")

    def in_command(self, queue, task_id):
        found = False
        if queue in server.task_queue_data:
            for i in server.task_queue_data[queue].task_list:
                if i.state != State.finished.value and i.task_id == task_id:
                    found = True
                    break
        if found is False:
            self.request.sendall(b"NO")
        else:
            self.request.sendall(b"YES")

    def save_command(self):
        server.save_data()
        self.request.sendall(b"OK")


class TaskQueueServer(socketserver.TCPServer):
    def __init__(self, ip, port, path, timeout):
        self.ip = ip
        self.port = port
        self.path = path + "data.pkl"
        self.timeout = timeout

        self.task_queue_data = dict()
        self.processes = list()

        self.load_data()

        self.allow_reuse_address = True
        super(TaskQueueServer, self).__init__((self.ip, self.port), TaskQueueTCPHandler)

    def load_data(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.task_queue_data = pickle.load(f)

    def save_data(self):
        with open(self.path, "w") as f:
            pickle.dump(self.task_queue_data, f)


def parse_args():
    parser = argparse.ArgumentParser(
        description="This is a simple task queue server with custom protocol"
    )
    parser.add_argument(
        "-p", action="store", dest="port", type=int, default=5555, help="Server port"
    )
    parser.add_argument(
        "-i",
        action="store",
        dest="ip",
        type=str,
        default="127.0.0.1",
        help="Server ip adress",
    )
    parser.add_argument(
        "-c",
        action="store",
        dest="path",
        type=str,
        default="./",
        help="Server checkpoints dir",
    )
    parser.add_argument(
        "-t",
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help="Task maximum GET timeout in seconds",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.serve_forever()
