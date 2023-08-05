from typing import Sequence, Union

import pytest
import _pytest
from _pytest.terminal import TerminalReporter

def pytest_addoption(parser: pytest.Parser, 
                     pluginmanager: pytest.PytestPluginManager):
    group = parser.getgroup('general')
    group.addoption(
        '--pyspec',
        action='store_true',
        default=False,
        help='Enables pyspec features'
    )

# def pytest_configure(config: pytest.Config):
    # if getattr(config.option, 'spec', 0) and not getattr(config.option, 'quiet', 0) and not getattr(config.option, 'verbose', 0):
    # old_logreport = TerminalReporter.pytest_runtest_logreport
    # TerminalReporter.pytest_runtest_logreport = _pytest_runtest_logreport

def _pytest_runtest_logreport(self: TerminalReporter, report: pytest.TestReport) -> None:
    # if report.when == 'call':
    #     self._tw.line()
    #     self._tw.line('teste')
    #     self._tw.write(report.item.obj.__doc__)
    #     # print(report.item, report.outcome)
    # self.flush()
    self._tests_ran = True
    rep = report
    res: Tuple[
        str, str, Union[str, Tuple[str, Mapping[str, bool]]]
    ] = self.config.hook.pytest_report_teststatus(report=rep, config=self.config)
    category, letter, word = res
    if not isinstance(word, tuple):
        markup = None
    else:
        word, markup = word
    self._add_stats(category, [rep])
    if not letter and not word:
        # Probably passed setup/teardown.
        return
    running_xdist = hasattr(rep, "node")
    if markup is None:
        was_xfail = hasattr(report, "wasxfail")
        if rep.passed and not was_xfail:
            markup = {"green": True}
        elif rep.passed and was_xfail:
            markup = {"yellow": True}
        elif rep.failed:
            markup = {"red": True}
        elif rep.skipped:
            markup = {"yellow": True}
        else:
            markup = {}
    # if self.verbosity <= 0:
    if self.verbosity < 0: 
        self._tw.write(letter, **markup)
    else:
        self._progress_nodeids_reported.add(rep.nodeid)
        line = self._locationline(rep.nodeid, *rep.location)
        if not running_xdist:
            self.write_ensure_prefix(line, word, **markup)
            if rep.skipped or hasattr(report, "wasxfail"):
                reason = _get_raw_skip_reason(rep)
                if self.config.option.verbose < 2:
                    available_width = (
                        (self._tw.fullwidth - self._tw.width_of_current_line)
                        - len(" [100%]")
                        - 1
                    )
                    formatted_reason = _format_trimmed(
                        " ({})", reason, available_width
                    )
                else:
                    formatted_reason = f" ({reason})"

                if reason and formatted_reason is not None:
                    self._tw.write(formatted_reason)
            if self._show_progress_info:
                self._write_progress_information_filling_space()
        else:
            self.ensure_newline()
            self._tw.write("[%s]" % rep.node.gateway.id)
            if self._show_progress_info:
                self._tw.write(
                    self._get_progress_information_message() + " ", cyan=True
                )
            else:
                self._tw.write(" ")
            self._tw.write(word, **markup)
            self._tw.write(" " + line)
            self.currentfspath = -2
    self.flush()

# @pytest.hookimpl(hookwrapper=True)
# @pytest.hookimpl(hookwrapper=True)
# @pytest.hookimpl(tryfirst=True)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # report = pytest.TestReport.from_item_and_call(item, call)
    outcome = yield
    report: pytest.Report = outcome.get_result()
    
    # report.caplog = "caplog"
    # report.capstdout = "capstdout"
    report.sections.append('t1')
    report.nodeid = item.obj.__doc__
    # print('pytest_runtest_makereport')
    return report

    # report = pytest.TestReport.from_item_and_call(item, call)
    # return report

# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     report.item = item

# def pytest_report_header(config: pytest.Config, 
#                          start_path, 
#                          startdir):
#     print("\npytest_report_header")
#     # return 'go', ['1', '2']
#     # return None


# def pytest_collectstart(collector: pytest.Collector):
#     print(f'-{collector.name}')

# def pytest_make_collect_report(collector: pytest.Collector):
#     if '::' in collector.nodeid:
#         print(f'{collector.name}')        

# # def pytest_report_collectionfinish(config: pytest.Config, 
# #                                    start_path,
# #                                    startdir,
# #                                    items: Sequence[pytest.Item]):
# #     pass
# #     # return ("Ok", ["Ok"])


# def pytest_report_teststatus(report: Union[pytest.CollectReport, 
    #                                        pytest.TestReport], 
    #                          config: pytest.Config):
    # # print(report)
    # if report.when == 'call':
    #     outcome = report.outcome
    #     return outcome, 'K', (outcome, {"green": True})

# def pytest_terminal_summary(terminalreporter: _pytest.terminal.TerminalReporter,
#                             exitstatus: int, 
#                             config: pytest.Config):
#     print(config)

# def pytest_make_collect_report(collector: pytest.Collector):
#     print(collector)

# def pytest_runtest_logreport(report: pytest.TestReport):
#     if report.when == 'setup':
#         print()
#     if report.when == 'call':
#         print(' - ')
#     # if report.when == 'call':
#     print(report.item.obj.__doc__)
