import argparse
import re
import sys
from collections import deque, namedtuple


def output(line):
    print(line)


class Grep:
    def __init__(self, params):
        self.line_number = params.line_number
        self.invert = params.invert

        pattern = params.pattern.replace("?", ".").replace("*", ".*")
        self.regex = (
            re.compile(pattern, re.IGNORECASE)
            if params.ignore_case
            else re.compile(pattern)
        )
        self.count = 0 if params.count is True else None

        before_context_len = max(params.before_context, params.context)
        self.after_context_len = max(params.after_context, params.context)

        self.before_context_deque = (
            deque(maxlen=before_context_len) if before_context_len != 0 else None
        )
        self.after_context_counter = 0

        self.before_context: bool = params.before_context > 0 or params.context > 0
        self.context: bool = params.context > 0
        self.after_context: bool = params.after_context > 0 or params.context > 0

        self.BeforeContextLine = namedtuple(
            "BeforeContextLine", ["line_number", "line"]
        )

    def match(self, line: str) -> bool:
        match_result = re.search(self.regex, line)
        if self.invert is True:
            return False if match_result is not None else True
        else:
            return True if match_result is not None else False

    def _output(self, current_line_number: int, line: str, context_line: bool) -> None:
        if self.count is not None:
            self.count += 1
        else:
            if self.line_number is True:
                if context_line is True:
                    output(f"{current_line_number}-{line}")
                else:
                    output(f"{current_line_number}:{line}")
            else:
                output(line)

    def grep(self, lines) -> None:
        for line_number, line in enumerate(lines, start=1):
            line = line.rstrip()

            matched = self.match(line)
            if matched is True:
                if self.before_context:
                    for line_before in self.before_context_deque:
                        self._output(line_before.line_number, line_before.line, True)
                    self.before_context_deque.clear()
                if self.after_context:
                    self.after_context_counter = self.after_context_len

                self._output(line_number, line, False)
            else:
                if self.before_context:
                    if self.after_context_counter == 0:
                        self.before_context_deque.append(
                            self.BeforeContextLine(line_number, line)
                        )

                if self.after_context:
                    if self.after_context_counter == 0:
                        pass
                    else:
                        self._output(line_number, line, True)
                        self.after_context_counter -= 1
        if self.count is not None:
            output(str(self.count))


def parse_args(args):
    parser = argparse.ArgumentParser(description="This is a simple grep on python")
    parser.add_argument(
        "-v",
        action="store_true",
        dest="invert",
        default=False,
        help="Selected lines are those not matching pattern.",
    )
    parser.add_argument(
        "-i",
        action="store_true",
        dest="ignore_case",
        default=False,
        help="Perform case insensitive matching.",
    )
    parser.add_argument(
        "-c",
        action="store_true",
        dest="count",
        default=False,
        help="Only a count of selected lines is written to standard output.",
    )
    parser.add_argument(
        "-n",
        action="store_true",
        dest="line_number",
        default=False,
        help="Each output line is preceded by its relative line number in the file, starting at line 1.",
    )
    parser.add_argument(
        "-C",
        action="store",
        dest="context",
        type=int,
        default=0,
        help="Print num lines of leading and trailing context surrounding each match.",
    )
    parser.add_argument(
        "-B",
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help="Print num lines of trailing context after each match",
    )
    parser.add_argument(
        "-A",
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help="Print num lines of leading context before each match.",
    )
    parser.add_argument(
        "pattern", action="store", help="Search pattern. Can contain magic symbols: ?*"
    )
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep = Grep(params)
    grep.grep(sys.stdin.readlines())


def grep(lines, params):
    grep = Grep(params)
    grep.grep(lines)


if __name__ == "__main__":
    main()
