# -*- coding: utf-8 -*-
# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
import pytest
from lxml import etree
from xml.dom import minidom
from collections import OrderedDict
from pytest_rpc import ENV_VARS, get_xsd
from dateutil import parser as date_parser


# ======================================================================================================================
# Classes
# ======================================================================================================================
class DomNode(object):
    def __init__(self, dom):
        self.__node = dom

    def __repr__(self):
        return self.__node.toxml()

    def node(self):
        return self.__node

    def find_first_by_tag(self, tag):
        return self.find_nth_by_tag(tag, 0)

    def _by_tag(self, tag):
        return self.__node.getElementsByTagName(tag)

    def find_nth_by_tag(self, tag, n):
        items = self._by_tag(tag)
        try:
            nth = items[n]
        except IndexError:
            pass
        else:
            return type(self)(nth)

    def find_by_tag(self, tag):
        t = type(self)
        return [t(x) for x in self.__node.getElementsByTagName(tag)]

    def __getitem__(self, key):
        node = self.__node.getAttributeNode(key)
        if node is not None:
            return node.value

    def assert_attr(self, **kwargs):
        # noinspection PyUnusedLocal
        __tracebackhide__ = True
        return assert_attr(self.__node, **kwargs)

    def get_property_value(self, name):
        for property in self.find_by_tag('property'):
            element = property.node()
            n = element.getAttributeNode('name').value
            if n == name:
                return element.getAttributeNode('value').value

    def toxml(self):
        return self.__node.toxml()

    @property
    def text(self):
        return self.__node.childNodes[0].wholeText

    @property
    def tag(self):
        return self.__node.tagName

    @property
    def next_sibling(self):
        return type(self)(self.__node.nextSibling)


# ======================================================================================================================
# Functions
# ======================================================================================================================
def runandparse(testdir, *args):
    resultpath = testdir.tmpdir.join('junit.xml')
    result = testdir.runpytest("--junitxml={}".format(resultpath), *args)
    xmldoc = minidom.parse(str(resultpath))
    return result, DomNode(xmldoc)


def assert_attr(node, **kwargs):
    # noinspection PyUnusedLocal
    __tracebackhide__ = True

    # noinspection PyShadowingNames
    def nodeval(node, name):
        anode = node.getAttributeNode(name)
        if anode is not None:
            return anode.value

    expected = dict((name, str(value)) for name, value in kwargs.items())
    on_node = dict((name, nodeval(node, name)) for name in expected)
    assert on_node == expected


def property_present(node, name):
    present = False
    for property in node.find_by_tag('property'):
        element = property.node()
        n = element.getAttributeNode('name').value
        if n == name:
            present = True
    return present


# ======================================================================================================================
# Tests
# ======================================================================================================================
class TestTestSuiteXMLProperties(object):
    """Test cases for the 'pytest_runtestloop' hook function for collecting environment variables"""

    def test_no_env_vars_set(self, testdir):
        """Verify that pytest accepts our fixture without setting any environment variables."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    def test_pass():
                        pass
        """)

        result, dom = runandparse(testdir)

        # Test
        assert result.ret == 0
        dom.find_first_by_tag("testsuite").assert_attr(name="pytest", errors=0, failures=0, skips=0, tests=1)

        for i in range(len(ENV_VARS)):
            dom.find_nth_by_tag('property', i).assert_attr(name=ENV_VARS[i], value='Unknown')

    def test_env_vars_set(self, testdir):
        """Verify that pytest accepts our fixture with all relevant environment variables set."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    def test_pass():
                        pass
        """)

        for env in ENV_VARS:
            os.environ[env] = env

        result, dom = runandparse(testdir)

        # Test
        assert result.ret == 0
        dom.find_first_by_tag("testsuite").assert_attr(name="pytest", errors=0, failures=0, skips=0, tests=1)

        for i in range(len(ENV_VARS)):
            dom.find_nth_by_tag('property', i).assert_attr(name=ENV_VARS[i], value=ENV_VARS[i])


