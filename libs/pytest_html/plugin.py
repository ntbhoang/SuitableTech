# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

from base64 import b64encode, b64decode
import datetime
import json
import os
import pkg_resources
import platform
import sys
import time
import bisect
import hashlib
from operator import itemgetter

from ansi2html import Ansi2HTMLConverter, style
import pytest
from py.xml import html, raw

from . import extras
from . import __version__, __pypi_url__

PY3 = sys.version_info[0] == 3

# Python 2.X and 3.X compatibility
if PY3:
    from html import escape
else:
    from codecs import open
    from cgi import escape

# khoi.ngo begin
def read_env():
    file_path = os.getcwd() + "/data_test/RunEnv.txt".replace("/", os.path.sep)
    setting_environment = open(file_path, "r")
    setting_env = setting_environment.read()
    setting_environment.close()

    newline_delim = "\n"
    tab_delim = "="
    maps = dict()
    items = setting_env.split(newline_delim)
    for i in range (0, len(items)):
        keys_values = items[i].split(tab_delim)
        if (len(keys_values) == 2):
            maps[keys_values[0]] = keys_values[1]       
    return maps      
def tuple_without(original_tuple, element_to_remove):
    new_tuple = []
    for s in original_tuple:
        if not s[0] == element_to_remove:
            new_tuple.append(s)
    return list(new_tuple)

def clear_file_env():
    file_path = os.getcwd() + "/data_test/RunEnv.txt".replace("/", os.path.sep)
    file_env = open(file_path, 'w')
    file_env.truncate()
    file_env.close()

start_time = datetime.datetime.now()
@pytest.fixture(scope='session', autouse=True)
def environment(request):
    # clean up RunEnv.txt
    clear_file_env()
    
    """Provide environment details for HTML report"""
    request.config._environment.extend([
        ('Python', platform.python_version(), '1'),
        ('Platform', platform.platform(), '4'),
        ('Start Time: ', start_time.strftime('%b %d, %Y - %H:%M:%S'), '7')
    ])

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        # always add url to report
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            maps = read_env()
            folder_name = ""
            if len(maps) > 0:
                folder_screen_shot = maps["screen_shot"].split(os.path.sep)
                folder_name = folder_screen_shot[len(folder_screen_shot)-1]
            file_name = (report.nodeid.split("::"))[2] + ".png"
            extra.append(pytest_html.extras.url(folder_name + os.path.sep + file_name))
            extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        report.extra = extra

# khoi.ngo end

def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption('--html', action='store', dest='htmlpath',
                    metavar='path', default=None,
                    help='create html report file at given path.')
    group.addoption('--self-contained-html', action='store_true',
                    help='create a self-contained html file containing all '
                    'necessary styles, scripts, and images - this means '
                    'that the report may not render or function where CSP '
                    'restrictions are in place (see '
                    'https://developer.mozilla.org/docs/Web/Security/CSP)')


def pytest_configure(config):
    config._environment = []
    htmlpath = config.option.htmlpath
    # prevent opening htmlpath on slave nodes (xdist)
    if htmlpath and not hasattr(config, 'slaveinput'):
        config._html = HTMLReport(htmlpath,
                                  config.getoption('self_contained_html'),
                                  config.pluginmanager
                                  .hasplugin('rerunfailures'))
        config.pluginmanager.register(config._html)
    if hasattr(config, 'slaveoutput'):
        config.slaveoutput['environment'] = config._environment


@pytest.mark.optionalhook
def pytest_testnodedown(node):
    # note that any environments from remote slaves will be replaced with the
    # environment from the final slave to quit
    if hasattr(node, 'slaveoutput'):
        node.config._environment = node.slaveoutput['environment']


def pytest_unconfigure(config):
    html = getattr(config, '_html', None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)


def data_uri(content, mime_type='text/plain', charset='utf-8'):
    if PY3:
        data = b64encode(content.encode(charset)).decode('ascii')
    else:
        data = b64encode(content)
    return 'data:{0};charset={1};base64,{2}'.format(mime_type, charset, data)


class HTMLReport(object):

    def __init__(self, logfile, self_contained, has_rerun):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.abspath(logfile)
        self.test_logs = []
        self.results = []
        self.errors = self.failed = 0
        self.passed = self.skipped = 0
        self.xfailed = self.xpassed = 0
        self.rerun = 0 if has_rerun else None
        self.self_contained = self_contained
        self.start_time = time.time()
