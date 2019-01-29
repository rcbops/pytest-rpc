# -*- coding: utf-8 -*-
# ==============================================================================
# Imports
# ==============================================================================
import re
import uuid
from time import sleep
from warnings import warn
from pprint import pformat
from platform import system
from subprocess import call


# ==============================================================================
# Helpers
# ==============================================================================
def expect_os_property(os_api_conn,
                       os_service,
                       os_object,
                       os_prop_name,
                       expected_value,
                       retries=10,
                       show_warnings=True,
                       case_insensitive=True,
                       only_extended_props=False):
    """Test whether an OpenStack object property matches an expected value.

    Note: this function uses an exponential back-off for retries which means the
    more retries specified the longer the wait between each retry. The total
    wait time is on the fibonacci sequence. (https://bit.ly/1ee23o9)

    Args:
        os_api_conn (openstack.connection.Connection): An authorized API
            connection to the 'default' cloud on the OpenStack infrastructure.
        os_service (str): The service to inspect for object state.
            (e.g. 'server', 'network', 'floating_ip')
        os_object (munch.Munch): The OpenStack object to inspect. (Note: this
            can also OpenStack resource types: https://bit.ly/2R7yjbi)
        os_prop_name (str): The name of the OpenStack object property to
            inspect.
        expected_value (str): The expected value for the given property.
        retries (int): The maximum number of retry attempts.
        show_warnings (bool): Flag for displaying warnings while attempting
            validate properties.(VERY NOISY!)
        case_insensitive (bool): Flag for controlling whether to match case
            sensitive or not for the 'expected_value'.
        only_extended_props (bool): Flag for forcing searching of ONLY extended
            OpenStack properties on the given OpenStack object.

    Returns:
        bool: Whether the property matched the expected value.

    Raises:
        RuntimeError: Invalid service specified.
        RuntimeError: The property was not found on the given object.
    """

    try:
        get_service_method = getattr(os_api_conn, "get_{}".format(os_service))
    except AttributeError:
        raise RuntimeError("Invalid '{}' service specified!".format(os_service))

    for attempt in range(1, retries + 1):
        result = get_service_method(os_object.id)

        # Search direct properties and extended properties.
        if not only_extended_props and os_prop_name in result:
            actual_value = str(result[os_prop_name])
        elif 'properties' in result and os_prop_name in result['properties']:
            actual_value = str(result['properties'][os_prop_name])
        else:
            raise RuntimeError(
                "The '{}' property was not "
                "found on the given object!\n\n"
                "Object properties:\n\n"
                "{}".format(os_prop_name, pformat(dict(result), indent=4))
            )

        if actual_value == expected_value:
            return True
        elif actual_value.lower() == expected_value and case_insensitive:
            return True
        else:
            if show_warnings:
                warning_message = (
                    "Validation attempt: #{}\n"
                    "Object ID: '{}'\n"
                    "Property name: '{}'\n"
                    "Expected value: '{}'\n"
                    "Actual value: '{}'".format(
                        attempt,
                        os_object.id,
                        os_prop_name,
                        expected_value,
                        actual_value
                    )
                )
                warn(UserWarning(warning_message))

        sleep(attempt)

    return False


def ping_from_mnaio(host_or_ip, retries=10):
    """Verify that a host can be pinged from the MNAIO deployment host.

    Note: this function uses an exponential back-off for retries which means the
    more retries specified the longer the wait between each retry. The total
    wait time is on the fibonacci sequence. (https://bit.ly/1ee23o9)

    Args:
        host_or_ip (str): A valid hostname or IP address to ping.
        retries (int): The maximum number of retry attempts.

    Returns:
        bool: True if host was successfully pinged otherwise False.
    """

    # Ping command count option as function of OS
    param = '-n' if system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping_from_mnaio -c 1 google.com"
    command = ['ping', param, '1', host_or_ip]

    # Pinging
    for attempt in range(1, retries + 1):
        if call(command) == 0:
            return True

        sleep(attempt)

    return False


def generate_random_string(string_length=10):
    """Generate a random string of specified length string_length.

    Args:
        string_length (int): Size of string to generate.

    Returns:
        str: Random string of specified length (maximum of 32 characters)
    """

    random_str = str(uuid.uuid4())
    random_str = random_str.upper()
    random_str = random_str.replace("-", "")

    return random_str[0:string_length]  # Return the random_str string.


def run_on_container(command, container_type, run_on_host):
    """Run the given command on the given container.

    Args:
        command (str): The bash command to run.
        container_type (str): The container type to run the command on.
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      wrapped command on.

    Returns:
        testinfra.CommandResult: Result of command execution.
    """

    pre_command = ("lxc-attach "
                   "-n $(lxc-ls -1 | grep {} | head -n 1) "
                   "-- bash -c".format(container_type))
    cmd = "{} '{}'".format(pre_command, command)
    return run_on_host.run(cmd)


def run_on_swift(cmd, run_on_host):
    """Run the given command on the swift container.

    Args:
        cmd (str): Command
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      wrapped command on.
    Returns:
        testinfra.CommandResult: Result of command execution.
    """

    command = (". ~/openrc ; "
               ". /openstack/venvs/swift-*/bin/activate ; "
               "{}".format(cmd))
    return run_on_container(command, 'swift', run_on_host)


def parse_swift_recon(recon_out):
    """Parse swift-recon output into list of lists grouped by the content of
    the delimited blocks.

    Args:
        recon_out (str): CLI output from the `swift-recon` command.

    Returns:
        list: List of lists grouped by the content of the delimited blocks

    Example output from `swift-recon --md5` to be parsed:
    ============================================================================
    --> Starting reconnaissance on 3 hosts (object)
    ============================================================================
    [2018-07-19 15:36:40] Checking ring md5sums
    3/3 hosts matched, 0 error[s] while checking hosts.
    ============================================================================
    [2018-07-19 15:36:40] Checking swift.conf md5sum
    3/3 hosts matched, 0 error[s] while checking hosts.
    ============================================================================
    """

    lines = recon_out.splitlines()
    delimiter_regex = re.compile(r'^={79}')
    collection = []

    delimiter_positions = [ind for ind, x in enumerate(lines)
                           if delimiter_regex.match(x)]

    for ind, delimiter_position in enumerate(delimiter_positions):
        if ind != len(delimiter_positions) - 1:  # Are in the last position?
            start = delimiter_position + 1
            end = delimiter_positions[ind + 1]
            collection.append(lines[start:end])
    return collection


def parse_swift_ring_builder(ring_builder_output):
    """Parse the supplied output into a dictionary of swift ring data.
    Args:
        ring_builder_output (str): The output from the swift-ring-builder
                                   command.
    Returns:
        dict of {str: float}: Swift ring data. Empty dictionary if parse fails.

    Example data:
        {'zones': 1.0,
         'replicas': 3.0,
         'devices': 9.0,
         'regions': 1.0,
         'dispersion': 0.0,
         'balance': 0.78,
         'partitions': 256.0}
    """

    swift_data = {}
    swift_lines = ring_builder_output.split('\n')
    matching = [s for s in swift_lines if "partitions" and "dispersion" in s]
    if matching:
        elements = [s.strip() for s in matching[0].split(',')]
        for element in elements:
            v, k = element.split(' ')
            swift_data[k] = float(v)

    return swift_data
