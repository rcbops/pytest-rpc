import json
import uuid
import re
from time import sleep


def get_osa_version(branch):
    """Get OpenStack version (code_name, major_version)

    This data is based on the git branch of the test suite being executed

    Arge:
        branch (str): The rpc-openstack branch to query for.

    Returns:
        tuple of (str, str): (code_name, major_version) OpenStack version.
                             These strings will be empty if the branch is
                             unknown.
    """

    if branch in ['newton', 'newton-rc']:
        return 'Newton', '14'
    elif branch in ['pike', 'pike-rc']:
        return 'Pike', '16'
    elif branch in ['queens', 'queens-rc']:
        return 'Queens', '17'
    elif branch in ['rocky', 'rocky-rc']:
        return 'Rocky', '18'
    else:
        return '', ''


def get_id_by_name(service_type, service_name, run_on_host):
    """Get the id associated with name

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object instance to query
                            for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Returns:
        str: Id of Openstack object instance. None if result not found.
    """

    resources = get_resource_list_by_name(service_type, run_on_host)
    if not resources:
        return

    try:
        matches = [x for x in resources if x['Name'] == service_name]
    except (KeyError, TypeError):
        try:
            matches = [x for x in resources if x['Display Name']
                       == service_name]
        except (KeyError, TypeError):
            return

    if not matches:
        return

    result = matches[0]

    if 'ID' in result.keys():
        return result['ID']
    else:
        return


def create_bootable_volume(data, run_on_host):
    """Create a bootable volume using a json file

    Args:
        data (dict): Dictionary in the following format:
                     { 'volume': { 'size': '',
                                   'imageref': '',
                                   'name': '',
                                   'zone': '',
                                 }
                     }
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Returns:
        str: The id of the created resource

    Raises:
        AssertionError: If failed to create the resource
    """

    cmd = (". ~/openrc ; "
           "openstack volume create "
           "-f json "
           "--size {} "
           "--image {} "
           "--availability-zone {} "
           "--bootable {}".format(data['volume']['size'],
                                  data['volume']['imageref'],
                                  data['volume']['zone'],
                                  data['volume']['name']))

    output = run_on_container(cmd, 'utility', run_on_host)

    try:
        result = json.loads(output.stdout)
    except ValueError:
        result = output.stdout

    assert type(result) is dict
    assert 'id' in result

    return result['id']


def get_resource_list_by_name(name, run_on_host):
    """Get a list of OpenStack object instances of given type.

    Args:
        name (str): The OpenStack object type to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Returns:
        list of dict: OpenStack object instances parsed from JSON
    """

    cmd = (". ~/openrc ; "
           "openstack {} list -f json".format(name))
    output = run_on_container(cmd, 'utility', run_on_host)
    try:
        result = json.loads(output.stdout)
    except ValueError:
        result = []
    return result


def delete_volume(volume_name, run_on_host, addl_flags=''):
    """Delete OpenStack volume

    Args:
        volume_name (str): OpenStack volume identifier (name or id).
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.
        addl_flags (str): Add additional flags to the call to OpenStack CLI
            when deleting a volume.

    Raises:
        AssertionError: If operation unsuccessful.
    """

    delete_it('volume', volume_name, run_on_host, addl_flags=addl_flags)


def parse_table(ascii_table):
    """Parse an OpenStack ascii table

    Args:
        ascii_table (str): OpenStack ascii table.

    Returns:
        list of str: Column headers from table.
        list of str: Rows from table.
    """
    header = []
    data = []
    for line in filter(None, ascii_table.split('\n')):
        if '-+-' in line:
            continue
        if not header:
            header = list(filter(lambda x: x != '|', line.split()))
            continue
        data_row = []
        splitted_line = list(filter(lambda x: x != '|', line.split()))
        for i in range(len(splitted_line)):
            data_row.append(splitted_line[i])
        while len(data_row) < len(header):
            data_row.append('')
        data.append(data_row)
    return header, data


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