#         self.maps = dict()

    class TestResult:

        def __init__(self, outcome, report, self_contained, logfile):
            self.test_id = report.nodeid
            if report.when != 'call':
                self.test_id = '::'.join([report.nodeid, report.when])
            self.time = getattr(report, 'duration', 0.0)
            self.outcome = outcome
            self.additional_html = []
            self.links_html = []
            self.self_contained = self_contained
            self.logfile = logfile

            test_index = hasattr(report, 'rerun') and report.rerun + 1 or 0

            for extra_index, extra in enumerate(getattr(report, 'extra', [])):
                self.append_extra_html(extra, extra_index, test_index)

            self.append_log_html(report, self.additional_html)

            self.row_table = html.tr([
                html.td(self.outcome, class_='col-result'),
                html.td(self.test_id, class_='col-name'),
                html.td('{0:.2f}'.format(self.time), class_='col-duration'),
                html.td(self.links_html, class_='col-links')])

            self.row_extra = html.tr(html.td(self.additional_html,
                                     class_='extra', colspan='5'))

        def __lt__(self, other):
            order = ('Error', 'Failed', 'Rerun', 'XFailed',
                     'XPassed', 'Skipped', 'Passed')
            return order.index(self.outcome) < order.index(other.outcome)

        def create_asset(self, content, extra_index,
                         test_index, file_extension, mode='w'):
            hash_key = ''.join([self.test_id, str(extra_index),
                               str(test_index)]).encode('utf-8')
            hash_generator = hashlib.md5()
            hash_generator.update(hash_key)
            asset_file_name = '{0}.{1}'.format(hash_generator.hexdigest(),
                                               file_extension)
            asset_path = os.path.join(os.path.dirname(self.logfile),
                                      'assets', asset_file_name)
            if not os.path.exists(os.path.dirname(asset_path)):
                os.makedirs(os.path.dirname(asset_path))

            relative_path = '{0}/{1}'.format('assets', asset_file_name)

            with open(asset_path, mode) as f:
                f.write(content)
            return relative_path

        def append_extra_html(self, extra, extra_index, test_index):
            href = None
            if extra.get('format') == extras.FORMAT_IMAGE:
                if self.self_contained:
                    src = 'data:{0};base64,{1}'.format(
                        extra.get('mime_type'),
                        extra.get('content'))
                    self.additional_html.append(html.div(
                        html.img(src=src), class_='image'))
                else:
                    content = extra.get('content')
                    if PY3:
                        content = b64decode(content.encode('utf-8'))
                    else:
                        content = b64decode(content)
                    href = src = self.create_asset(
                        content, extra_index, test_index,
                        extra.get('extension'), 'wb')
                    self.additional_html.append(html.div(
                        html.a(html.img(src=src), href=href),
                        class_='image'))

            elif extra.get('format') == extras.FORMAT_HTML:
                self.additional_html.append(html.div(
                                            raw(extra.get('content'))))

            elif extra.get('format') == extras.FORMAT_JSON:
                content = json.dumps(extra.get('content'))
                if self.self_contained:
                    href = data_uri(content,
                                    mime_type=extra.get('mime_type'))
                else:
                    href = self.create_asset(content, extra_index,
                                             test_index,
                                             extra.get('extension'))

            elif extra.get('format') == extras.FORMAT_TEXT:
                content = extra.get('content')
                if self.self_contained:
                    href = data_uri(content)
                else:
                    href = self.create_asset(content, extra_index,
                                             test_index,
                                             extra.get('extension'))

            elif extra.get('format') == extras.FORMAT_URL:
                href = extra.get('content')

            if href is not None:
                self.links_html.append(html.a(
                    extra.get('name'),
                    class_=extra.get('format'),
                    href=href,
                    target='_blank'))
                self.links_html.append(' ')

        def append_log_html(self, report, additional_html):
            log = html.div(class_='log')
            if report.longrepr:
                for line in str(report.longrepr).splitlines():
                    if not PY3:
                        line = line.decode('utf-8')
                    separator = line.startswith('_ ' * 10)
                    if separator:
                        log.append(line[:80])
                    else:
                        exception = line.startswith("E   ")
                        if exception:
                            log.append(html.span(raw(escape(line)),
                                                 class_='error'))
                        else:
                            log.append(raw(escape(line)))
                    log.append(html.br())

            for header, content in report.sections:
                log.append(' {0} '.format(header).center(80, '-'))
                log.append(html.br())
                content = Ansi2HTMLConverter(inline=False).convert(content,
                                                                   full=False)
                log.append(raw(content))

            if len(log) == 0:
                log = html.div(class_='empty log')
                log.append('No log output captured.')
            additional_html.append(log)

    def _appendrow(self, outcome, report):
        result = self.TestResult(outcome, report, self.self_contained,
                                 self.logfile)
        index = bisect.bisect_right(self.results, result)
        self.results.insert(index, result)
        self.test_logs.insert(index, html.tbody(result.row_table,
                              result.row_extra, class_=result.outcome.lower() +
                              ' results-table-row'))

    def append_passed(self, report):
        if report.when == 'call':
            if hasattr(report, "wasxfail"):
                self.xpassed += 1
                self._appendrow('XPassed', report)
            else:
                self.passed += 1
                self._appendrow('Passed', report)

    def append_failed(self, report):
        if report.when == "call":
            if hasattr(report, "wasxfail"):
                # pytest < 3.0 marked xpasses as failures
                self.xpassed += 1
                self._appendrow('XPassed', report)
            else:
                self.failed += 1
                self._appendrow('Failed', report)
        else:
            self.errors += 1
            self._appendrow('Error', report)

    def append_skipped(self, report):
        if hasattr(report, "wasxfail"):
            self.xfailed += 1
            self._appendrow('XFailed', report)
        else:
            self.skipped += 1
            self._appendrow('Skipped', report)

    def append_other(self, report):
        # For now, the only "other" the plugin give support is rerun
        self.rerun += 1
        self._appendrow('Rerun', report)

    def _generate_report(self, session):
        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time
        numtests = self.passed + self.failed + self.xpassed + self.xfailed
        generated = datetime.datetime.now()

        self.style_css = pkg_resources.resource_string(
            __name__, os.path.join('resources', 'style.css'))
        if PY3:
            self.style_css = self.style_css.decode('utf-8')

