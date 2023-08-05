# Copyright (c) 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-qos.
#
# linuxnet-qos is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-qos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-qos. If not, see
# <https://www.gnu.org/licenses/>.

"""
This module contains parsers to create Python objects from the output
of the **tc(8)** command.
"""

from typing import Any, Iterable, Iterator, List, Optional

from .deps import get_logger
from .exceptions import TcError, TcParsingError
from .handle import Handle


_logger = get_logger("linuxnet.qos.parsers")


class _PeekingIterator:
    """An iterator that supports peeking
    """
    def __init__(self, iterable) -> Iterable[Any]:
        """
        :param iterable: an iterable object that does not contain ``None``
        """
        self.__iter = iter(iterable)
        self.__peeked = None

    def __iter__(self):
        return self

    def __next__(self) -> Any:
        if self.__peeked is not None:
            token = self.__peeked
            self.__peeked = None
        else:
            token = next(self.__iter)
        return token

    def peek(self) -> Optional[Any]:
        """Returns the next token or ``None`` if there are no more tokens.
        """
        if self.__peeked is not None:
            return self.__peeked
        try:
            self.__peeked = next(self.__iter)
            return self.__peeked
        except StopIteration:
            return None


class LineGroupIterator:
    """The LineGroupIterator is used to parse the output of
    ``tc filter ls``. It returns lines one-by-one and is capable of
    single-level backtracking. This allows the filter-specific
    parsing code to return a line back to the iterator if it
    does not belong to it.
    """
    def __init__(self, tc_output: List[str]):
        self.__line_iter = iter(tc_output)
        self.__backtracked_line = None
        self.__current_line = None
        self.__field_iter = None

    def __iter__(self):
        return self

    def __next__(self) -> str:
        """Returns either the backtracked line or the next line from
        the sub-iterator
        """
        if self.__backtracked_line is None:
            self.__current_line = next(self.__line_iter)
        else:
            self.__current_line = self.__backtracked_line
            self.__backtracked_line = None
        self.__field_iter = None
        return self.__current_line

    def next_field(self) -> str:
        """Returns the next field of the current line
        """
        return next(self.get_field_iter())

    def get_field_iter(self) -> Iterator[str]:
        """Returns an iterator over the fields of the current line
        """
        if self.__current_line is None:
            raise TcError("attempt to access next field before line iteration")
        if self.__field_iter is None:
            self.__field_iter = _PeekingIterator(self.__current_line.split())
        return self.__field_iter

    def clear_field_iter(self):
        """This method removes the field iterator so that a call
        to :meth:`get_field_iter` will create a new one to scan
        the line from the beginning.
        """
        self.__field_iter = None

    def get_last_line(self) -> str:
        """Returns the last line returned by :meth:`__next__`
        """
        return self.__current_line

    def backtrack(self) -> None:
        """Backtrack the current line.
        """
        if self.__backtracked_line is not None:
            _logger.error("%s: attempt to backtrack twice; current line: %s",
                self.backtrack.__qualname__, self.__backtracked_line)
            raise TcError('attempt to backtrack twice')
        self.__backtracked_line = self.__current_line
        self.__current_line = None
        self.__field_iter = None


class FilterOutputLine:
    """A class that holds a line of filter output.

    One can iterate over the fields of the line::

        def parse_fields(fline: FilterOutputLine):
            for field in fline:
                if field == 'xxx':
                    ...

    The entire line can be returned by using the :func:`str` builtin function.
    """
    def __init__(self, line: str, fields: List[str]):
        """
        :param line: the complete **tc(8)** filter line
        :param fields: list of fields of the line **after** the filter type
        """
        self.__line = line
        self.__fields = fields

    def __iter__(self):
        return iter(self.__fields)

    def __str__(self):
        return self.__line