def get_expected_value(resource_type,
                       resource_name,
                       key,
                       expected_value,
                       run_on_host,
                       retries=10,
                       case_insensitive=True):
    """Getting an expected status after retries

    Args:
        resource_type (str): The OpenStack object type to query for.
        resource_name (str): The name of the OpenStack object instance to query
            for.
        key (str): The OpenStack object instance parameter to check against.
        expected_value (str): The expected value for the given key.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.
        retries (int): The maximum number of retry attempts.
        case_insensitive (bool): Flag for controlling whether to match case
            sensitive or not for the 'expected_value'.

    Returns:
        bool: Whether the expected value was found or not.
    """

    for i in range(0, retries):
        sleep(6)
        cmd = (". ~/openrc ; "
               "openstack {} show \'{}\' "
               "-f json".format(resource_type, resource_name))
        output = run_on_container(cmd, 'utility', run_on_host)

        try:
            result = json.loads(output.stdout)
        except ValueError as e:
            result = str(e)
            continue

        if key in result:
            if result[key] == expected_value:
                return True
            elif result[key].lower() == expected_value and case_insensitive:
                return True
            else:
                continue
        else:
            print("\n Key not found: {}\n".format(key))
            break

    # Printing out logs if failed
    print("\n===== Debug: get_expected_value logs =====")
    # noinspection PyUnboundLocalVariable
    print("\ncmd = {}".format(cmd))
    # noinspection PyUnboundLocalVariable
    print("\nOutput:\n {}".format(result))
    print("\n===== End of get_expected_value logs =====")

    return False


def delete_instance(instance_name, run_on_host):
    """Delete OpenStack instance

    Args:
        instance_name (str): OpenStack server identifier (name or id).
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Raises:
        AssertionError: If operation unsuccessful.
    """

    delete_it('server', instance_name, run_on_host)


def create_instance(data, run_on_host):
    """Create an instance from source (a glance image or a snapshot)

    Args:
        data (dict): Dictionary in the following format:
                    data = {
                        "instance_name": 'instance_name',
                        "from_source": 'image',
                        "source_name": 'image_name',
                        "flavor": 'flavor',
                        "network_name": 'network',
                    }
        run_on_host (testinfra.host.Host): A hostname where the command is being
            executed.

    Returns:
        str: The id of the created resource

    Raises:
        AssertionError: If failed to create the resource

    Example:
    `openstack server create --image <image_id> flavor <flavor> \
        --nic <net-id=network_id> server/instance_name` \
    `openstack server create --snapshot <snapshot_id> flavor <flavor> \
        --nic <net-id=network_id> server/instance_name`
    """
    source_id = get_id_by_name(data['from_source'],
                               data['source_name'],
                               run_on_host)
    network_id = get_id_by_name('network', data['network_name'], run_on_host)

    cmd = (". ~/openrc ; "
           "openstack server create "
           "-f json "
           "--{} {} "
           "--flavor {} "
           "--nic net-id={} {}".format(data['from_source'],
                                       source_id, data['flavor'],
                                       network_id,
                                       data['instance_name']))

    output = run_on_container(cmd, 'utility', run_on_host)

    try:
        result = json.loads(output.stdout)
    except ValueError:
        result = output.stdout

    assert type(result) is dict
    assert 'id' in result

    return result['id']


def _resource_in_list(service_type,
                      service_name,
                      expected_resource,
                      run_on_host,
                      retries=10):
    """Verify if a volume/server/image is existing

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        expected_resource (bool): Whether or not the resource is expected in the
            list.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.
        retries (int): The maximum number of retry attempts.

    Returns:
        bool: Whether the expected resource was found or not.
    """

    sleep_timeout = 2

    for i in range(0, retries):

        res_id = get_id_by_name(service_type, service_name, run_on_host)

        # Expecting that a resource IS in the list, for example after creating
        # a resource, it is not shown in the list until several seconds later,
        # retry every SLEEP seconds until reaching max retries (default = 10)
        # to ensure the expected resource seen in the list.
        if expected_resource:
            if res_id:
                return True
            else:
                sleep(sleep_timeout)

        # Expecting that a resource is NOT in the list, for example after
        # deleting a resource, it is STILL shown in the list until several
        # seconds later, retry every SLEEP seconds until reaching max retries
        # (default = 10) to ensure the resource is removed from the list
        else:
            if not res_id:
                return True
            else:
                sleep(sleep_timeout)
    return False


