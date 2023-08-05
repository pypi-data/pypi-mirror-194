import re
import select
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import IO, Pattern

from .incremental_line_split import IncrementalLineSplitter


class TimeoutException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NegativeMatchException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@dataclass
class Line:
    """
    A wrapper class to describe a line of text that was read from an input stream.
    """
    number: int
    text: str


@dataclass
class InputStream:
    """
    A wrapper class around a file-like object which data can be read from. The
    tee_out file-like object may be used to duplicate the input stream to
    another stream.
    """
    input: IO[bytes]
    tee_out: IO[str] | None = None
    splitter: IncrementalLineSplitter = field(default_factory = IncrementalLineSplitter)
    line_number = 1
    lines: list[Line] = field(default_factory=list)

    def append_line(self, data):
        text = data.decode('utf-8')
        self.lines.append(Line(number=self.line_number, text=text))
        if self.tee_out:
            self.tee_out.write(text + '\n')
        self.line_number += 1


@dataclass
class PatternSet:
    regexes: list[re.Pattern]

    def search_all(self, text: str) -> bool:
        return all(regex.search(text) for regex in self.regexes)


@dataclass
class SearchGoal:
    yes: re.Pattern
    filter: PatternSet


@dataclass
class EventContext:
    verbose_out: IO[str] | None
    line_start: dict[str, int]
    regexes_no: list[re.Pattern]
    regexes_always_no: list[re.Pattern]
    # Mapping from input label to search goals
    regexes_pending: dict[str, list[SearchGoal]]
    matches: list[tuple[str]]


def compile_patterns(patterns: Sequence[str] | None, wordwise: bool) -> list[Pattern[str]]:
    if not patterns:
        return []
    regexes = []
    for pattern in patterns:
        if wordwise:
            pattern = '\\b' + pattern + '\\b'
        regexes.append(re.compile(pattern))
    return regexes


def format_regex(regex: re.Pattern) -> str:
    return regex.pattern.removeprefix('\\b').removesuffix('\\b')


def format_regexes(regexes: Sequence[re.Pattern]) -> str:
    return ', '.join(["'" + format_regex(r) + "'" for r in regexes]) if regexes else '<none>'


def filter_message(regex: re.Pattern, filter_regexes: Sequence[re.Pattern]) -> str:
    if filter_regexes:
        return "'{}' ({})".format(format_regex(regex), format_regexes(filter_regexes))
    else:
        return "'{}'".format(format_regex(regex))