#         ansi_css = [
#             '\n/******************************',
#             ' * ANSI2HTML STYLES',
#             ' ******************************/\n']
#         ansi_css.extend([str(r) for r in style.get_styles()])
#         self.style_css += '\n'.join(ansi_css)
#  
#         css_href = '{0}/{1}'.format('assets', 'style.css')
#         html_css = html.link(href=css_href, rel='stylesheet',
#                              type='text/css')
#         if self.self_contained:
            html_css = html.style(raw(self.style_css))

        head = html.head(
            html.meta(charset='utf-8'),
            html.title('Test Report'),
            html_css)

        class Outcome:

            def __init__(self, outcome, total=0, label=None,
                         test_result=None, class_html=None):
                self.outcome = outcome
                self.label = label or outcome
                self.class_html = class_html or outcome
                self.total = total
                self.test_result = test_result or outcome

                self.generate_checkbox()
                self.generate_summary_item()
                self.generate_summary_item_ex()
                self.generate_summary_cell()

            def generate_checkbox(self):
                checkbox_kwargs = {'data-test-result':
                                   self.test_result.lower()}
                if self.total == 0:
                    checkbox_kwargs['disabled'] = 'true'

                self.checkbox = html.input(type='checkbox',
                                           checked='true',
                                           onChange='filter_table(this)',
                                           name='filter_checkbox',
                                           class_='filter',
                                           hidden='true',
                                           **checkbox_kwargs)

            def generate_summary_item_ex(self):
                self.summary_item_ex = html.th(html.div(html.span(self.checkbox),
                                                        html.span('{0}'.format(self.label),col=self.class_html,class_=self.class_html)))

            def generate_summary_cell(self):
                self.sumary_cell = html.td(html.span('{0}'.format(self.total),class_=self.class_html,col=self.class_html))
            
            def generate_summary_item(self):
                self.summary_item = html.span('{0} {1}'.
                                              format(self.total, self.label),
                                              class_=self.class_html)

        outcomes = [Outcome('passed', self.passed),
                    Outcome('skipped', self.skipped),
                    Outcome('failed', self.failed),
                    Outcome('error', self.errors, label='errors'),
                    Outcome('xfailed', self.xfailed,
                            label='expected failures'),
                    Outcome('xpassed', self.xpassed,
                            label='unexpected passes')]

        if self.rerun is not None:
            outcomes.append(Outcome('rerun', self.rerun))

        summary = [html.h2('Summary'), html.p(
            '{0} tests ran in {1:.2f} seconds. '.format(
                numtests, suite_time_delta)),
            html.p('(Un)check the boxes to filter the results.',
                   class_='filter',
                   hidden='true')]

        sum_header = []
        sum_body = []
        for i, outcome in enumerate(outcomes, start=1):
            sum_header.append(outcome.summary_item_ex)
            sum_body.append(outcome.sumary_cell)


        results = [html.h2('Results'), html.table([html.thead(
            html.tr([
                html.th('Result',
                        class_='sortable result initial-sort',
                        col='result'),
                html.th('Test', class_='sortable', col='name'),
                html.th('Duration',
                        class_='sortable numeric',
                        col='duration'),
                html.th('Links')]),
            html.tr([
                html.th('No results found. Try to check the filters',
                    colspan='5')],
                    id='not-found-message', hidden='true'),
            id='results-table-head'),
                self.test_logs], id='results-table')]

        main_js = pkg_resources.resource_string(
            __name__, os.path.join('resources', 'main.js'))
        if PY3:
            main_js = main_js.decode('utf-8')

        body = html.body(
            html.script(raw(main_js)),
            html.p('Report generated on {0} at {1}'.format(
                generated.strftime('%d-%b-%Y'),
                generated.strftime('%H:%M:%S'))),
            onLoad='init()')

        if session.config._environment:
            # khoi.ngo begin
            maps = read_env()
            if len(maps) > 0:
                session.config._environment.append(('Machine', maps["machine"], '3'))
                session.config._environment.append(('Browser: ', maps["browser"], '5'))
                session.config._environment.append(('Language: ', maps["language"], '6'))
                session.config._environment.append(('End Time: ', generated.strftime('%b %d, %Y - %H:%M:%S'), '7a'))
                session.config._environment.append(('Duration Time: ', time.strftime('%H:%M:%S', time.gmtime(suite_time_delta)), '8'))
            # khoi.ngo end 

            environment = set(session.config._environment)
            # remove 'Base URL' from environment
            environment = tuple_without(environment, 'Base URL')
            body.append(html.h1("Suitable Technologies"))
            body.append(html.h3("Automation Execution Report"))
                
            body.append(html.h2('Environment'))

            # khoi.ngo begin
            body.append(html.table(
                [html.tr(html.td(e[0]), html.td(e[1])) 
                for e in sorted(environment, key=itemgetter(2))]
                , id='environment'))
            # khoi.ngo end

        body.extend(summary)
        body.append(
            html.table([
                html.thead(html.tr(sum_header),id='sum-table-head'),
                html.tbody(html.tr(sum_body), id='sum-table-body')
            ],id='sum-table'))
        body.extend(results)

        doc = html.html(head, body)

        unicode_doc = u'<!DOCTYPE html>\n{0}'.format(doc.unicode(indent=2))
        if PY3:
            # Fix encoding issues, e.g. with surrogates
            unicode_doc = unicode_doc.encode('utf-8',
                                             errors='xmlcharrefreplace')
            unicode_doc = unicode_doc.decode('utf-8')
        return unicode_doc

    def _save_report(self, report_content):
        # khoi.ngo begin
        maps = read_env()
        language = ""
        if len(maps) > 0:
            language = maps["language"]
            browser = " " + maps["browser"].split(',')[0].upper()
            platform = " " + maps["platform"]
        file_name = "ST Automation Report "
        self.logfile = self.logfile + os.path.sep + file_name + language + platform + browser+ start_time.strftime(' %b %d %Y %H-%M-%S') + ".html"
        # khoi.ngo end
        
        dir_name = os.path.dirname(self.logfile)
#         assets_dir = os.path.join(dir_name, 'assets')

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
#         if not self.self_contained and not os.path.exists(assets_dir):
#             os.makedirs(assets_dir)

        with open(self.logfile, 'w', encoding='utf-8') as f:
            f.write(report_content)
#         if not self.self_contained:
#             style_path = os.path.join(assets_dir, 'style.css')
#             with open(style_path, 'w', encoding='utf-8') as f:
#                 f.write(self.style_css)

        # clean up RunEnv.txt
        clear_file_env()

    def pytest_runtest_logreport(self, report):
        if report.passed:
            self.append_passed(report)
        elif report.failed:
            self.append_failed(report)
        elif report.skipped:
            self.append_skipped(report)
        else:
            self.append_other(report)

    def pytest_sessionstart(self, session):
        self.suite_start_time = time.time()

    def pytest_sessionfinish(self, session):
        report_content = self._generate_report(session)
        self._save_report(report_content)

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'generated html file: {0}'.format(
            self.logfile))