class FilterOutput:
    """An instance of this class contains the **tc(8)** output for a
    single filter.
    """
    def __init__(self, proto: str, prio: int, filter_type: str):
        """
        :param proto: filter protocol
        :param prio: filter priority
        :param filter_type: filter type
        """
        self.__proto = proto
        self.__prio = prio
        self.__filter_type = filter_type
        self.__filter_lines = []
        self.__nonfilter_lines = []

    def matches(self, proto: str, prio: int, filter_type: str) -> bool:
        """Returns ``True`` if the ``proto``, ``prio``, ``filter_type``
        parameters match with the corresponding attributes of this object.

        :meta private:
        """
        return (self.__proto == proto and self.__prio == prio and
                                        self.__filter_type == filter_type)

    def get_prio(self) -> int:
        """Returns the priority value
        """
        return self.__prio

    def get_proto(self) -> str:
        """Returns the protocol value
        """
        return self.__proto

    def get_filter_type(self) -> str:
        """Returns the filter type
        """
        return self.__filter_type

    def get_first_line(self) -> str:
        """Returns the first line from the **tc(8)** output for this filter
        """
        return str(self.__filter_lines[0])

    def has_nonfilter_lines(self) -> bool:
        """Returns ``True`` if the filter output has any lines not
        starting with the word ``filter``
        """
        return bool(self.__nonfilter_lines)

    def add_filter_line(self, line: str, fields: List[str]) -> None:
        """Add a line that starts with ``filter ``

        :meta private:
        """
        self.__filter_lines.append(FilterOutputLine(line, fields))

    def add_line(self, line: str) -> None:
        """Add a non-filter prefixed line

        :meta private:
        """
        self.__nonfilter_lines.append(line.strip())

    def filter_lines_iter(self) -> Iterator[FilterOutputLine]:
        """Returns an iterator that returns :class:`FilterOutputLine`
        instances.
        """
        return iter(self.__filter_lines)

    def nonfilter_lines_iter(self) -> Iterator[str]:
        """Returns an iterator that returns lines (strings)
        """
        return iter(self.__nonfilter_lines)


