# -*- encoding: utf-8 -*-


from collections import Counter
from datetime import datetime
import re


def gen_regexp(
    ignore_files=False, request_type=None, ignore_www=False, slow_queries=False
):
    """
    Generates regular expression depending on arguments.

    Keyword arguments:
        :param ignore_files:
        :param request_type:
        :param ignore_www:
        :param slow_queries:
    Return:
        Regular expression string
    """
    regexp = '{date} "{req_type} {url} \S+" \d+ {p_time}'
    date = "\[(?P<datetime>\d+/\w+/\d+ \d+:\d+:\d+)\]"
    req_type = (
        "\w+" if request_type is None else "(?:{})".format("|".join(request_type))
    )
    url_w_ext = r"\w+://{}(?P<url>[\w.]+[^ \t\n\r\f\v]*)"
    url_wo_ext = r"\w+://{}(?P<url>[\w.]+[^ \t\n\r\f\v.]*)"
    url = url_wo_ext if ignore_files else url_w_ext
    url = url.format("(?:www\.)?" if ignore_www else "")
    p_time = "(?P<p_time>\d+)" if slow_queries else "\d+"
    fields = {"date": date, "req_type": req_type, "url": url, "p_time": p_time}
    regexp = regexp.format(**fields)
    return regexp


def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False,
    file_name="log.log",
):
    with open(file_name) as file:
        regexp = gen_regexp(ignore_files, request_type, ignore_www, slow_queries)
        regexp = re.compile(regexp)
        ignore_urls_set = set(ignore_urls)
        counter = Counter()
        if slow_queries:
            p_time = Counter()
        if start_at:
            start_at = datetime.strptime(start_at, "%d/%b/%Y %H:%M:%S")
        if stop_at:
            stop_at = datetime.strptime(stop_at, "%d/%b/%Y %H:%M:%S")
        for line in file:
            match = regexp.match(line)
            if match:
                match = match.groupdict()
                if start_at or stop_at:
                    log_datetime = datetime.strptime(
                        match["datetime"], "%d/%b/%Y %H:%M:%S"
                    )
                if start_at:
                    if log_datetime < start_at:
                        continue
                if stop_at:
                    if log_datetime > stop_at:
                        break
                if ignore_urls:
                    if match["url"] in ignore_urls_set:
                        continue
                if slow_queries:
                    p_time[match["url"]] += int(match["p_time"])
                counter[match["url"]] += 1
        if slow_queries:
            for key in counter:
                counter[key] = p_time[key] // counter[key]
    return [val[1] for val in counter.most_common(5)]


if __name__ == "__main__":
    parse()