def resource_is_in_the_list(service_type, service_name, run_on_host):
    """ Verify if the resource is IN the list

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.

    Returns:
        bool: True if the resource is IN the list, False if the resource is not
            in the list
    """

    return _resource_in_list(service_type, service_name, True, run_on_host)


def resource_not_in_the_list(service_type, service_name, run_on_host):
    """ Verify if the resource in NOT in the list

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.

    Returns:
        bool: True if the resource is NOT in the list, False if the resource is
            in the list
    """

    return _resource_in_list(service_type, service_name, False, run_on_host)


def stop_server_instance(instance_name, run_on_host):
    """Stop an OpenStack server/instance

    Args:
        instance_name (str): The name of the OpenStack instance to be stopped.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.

    Raises:
        AssertionError: If operation is unsuccessful.
    """
    instance_id = get_id_by_name('server', instance_name, run_on_host)

    cmd = (". ~/openrc ; "
           "openstack server stop {}".format(instance_id))

    assert run_on_container(cmd, 'utility', run_on_host).rc == 0


def create_snapshot_from_instance(snapshot_name, instance_name, run_on_host):
    """Create snapshot on an instance

    Args:
        snapshot_name (str): The name of the OpenStack snapshot to be created.
        instance_name (str): The name of the OpenStack instance from which the
            snapshot is created.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.

    Returns:
        str: The id of the created resource

    Raises:
        AssertionError: If failed to create the resource
    """

    instance_id = get_id_by_name('server', instance_name, run_on_host)
    cmd = (". ~/openrc ; "
           "openstack server image create "
           "-f json "
           "--name {} {}".format(snapshot_name, instance_id))

    output = run_on_container(cmd, 'utility', run_on_host)

    try:
        result = json.loads(output.stdout)
    except ValueError:
        result = output.stdout

    assert type(result) is dict
    assert 'id' in result

    return result['id']


def delete_it(service_type, service_name, run_on_host, addl_flags=''):
    """Delete an OpenStack object

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.
        addl_flags (str): Additional flags to pass to the openstack command

    Raises:
        AssertionError: If operation is unsuccessful.
    """

    service_id = get_id_by_name(service_type, service_name, run_on_host)
    cmd = (". ~/openrc ; "
           "openstack {} delete "
           "{} "
           "{}".format(service_type, addl_flags, service_id))

    assert run_on_container(cmd, 'utility', run_on_host).rc == 0
    assert (resource_not_in_the_list(service_type, service_name, run_on_host))


def create_floating_ip(network_name, run_on_host):
    """Create floating IP on a network

    Args:
        network_name (str): The name of the OpenStack network object on which
            the floating IP is created.
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.

    Returns:
        str: The newly created floating ip name

    Raises:
        AssertionError: If operation is unsuccessful.
    """

    network_id = get_id_by_name('network', network_name, run_on_host)
    assert network_id is not None

    cmd = (". ~/openrc ; "
           "openstack floating ip create -f json {}".format(network_id))
    output = run_on_container(cmd, 'utility', run_on_host)

    assert (output.rc == 0)

    try:
        result = json.loads(output.stdout)
    except ValueError:
        result = output.stdout

    assert type(result) is dict
    key = 'floating_ip_address'
    assert key in result.keys()

    return result[key]


# TODO: What is the specific use case for pinging from utility container?
# TODO: Is no specific use case identified, then this helper is not needed.
def ping_ip_from_utility_container(ip, run_on_host):
    """Verify the IP address can be pinged from utility container on a host

    Args:
        ip (str): The string of the pinged IP address
        run_on_host (testinfra.Host): Testinfra host object to execute the
            action on.

    Returns:
        bool: Whether the IP address can be pinged or not
    """

    cmd = "ping -c1 {}".format(ip)
    if run_on_container(cmd, 'utility', run_on_host).rc == 0:
        return True
    else:
        return False


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