class TrafficFilterParser:
    """Helper class that creates :class:`TrafficFilter` objects from the
    output of the **tc(8)** command.
    """

    #
    # Key: the tuple (filter_type, protocol) - both strings
    # Value: a TrafficFilter subclass
    #
    _filter_class_map = {}

    def __init__(self):
        self.__filter_list = []
        # __iter is a LineGroupIterator
        self.__iter: LineGroupIterator = None

    @classmethod
    def register_filter(cls, *, filter_type: str, protocol: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`TrafficFilter` class).

        This method is intended to be used for adding support for new
        traffic filter types.

        :param filter_type: a **tc(8)** filter type, e.g. ``u32``
        :param protocol: a **tc(8)** protocol name, e.g. ``ip``
        :param klass: the Python class for this ``(filter_type, protocol)``
        """
        cls._filter_class_map[(filter_type, protocol)] = klass

    def __process_filter(self, filt_output: FilterOutput):
        """Try to create a new :class:`TrafficFilter` from ``filt_output``.
        """
        #
        # Currently we only support 'ip' filters
        #
        line = filt_output.get_first_line()
        protocol = filt_output.get_proto()
        if protocol != 'ip':
            _logger.warning(
                "we cannot handle protocol '%s' (will skip); "
                "line=%s", protocol, line)
            return
        filter_type = filt_output.get_filter_type()
        klass = self._filter_class_map.get((filter_type, protocol))
        if klass is None:
            _logger.warning(
                "cannot handle filter type '%s', protocol '%s' (will skip); "
                "line=%s",
                    filter_type, protocol, line)
            return
        try:
            traffic_filter = klass.parse(filt_output)
        except TcParsingError as tcparserr:
            _logger.warning("failed to parse U32 filter output: %s", tcparserr)
            return
        if traffic_filter.get_dest_handle() is None:
            _logger.warning("filter %s has no dest handle", traffic_filter)
        traffic_filter._mark_as_instantiated()
        self.__filter_list.append(traffic_filter)

    def __advance(self, field_name: str, has_value=True) -> Optional[str]:
        """We are expecting the next 2 fields to be ``field_name``
        followed by its value.
        We return that value.
        """
        next_field = None
        try:
            next_field = self.__iter.next_field()
            if next_field != field_name:
                _logger.error("%s: expected '%s', found '%s'",
                    self.__advance.__qualname__, field_name, next_field)
                raise TcParsingError(f"expecting '{field_name}'")
            return self.__iter.next_field() if has_value else None
        except StopIteration as stopit:
            if next_field is None:
                raise TcParsingError(f'missing {field_name}') from stopit
            raise TcParsingError(f'no value for {field_name}') from stopit

    def parse_output(self, tc_output_lines: List[str]) -> None:
        """Parse the **tc(8)** output in ``tc_output_lines`` into a list
        of :class:`TrafficFilter` objects; the list can be accessed via
        the :meth:`get_filter_list` method.

        :meta private:
        """
        self.__filter_list = []
        self.__iter = LineGroupIterator(tc_output_lines)
        #
        # Process lines into FilterOutput objects.
        # Each FilterOutput object has the lines of one filter.
        # Once all lines of a filter are seen, invoke the
        # filter's parse method to create the TrafficFilter object.
        #
        filt_out = None
        for line in self.__iter:
            line = line.strip()
            if not line:
                continue
            if not line.startswith('filter '):
                if filt_out is None:
                    raise TcParsingError('unexpected filter line', line=line)
                filt_out.add_line(line)
                continue
            #
            # We expect a filter line to look like this:
            #   filter protocol <val> pref <int> <type>
            #
            try:
                _ = self.__advance('filter', has_value=False)
                protocol = self.__advance('protocol')
                priostr = self.__advance('pref')
                try:
                    prio = int(priostr)
                except ValueError as valerr:
                    _logger.error("%s: bad priority: %s",
                        self.parse_output.__qualname__, priostr)
                    raise TcParsingError('bad filter priority') from valerr
                try:
                    filter_type = self.__iter.next_field()
                except StopIteration as stopit:
                    raise TcParsingError("missing filter type") from stopit
                if filt_out is None:
                    filt_out = FilterOutput(protocol, prio, filter_type)
                    filt_out.add_filter_line(line,
                                    fields=list(self.__iter.get_field_iter()))
                    continue
                if filt_out.matches(protocol, prio, filter_type):
                    filt_out.add_filter_line(line,
                                    fields=list(self.__iter.get_field_iter()))
                    continue
            except TcParsingError as parserr:
                parserr.set_line(line)
                raise
            #
            # Beginning of output for a new filter.
            # Process the one we have.
            #
            self.__process_filter(filt_out)
            filt_out = FilterOutput(protocol, prio, filter_type)
            filt_out.add_filter_line(line,
                            fields=list(self.__iter.get_field_iter()))
        if filt_out is not None:
            self.__process_filter(filt_out)

    def get_filter_list(self) -> List['TrafficFilter']:
        """Returns a list of :class:`TrafficFilter` objects from the
        parsed output

        :meta private:
        """
        return self.__filter_list

    def get_filter(self) -> Optional['TrafficFilter']:
        """Returns the first :class:`TrafficFilter` from the parsed output,
        or ``None`` if no filter was successfully parsed.

        :meta private:
        """
        return self.__filter_list[0] if self.__filter_list else None


def _group_split(lines: List[str], marker: str) -> List[List[str]]:
    """Given a list of lines, break them into groups of
    consecutive lines, where the first line of each group starts with
    the ``marker`` string.
    """
    group_list = []
    line_group = []
    for line in lines:
        if not line:
            continue
        if line.startswith(marker):
            # Beginning of new line group
            if line_group:
                group_list.append(line_group)
                line_group = []
            line_group.append(line)
        else:
            if line_group:
                line_group.append(line)
            else:
                raise TcParsingError(
                    f"first line does not start with '{marker}'", line=line)
    if line_group:
        group_list.append(line_group)
    return group_list


class QClassOutput:
    """Helper class used for parsing ``tc class ls`` output for a single qclass
    """
    def __init__(self, line_group: List[str]):
        """
        :param line_group: list of lines, guaranteed not to be empty
        """
        self.__line_iter = LineGroupIterator(line_group)
        self.__handle = None
        self.__parent_handle = None
        self.__qclass_line = None
        self.__qdisc_handle = None

    def get_handle(self) -> Handle:
        """Returns the (parsed) :class:`Handle` of the queuing class.
        """
        return self.__handle

    def get_parent_handle(self) -> Handle:
        """Returns the (parsed) :class:`Handle` of the parent of the
        queuing class.
        """
        return self.__parent_handle

    def get_qdisc_handle(self) -> Optional[Handle]:
        """Returns the :class:`Handle` of a (leaf) qdisc
        """
        return self.__qdisc_handle

    def get_linegroup_iter(self) -> LineGroupIterator:
        """Returns the LineGroupIterator for the tc output lines.

        :meta private:
        """
        return self.__line_iter

    def get_class_line(self) -> str:
        """Returns the **tc(8)** output class line
        """
        return self.__line_iter.get_last_line()

    def get_field_iter(self) -> Iterator[str]:
        """Return an iterator for the (remaining) fields of the class line
        """
        return self.__line_iter.get_field_iter()

    def parse_first_line(self) -> str:
        """Parse the first line and return a string with the qdisc type
        (e.g. 'htb')

        :meta private:
        """
        if self.__qclass_line is not None:
            raise TcError('attempt to parse first line twice')
        self.__qclass_line = next(self.__line_iter)
        field_iter = self.get_field_iter()
        try:
            #
            # All class lines have the form:
            #
            # class <type> <handle> parent <handle> [leaf <qdisc-handle>] ...
            #
            # where the ... part is type-specific
            #
            if next(field_iter) != 'class':
                raise TcParsingError("line does not start with 'class'")
            qdisc_type = next(field_iter)
            # The handle string may not include a major number, e.g.
            #    class mq :1 root
            # or
            #    class mq :1 parent 10:
            #
            # We need to parse the parent handle before we can
            # parse the class handle. If the parent is root, we assume
            # the major number is 0 (so the class handle for the first
            # line will be 0:1)
            handle_str = next(field_iter)
            try:
                handle = Handle.parse(handle_str)
            except TcParsingError:
                handle = None
            parent_field = next(field_iter)
            if parent_field == 'root':
                parent_major = 0 if handle is None else handle.major
                self.__parent_handle = Handle.qdisc_handle(parent_major)
            elif parent_field == 'parent':
                self.__parent_handle = Handle.parse(next(field_iter))
            else:
                raise TcParsingError(
                    f"cannot determine class parent from field {parent_field}")
            if handle is None:
                self.__handle = Handle.parse(handle_str,
                                    default_major=self.__parent_handle.major)
            else:
                self.__handle = handle
            if field_iter.peek() == 'leaf':
                _ = next(field_iter)
                self.__qdisc_handle = Handle.parse(next(field_iter))
            return qdisc_type
        except StopIteration as stopit:
            raise TcParsingError("not enough fields") from stopit


class QClassParser:
    """Helper class that creates :class:`QClass` objects from the
    output of the **tc(8)** command.
    """

    _qclass_map = {}

    def __init__(self, allow_parsing_errors: bool):
        self.__allow_parsing_errors = allow_parsing_errors
        self.__parsing_errors = 0
        self.__qclass_list = []

    def get_error_count(self) -> int:
        """Returns number of parsing errors encountered

        :meta private:
        """
        return self.__parsing_errors

    @classmethod
    def register_qclass(cls, ident: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`QClass` class).

        This method is intended to be used for adding support for new
        queuing discipline classes.

        :param ident: the queuing class name that appears in the
            ``tc -s class ls`` output.
        :param klass: the Python class for this queuing class
        """
        cls._qclass_map[ident] = klass

    def parse_output(self, tc_output_lines: List[str]) -> None:
        """Parse the **tc(8)** output in ``tc_output_lines`` into a list
        of :class:`QClass` objects; the list can be accessed via
        the :meth:`get_qclass_list` method.

        :meta private:
        """
        self.__qclass_list = []
        for line_group in _group_split(tc_output_lines, 'class '):
            qclass_output = QClassOutput(line_group)
            try:
                qdisc_type = qclass_output.parse_first_line()
                klass = self._qclass_map.get(qdisc_type)
                if klass is None:
                    if qdisc_type == 'sfq':
                        # SFQ is classless, so this should never happen;
                        # yet on CentOS 6.10, I observed the following in
                        # the output of 'tc class ls':
                        #
                        # class sfq 202:2c9 parent 202:
                        #
                        # 202: was a SFQ qdisc; the class minor number
                        # changed for every invocation of 'tc class ls'
                        _logger.warning("classless SFQ has a class: %s",
                                qclass_output.get_class_line())
                        continue
                    raise TcParsingError(f"unknown qdisc type {qdisc_type}")
                qclass = klass.parse(qclass_output)
                qclass._parse_stats(qclass_output.get_linegroup_iter())
                self.__qclass_list.append(qclass)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                line = qclass_output.get_class_line()
                _logger.error("%s: parsing error, line='%s'",
                    self.parse_output.__qualname__, line)
                if not self.__allow_parsing_errors:
                    parserr.set_line(line)
                    raise

    def get_qclass_list(self) -> List['QClass']:
        """Returns a list of :class:`QClass` objects from the
        parsed output

        :meta private:
        """
        return self.__qclass_list

    def get_qclass(self) -> Optional['QClass']:
        """Returns the first :class:`QClass` from the parsed output,
        or ``None`` if no queuing class was successfully parsed.

        :meta private:
        """
        return self.__qclass_list[0] if self.__qclass_list else None