class TestTestCaseXMLProperties(object):
    """Test cases for the 'pytest_collection_modifyitems' hook function for recording the UUID for test cases."""

    def test_uuid_mark_present(self, testdir):
        """Verify that 'test_id' property element is present when a test is decorated with a UUID mark."""

        # Expect
        test_id = '123e4567-e89b-12d3-a456-426655440000'
        test_name = 'test_uuid'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('{}')
                    def {}():
                        pass
        """.format(test_id, test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        test_case.find_first_by_tag('property').assert_attr(name='test_id', value=test_id)

    def test_jira_mark_present(self, testdir):
        """Verify that 'jira' property element is present when a test is decorated with a Jira mark."""

        # Expect
        jira_id = 'ASC-123'
        test_name = 'test_jira'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.jira('{}')
                    def {}():
                        pass
        """.format(jira_id, test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        test_case.find_first_by_tag('property').assert_attr(name='jira', value=jira_id)

    def test_multiple_marks(self, testdir):
        """Verify that 'test_id' and 'jira' property elements are present when a test is decorated with multiple marks.
        The plug-in will choose the bottom-most decorator for the marks. Note: we DO NOT want to cause the test
        run to fail in this scenario.
        """

        # Expect
        test_ids = ['first', 'second']
        jira_ids = ['1st', '2nd']
        test_name = 'test_uuid'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('{}')
                    @pytest.mark.test_id('{}')
                    @pytest.mark.jira('{}')
                    @pytest.mark.jira('{}')
                    def {}():
                        pass
        """.format(test_ids[0], test_ids[1], jira_ids[0], jira_ids[1], test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        test_case.find_by_tag('property')[0].assert_attr(name='test_id', value=test_ids[1])
        test_case.find_by_tag('property')[1].assert_attr(name='jira', value=jira_ids[1])

    def test_multiple_test_cases_with_marks_present(self, testdir):
        """Verify that 'test_id' and 'jira' property elements are present when multiple tests are decorated with
        required marks.
        """

        # Expect
        test_info = OrderedDict([('test0_name', 'test_mark1'),
                                 ('test0_test_id', 'first'),
                                 ('test0_jira_id', '1st'),
                                 ('test1_name', 'test_mark2'),
                                 ('test1_test_id', 'second'),
                                 ('test1_jira_id', '2nd')])

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('{test0_test_id}')
                    @pytest.mark.jira('{test0_jira_id}')
                    def {test0_name}():
                        pass

                    @pytest.mark.test_id('{test1_test_id}')
                    @pytest.mark.jira('{test1_jira_id}')
                    def {test1_name}():
                        pass
        """.format(**test_info))

        result, dom = runandparse(testdir)
        test_cases = dom.find_by_tag('testcase')

        # Test
        assert result.ret == 0

        for i in range(len(test_cases)):
            test_cases[i].assert_attr(name=test_info.get('test{}_name'.format(i)))
            test_cases[i].find_by_tag('property')[0].assert_attr(name='test_id',
                                                                 value=test_info.get('test{}_test_id'.format(i)))
            test_cases[i].find_by_tag('property')[1].assert_attr(name='jira',
                                                                 value=test_info.get('test{}_jira_id'.format(i)))

    def test_missing_marks(self, testdir):
        """Verify that 'test_id' and 'jira' property elements are absent when a test is NOT decorated with required
        marks.
        """

        # Expect
        test_name = 'test_no_marks'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    def {}():
                        pass
        """.format(test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        assert not property_present(test_case, 'test_id')
        assert not property_present(test_case, 'jira')

    @pytest.mark.skipif('SKIP_LONG_RUNNING_TESTS' in os.environ, reason='Impatient developer is impatient')
    def test_start_time(self, testdir):
        """Verify that 'start_time' property element is present."""

        # Expect
        test_name = 'test_i_can_has_start_time'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    import time
                    def {}():
                        time.sleep(1)
        """.format(test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        assert property_present(test_case, 'start_time')

    @pytest.mark.skipif('SKIP_LONG_RUNNING_TESTS' in os.environ, reason='Impatient developer is impatient')
    def test_end_time(self, testdir):
        """Verify that 'end_time' property element is present."""

        # Expect
        test_name = 'test_i_can_has_end_time'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    import time
                    def {}():
                        time.sleep(1)
        """.format(test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        assert property_present(test_case, 'end_time')

    @pytest.mark.skipif('SKIP_LONG_RUNNING_TESTS' in os.environ, reason='Impatient developer is impatient')
    def test_accurate_test_time(self, testdir):
        """Verify that '*_time' properties element are accurate."""

        # Expect
        test_name = 'test_i_can_has_a_duration'
        sleep_seconds = 2

        # Setup
        testdir.makepyfile("""
                    import pytest
                    import time
                    def {}():
                        time.sleep({})
        """.format(test_name, sleep_seconds))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        assert property_present(test_case, 'start_time')
        assert property_present(test_case, 'end_time')

        start = date_parser.parse(str(test_case.get_property_value('start_time')))
        end = date_parser.parse(str(test_case.get_property_value('end_time')))
        delta = end - start
        assert delta.seconds == sleep_seconds


class TestXsd(object):
    """Test cases for the 'get_xsd' utility function for retrieving the XSD for the project."""

    test_env_vars = list(ENV_VARS)      # Shallow copy.

    def test_happy_path(self, testdir):
        """Verify that 'get_xsd' returns an XSD stream that can be used to validate JUnitXML."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.jira('ASC-123')
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    def test_xsd():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        xmlschema.assertValid(xml_doc)

    def test_missing_global_property(self, testdir, mocker):
        """Verify that XSD will enforce the presence of all required global test suite properties."""

        # Mock
        # Missing 'BUILD_URL'
        mock_env_vars = [x for x in self.test_env_vars if x != 'BUILD_URL']

        mocker.patch('pytest_rpc.ENV_VARS', mock_env_vars)

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    def test_missing_global_property():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_extra_global_property(self, testdir, mocker):
        """Verify that XSD will enforce the strict presence of only required global test suite properties."""

        # Mock
        # Extra 'BUILD_URL'
        mock_env_vars = self.test_env_vars + ['BUILD_URL']

        mocker.patch('pytest_rpc.ENV_VARS', mock_env_vars)

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    def test_missing_global_property():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_typo_global_property(self, testdir, mocker):
        """Verify that XSD will enforce the only certain property names are allowed for the test suite."""

        # Mock
        # Typo for RPC_RELEASE
        mock_env_vars = [x for x in self.test_env_vars if x != 'RPC_RELEASE'] + ['RCP_RELEASE']

        mocker.patch('pytest_rpc.ENV_VARS', mock_env_vars)

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    def test_missing_global_property():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_missing_required_marks(self, testdir):
        """Verify that XSD will enforce the presence of 'test_id' and 'jira_id' properties for test cases."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    def test_missing_marks():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_missing_uuid_mark(self, testdir):
        """Verify that XSD will enforce the presence of 'test_id' property for test cases."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.jira('ASC-123')
                    def test_missing_uuid():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_missing_jira_mark(self, testdir):
        """Verify that XSD will enforce the presence of 'jira' property for test cases."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    def test_missing_uuid():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        xml_doc = etree.parse(str(resultpath))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_extra_testcase_property(self, testdir):
        """Verify that XSD will enforce the strict presence of only required test case properties."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    @pytest.mark.jira('ASC-123')
                    def test_extra_mark():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        # Add another property element for the testcase.
        xml_doc = etree.parse(str(resultpath))
        xml_doc.getroot().find('./testcase/properties').append(etree.Element('property',
                                                                             attrib={'name': 'extra', 'value': 'fail'}))
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False

    def test_typo_property(self, testdir):
        """Verify that XSD will enforce the only certain property names are allowed for the testcase."""

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('123e4567-e89b-12d3-a456-426655440000')
                    @pytest.mark.jira('ASC-123')
                    def test_extra_mark():
                        pass
        """)

        resultpath = testdir.tmpdir.join('junit.xml')
        result = testdir.runpytest("--junitxml={}".format(resultpath))

        # Add another property element for the testcase.
        xml_doc = etree.parse(str(resultpath))
        xml_doc.getroot().find('./testcase/properties/property').attrib['name'] = 'wrong_test_id'
        xmlschema = etree.XMLSchema(etree.parse(get_xsd()))

        # Test
        assert result.ret == 0
        assert xmlschema.validate(xml_doc) is False