class Logscan:
    """
    Class Logscan scans one or more input streams for specific regular
    expression patterns.
    """

    def __init__(self, inputs: Mapping[str, InputStream], timeout=30):
        self.inputs = inputs
        self.timeout = timeout
        self.verbose_out: IO[str] | None = None
        self.read_list: list[IO[bytes]] = [input.input for input in inputs.values()]
        self.input_file_to_label: dict[IO[bytes], str] = {input.input: label for label, input in inputs.items()}

    @staticmethod
    def _check_negative_match(text, regexes, filter_regexes, label, line):
        for r in regexes:
            if r.search(text):
                message = "Unexpected pattern {} matches at {}:{}".format(
                        filter_message(r, filter_regexes), label, line)
                raise NegativeMatchException(message)

    @staticmethod
    def _verbose(out, msg):
        if out:
            out.write(msg + '\n')

    def _print_waiting_for(self, context: EventContext,
            regexes_yes: list[re.Pattern],
            regexes_filter: dict[str, list[PatternSet]]) -> None:
        def format_filter(label: str, label_filters: list[PatternSet]) -> str:
            if len(label_filters) == 1 and not label_filters[0].regexes:
                return label
            label_filters_texts = [format_regexes(filter_set.regexes) for filter_set in label_filters]
            return '{} ({})'.format(label, '; '.join(label_filters_texts))

        not_text = " (not: {})".format(format_regexes(context.regexes_no)) if context.regexes_no else ""
        text = "Waiting for events {}{} in {}".format(
                format_regexes(regexes_yes), not_text,
                ', '.join([format_filter(label, label_filters) for label, label_filters in regexes_filter.items()]))
        self._verbose(context.verbose_out, text)

    def _match_line(self, context: EventContext, label: str, line: Line) -> None:
        self._check_negative_match(line.text, context.regexes_always_no, None, label, line.number)

        pending = context.regexes_pending[label]
        matched = []
        for goal in pending:
            if not goal.filter.search_all(line.text):
                continue

            self._check_negative_match(line.text, context.regexes_no, goal.filter.regexes, label, line.number)

            m = goal.yes.search(line.text)
            if m:
                self._verbose(context.verbose_out,
                              "Pattern {} matches at {}:{}".format(
                                  filter_message(goal.yes, goal.filter.regexes),
                                  label, line.number))
                matched.append(goal)
                context.matches.append(m.groups())

        for r in matched:
            pending.remove(r)

    def _match_input_lines(self, context: EventContext, label) -> None:
        input = self.inputs[label]
        if label not in context.regexes_pending:
            return

        line_index = -1
        try:
            for line_index, line in enumerate(input.lines):
                self._match_line(context, label, line)
                if not context.regexes_pending[label]:
                    del context.regexes_pending[label]
                    break
        finally:
            # Consume the lines even if we hit a negative match
            input.lines = input.lines[line_index + 1:]

    def _match_lines(self, context: EventContext) -> None:
        # Copy the list of keys because we may delete from regexes_pending in the loop
        for label in list(context.regexes_pending.keys()):
            self._match_input_lines(context, label)

    def _timeout_message(self, context: EventContext) -> str:
        lines = ['Timeout waiting for patterns to match']

        for label, pending in context.regexes_pending.items():
            line_start = context.line_start[label]
            line_end = self.inputs[label].line_number

            if line_end > line_start:
                lines_message = ':{}-{}'.format(line_start, line_end - 1)
            elif line_end == 1:
                lines_message = ' (input stream is empty)'
            else:
                lines_message = ' (last line is {})'.format(line_end - 1)

            for goal in pending:
                lines.append("Pattern {} does not match in {}{}".format(
                    filter_message(goal.yes, goal.filter.regexes),
                    label,
                    lines_message))

        return '\n'.join(lines)

    def _read_input(self, context: EventContext, remaining: float):
        ready_to_read = select.select(self.read_list, [], [], remaining)[0]
        if not ready_to_read:
            raise TimeoutException(self._timeout_message(context))

        for stream in ready_to_read:
            label = self.input_file_to_label[stream]
            input = self.inputs[label]
            # for non-blocking streams 'read()' just reads the available bytes
            data = stream.read()
            if data:
                for line_bytes in input.splitter.split(data):
                    input.append_line(line_bytes)
            elif input.splitter.has_remaining():
                input.append_line(input.splitter.read_remaining())
            else:
                raise EOFError('logscan input closed: {}'.format(label))

    def event(self, yes: Sequence[str], no: Sequence[str] = [], always_no: Sequence[str] = [],
            filters: Mapping[str, Sequence[Sequence[str]]] = {},
            wordwise: bool = False,
            timeout: float | None = None,
            verbose_out: IO[str] | None = None) -> list[tuple[str]]:
        """
        Wait for patterns to appear in the input streams for which a filter is
        given. Each line of the input streams is matched against the regular
        expressions separately. Only lines from the streams for which a filter
        is given are consumed. Lines are only consumed until all the "yes"
        patterns match for each set of filter expressions.

        Here is an example "filter":
        {
            'node0': [['a', 'b']],
            'node1': [['c'], ['d']]
        }

        This means that lines satisfying the following conditions will be
        searched. They will be searched until each "yes" pattern has matched
        for each condition, or until a "no" pattern matches:

        * Lines from 'node0' matching both regexes 'a' and 'b'
        * Lines from 'node1' matching regex 'c'
        * Lines from 'node1' matching regex 'd'

        :param yes: A list of regular expression strings to look for in the input
            streams. All the patterns must match in arbitrary order. If one or
            more patterns do not match within the specified timeout, a
            TimeoutException is raised.
        :param no: A list of regular expression strings that may not match any
            line of the input streams. If any of these patterns match, a
            NegativeMatchException is raised.
        :param always_no: Like the "no" parameter, but ignoring any filters.
        :param filter: A list of sets of regular expressions for each input
            stream that should be matched. See the example in the function
            description.
        :param wordwise: If True, require that all patterns begin and end at
            word boundaries (see also the "\\b" special character in regular
            expressions).
        :param timeout: Only wait for a match for the specified amount of time
            (in seconds). If the timeout expires before a match is found, a
            TimeoutException is raised. If timeout is None (the default value),
            the global timeout value from the class instance is used.
        :param verbose_out: A file-like object to write verbose output to. This
            includes details on what patterns matched or did not match, among
            other things. If verbose_out is None (the default value), no verbose
            output is printed.
        :raises: NegativeMatchException if a forbidden pattern is matched.
            TimeoutException if no match is found before the timeout expires.
        """

        for label in filters.keys():
            if label not in self.inputs:
                raise ValueError('filter for unknown label {}'.format(label))

        line_start = {label: input.lines[0].number if input.lines else input.line_number
            for label, input in self.inputs.items()}

        regexes_yes = compile_patterns(yes, wordwise)
        regexes_no = compile_patterns(no, wordwise)
        regexes_always_no = compile_patterns(always_no, wordwise)

        regexes_filter = {
                label: [PatternSet(compile_patterns(filter_set, wordwise)) for filter_set in label_filters]
                for label, label_filters in filters.items()}

        regexes_pending = {
                label: [SearchGoal(yes, filter)
                    for yes in regexes_yes
                    for filter in regexes_filter[label]]
                for label in regexes_filter.keys()}

        timeout = timeout if timeout is not None else self.timeout

        context = EventContext(
                verbose_out=verbose_out,
                line_start=line_start,
                regexes_no=regexes_no,
                regexes_always_no=regexes_always_no,
                regexes_pending=regexes_pending,
                matches=[])
        self._print_waiting_for(context, regexes_yes, regexes_filter)

        # Match any lines captured in a previous call to event()
        self._match_lines(context)

        start = time.time()
        while context.regexes_pending:
            elapsed = time.time() - start
            remaining = max(0., timeout - elapsed)
            self._read_input(context, remaining)
            self._match_lines(context)

        return context.matches