class QDiscOutput:
    """Helper class used for parsing ``tc qdisc ls`` output for a single qdisc
    """
    def __init__(self, line_group: List[str]):
        """
        :param line_group: list of lines, guaranteed not to be empty
        """
        self.__line_iter = LineGroupIterator(line_group)
        self.__handle = None
        self.__parent_handle = None
        self.__refcnt = None
        self.__qdisc_line = None

    def get_handle(self) -> Handle:
        """Returns the (parsed) :class:`Handle` of the queuing discipline.
        """
        return self.__handle

    def get_parent_handle(self) -> Optional[Handle]:
        """Returns the (parsed) :class:`Handle` of the parent of this
        queueing discipline, or ``None`` if this is a root qdisc
        """
        return self.__parent_handle

    def get_refcnt(self) -> Optional[int]:
        """Returns reference count of qdisc (``None`` for non-root qdiscs,
        and for some root qdiscs like ``mq``)
        """
        return self.__refcnt

    def get_linegroup_iter(self) -> LineGroupIterator:
        """Returns the LineGroupIterator for the tc output lines.

        :meta private:
        """
        return self.__line_iter

    def get_qdisc_line(self) -> str:
        """Returns the **tc(8)** output qdisc line
        """
        return self.__line_iter.get_last_line()

    def get_field_iter(self) -> Iterator[str]:
        """Return an iterator for the (remaining) fields of the qdisc line
        """
        return self.__line_iter.get_field_iter()

    def parse_first_line(self) -> str:
        """Parse the first line and return a string with the qdisc type
        (e.g. 'htb')

        :meta private:
        """
        if self.__qdisc_line is not None:
            raise TcError('attempt to parse first line twice')
        self.__qdisc_line = next(self.__line_iter)
        field_iter = self.__line_iter.get_field_iter()
        try:
            #
            # All qdisc lines have the form:
            #
            # qdisc <type> <handle> (root refcnt <num> |parent <handle>) ...
            #
            # where the ... part is type-specific
            #
            if next(field_iter) != 'qdisc':
                raise TcParsingError("line does not start with 'qdisc'")
            qdisc_type = next(field_iter)
            self.__handle = Handle.parse(next(field_iter))
            parent_field = next(field_iter)
            if parent_field == 'root':
                # Some root qdiscs like 'mq' do not provide a refcount
                next_field = next(field_iter, None)
                if next_field is None:
                    return qdisc_type
                if next_field != 'refcnt':
                    raise TcParsingError(
                        f"found '{next_field}' after 'root' "
                        "instead of 'refcnt'")
                self.__refcnt = int(next(field_iter))
            elif parent_field == 'parent':
                self.__parent_handle = Handle.parse(next(field_iter),
                                            default_major=self.__handle.major)
            else:
                raise TcParsingError(
                    f"cannot determine qdisc parent from field {parent_field}")
            return qdisc_type
        except StopIteration as stopit:
            raise TcParsingError("not enough fields") from stopit


