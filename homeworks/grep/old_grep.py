import argparse
import sys
import re


def output(line):
    print(line)


def match(params, line: str) -> bool:
    pattern = params.pattern.replace("*", ".*").replace("?", ".")

    if params.ignore_case is True:
        pattern = re.compile(pattern, re.I)
    else:
        pattern = re.compile(pattern)

    if params.invert is True:
        return False if re.search(pattern, line) else True
    else:
        return True if re.search(pattern, line) else False


def grep(lines, params):
    matched_lines = set()

    for line_number, line in enumerate(lines):
        line = line.rstrip()
        if match(params, line):
            matched_lines.add(line_number)

    if params.context > 0 or params.before_context > 0 or params.after_context > 0:
        matched_lines_with_context = set()
        context = params.context if params.context > 0 else 0
        before_context = params.before_context if params.before_context > 0 else 0
        after_context = params.after_context if params.after_context > 0 else 0

        for line_number in matched_lines:
            for i in range(line_number, line_number - before_context - 1, -1):
                matched_lines_with_context.add(i)
            for i in range(line_number, line_number + after_context + 1, 1):
                matched_lines_with_context.add(i)
            for i in range(line_number, line_number - context - 1, -1):
                matched_lines_with_context.add(i)
            for i in range(line_number, line_number + context + 1, 1):
                matched_lines_with_context.add(i)

        if params.count is True:
            output(str(len(matched_lines_with_context)))
        else:
            for line_number, line in enumerate(lines):
                if line_number in matched_lines:
                    line = line.rstrip()
                    if params.line_number is True:
                        output(f"{line_number+1}:{line}")
                    else:
                        output(line)
                elif line_number in matched_lines_with_context:
                    line = line.rstrip()
                    if params.line_number is True:
                        output(f"{line_number + 1}-{line}")
                    else:
                        output(line)

    else:
        if params.count is True:
            output(str(len(matched_lines)))
        else:
            for line_number, line in enumerate(lines):
                if line_number in matched_lines:
                    line = line.rstrip()
                    if params.line_number is True:
                        output(f"{line_number+1}:{line}")
                    else:
                        output(line)


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
    grep(sys.stdin.readlines(), params)


if __name__ == "__main__":
    main()
