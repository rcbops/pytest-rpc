# -*- coding: utf-8 -*-
# ======================================================================================================================
# Imports
# ======================================================================================================================
import os
from xml.dom import minidom
from pytest_rpc import ENV_VARS


# ======================================================================================================================
# Classes
# ======================================================================================================================
class DomNode(object):
    def __init__(self, dom):
        self.__node = dom

    def __repr__(self):
        return self.__node.toxml()

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
        __tracebackhide__ = True
        return assert_attr(self.__node, **kwargs)

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
    __tracebackhide__ = True

    def nodeval(node, name):
        anode = node.getAttributeNode(name)
        if anode is not None:
            return anode.value

    expected = dict((name, str(value)) for name, value in kwargs.items())
    on_node = dict((name, nodeval(node, name)) for name in expected)
    assert on_node == expected


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

    def test_multiple_uuid_marks(self, testdir):
        """Verify that 'test_id' property element is present when a test is decorated with multiple UUID marks.
        The plug-in will choose the bottom-most decorator for the 'test_id'. Note: we DO NOT want to cause the test
        run to fail in this scenario.
        """

        # Expect
        test_id1 = 'first'
        test_id2 = 'second'
        test_name = 'test_uuid'

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('{}')
                    @pytest.mark.test_id('{}')
                    def {}():
                        pass
        """.format(test_id1, test_id2, test_name))

        result, dom = runandparse(testdir)
        test_case = dom.find_first_by_tag('testcase')

        # Test
        assert result.ret == 0

        test_case.assert_attr(name=test_name)
        test_case.find_first_by_tag('property').assert_attr(name='test_id', value=test_id2)

    def test_multiple_test_cases_with_uuid_mark_present(self, testdir):
        """Verify that 'test_id' property element is present when multiple tests are decorated with a UUID mark."""

        # Expect
        test_ids = ['first', 'second']
        test_names = ['test_uuid1', 'test_uuid2']

        # Setup
        testdir.makepyfile("""
                    import pytest
                    @pytest.mark.test_id('{}')
                    def {}():
                        pass

                    @pytest.mark.test_id('{}')
                    def {}():
                        pass
        """.format(test_ids[0], test_names[0], test_ids[1], test_names[1]))

        result, dom = runandparse(testdir)
        test_cases = dom.find_by_tag('testcase')

        # Test
        assert result.ret == 0

        for i in range(len(test_cases)):
            test_cases[i].assert_attr(name=test_names[i])
            test_cases[i].find_first_by_tag('property').assert_attr(name='test_id', value=test_ids[i])

    def test_missing_uuid_marks(self, testdir):
        """Verify that 'test_id' property element is absent when a test is NOT decorated with a UUID mark."""

        # Expect
        test_name = 'test_no_uuid'

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
        assert test_case.find_first_by_tag('property') is None