class QDiscParser:
    """Helper class that creates :class:`QDisc` objects from the
    output of the **tc(8)** command.
    """

    _qdisc_class_map = {}

    def __init__(self, allow_parsing_errors: bool):
        self.__allow_parsing_errors = allow_parsing_errors
        self.__parsing_errors = 0
        self.__qdisc_list = []

    def get_error_count(self) -> int:
        """Returns number of parsing errors encountered

        :meta private:
        """
        return self.__parsing_errors

    @classmethod
    def register_qdisc(cls, ident: str, klass) -> None:
        """Register the given class (which should be a subclass of
        the :class:`QDisc` class).

        This method is intended to be used for adding support for new
        queuing disciplines.

        :param ident: the qdisc name that appears in the
            ``tc -s qdisc ls`` output.
        :param klass: the Python class for this queuing discipline
        """
        cls._qdisc_class_map[ident] = klass

    def parse_output(self, tc_output_lines: List[str]) -> None:
        """Parse the **tc(8)** output in ``tc_output_lines`` into a list
        of :class:`QDisc` objects; the list can be accessed via
        the :meth:`get_qdisc_list` method.

        :meta private:
        """
        #
        # High-level logic:
        #   - parse the output into line groups, one for each qdisc; parsing
        #     is at the syntactic level only
        #   - for each group, determine the particular qdisc and let it
        #     parse the output
        #
        # Parsing requirements:
        #  1. The 1st line needs to be partially parsed to determine the
        #     specific qdisc
        #  2. The next 2 lines (with stats) can be parsed by common code
        #     because they are the same across qdisc's
        #  3. Give the option to the qdisc-specific parsing code to parse
        #     the whole output
        #  4. Give the option to the qdisc-specific code to use the
        #     common parsing code
        #
        # Based on the above, the QDiscOutput object contains the common
        # parsing code. Consequently, it also holds parsed fields
        # (like handles etc.)
        #
        self.__qdisc_list = []
        for line_group in _group_split(tc_output_lines, 'qdisc '):
            qdisc_output = QDiscOutput(line_group)
            try:
                qdisc_type = qdisc_output.parse_first_line()
                klass = self._qdisc_class_map.get(qdisc_type)
                if klass is None:
                    raise TcParsingError(f"unknown qdisc {qdisc_type}")
                qdisc = klass.parse(qdisc_output)
                qdisc._parse_stats(qdisc_output.get_linegroup_iter())
                self.__qdisc_list.append(qdisc)
            except TcParsingError as parserr:
                self.__parsing_errors += 1
                line = qdisc_output.get_qdisc_line()
                _logger.error("%s: parsing error, line='%s'",
                    self.parse_output.__qualname__, line)
                if not self.__allow_parsing_errors:
                    parserr.set_line(line)
                    raise

    def get_qdisc_list(self) -> List['QDisc']:
        """Returns a list of :class:`QDisc` objects from the
        parsed output

        :meta private:
        """
        return self.__qdisc_list

    def get_qdisc(self) -> Optional['QDisc']:
        """Returns the first :class:`QDisc` from the parsed output,
        or ``None`` if no queuing discipline was successfully parsed.

        :meta private:
        """
        return self.__qdisc_list[0] if self.__qdisc_list else None
