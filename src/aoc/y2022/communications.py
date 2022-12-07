#!/usr/bin/env python3

"""Advent of Code 2022 Communications Parser"""

from pathlib import PurePath


class Communicator:
    def __init__(self):
        self.minimum_space = 3000000
        self.total_space = 7000000


class Message:
    def __init__(self, message):
        self.start_packet = Message.get_start(message, 4)
        self.start_message = Message.get_start(message, 14)

    @classmethod
    def get_start(cls, message, length):
        """Calculate the start of a message.

        To fix the communication system, you need to add a subroutine to the
        device that detects a *start-of-packet marker* in the datastream. In
        the protocol being used by the Elves, the start of a packet is
        indicated by a sequence of *four characters that are all different*.
        The device will send your subroutine a datastream buffer (your puzzle
        input); your subroutine needs to identify the first position where the
         four most recently received characters were all different.
        Specifically, it needs to report the number of characters from the
        beginning of the buffer to the end of the first such four-character
        marker.
        For example, suppose you receive the following datastream buffer:
        `mjqjpqmgbljsphdztnvjfqwrcgsmlb`
        """
        for i in range(length, len(message), 1):
            unique_chars = set(message[i - length : i])
            if len(unique_chars) == length:
                return i
        else:
            return -1


def parse_line(line):
    """Parse a line of input converting it to a directory or a file.

    Returns a tuple of Class, Context
    """
    left, right = line.split(" ", maxsplit=1)
    if left == "dir":
        # Make sure there's no monkey business going on
        assert right.split(" ") == [right]
        return Directory, right
    elif left == "$":
        return Command, right
    elif left.isdecimal():
        return File, line


def get_size(tree_output):
    """Return the size of a tree output."""
    left, right = tree_output
    pass


def walk_commands(commands):
    """Walk the command output."""
    path = None
    root = None
    for line in commands.splitlines():
        obj_type, context = parse_line(line)
        if obj_type == Command:
            cmd = Command(context)
            if cmd.cmd == "cd":
                new_dir = cmd.args
                if new_dir == "..":
                    path = path.parent
                else:
                    if not path:
                        path = Directory(PurePath(new_dir), parent=None)
                        root = path
                    else:
                        path = path.get_child(new_dir)
            elif cmd.cmd == "ls":
                # need to parse new lines
                continue
        elif obj_type == File:
            # Sanity check
            assert path is not None
            size, fname = context.split(" ", maxsplit=1)
            file = File(path.path / fname, size)
            path.add_child(file)
        elif obj_type == Directory:
            assert path is not None
            dir = Directory(path.path / context, path)
            path.add_child(dir)
    return root


class Command:
    """Class to represent a command on the communicator.

    Command could be cd or ls
    If cd, then the args is either `..` or a string
    """

    def __init__(self, cmd_line):
        if " " in cmd_line:
            cmd, args = cmd_line.split(" ", maxsplit=1)
        else:
            cmd, args = cmd_line, ""
        # sanity check
        assert len(args.split(" ")) <= 1
        self.cmd = cmd
        self.args = args


class File:
    """Class to represent a file on the communicator"""

    def __init__(self, path: PurePath, size):
        self.path = path
        self.size = int(size)

    def __str__(self):
        prefix = "  " * (len(self.path.parents))
        output = f"{prefix}- {self.path.name} (file, size={self.size})"
        return output


class Directory:
    """Class to represent a directory on the communicator."""

    def __init__(self, path: PurePath, parent):
        self.path = path
        self.parent = parent
        self.children = set()
        self._size = 0

    def __str__(self):
        prefix = "  " * (len(self.path.parents))
        if prefix == "":
            output = [f"- /{self.path.name} (dir)"]
        else:
            output = [f"{prefix}- {self.path.name} (dir)"]
        for entry in sorted(self.children, key=str):
            output.append(str(entry))
        return "\n".join(output)

    @property
    def size(self):
        if not self._size:
            size = 0
            for entry in self.children:
                size += entry.size
            self._size = size
        return self._size

    def add_child(self, pathlike):
        self.children.add(pathlike)

    def get_child(self, pathlike):
        for entry in self.children:
            if entry.path == self.path / pathlike:
                return entry
        else:
            raise FileNotFoundError

    def remove_child(self, entry):
        self.children.remove(entry)
