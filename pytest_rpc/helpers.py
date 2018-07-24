import sh
import json
import uuid
import re
from time import sleep

utility_container = ("lxc-attach -n $(lxc-ls -1 | grep utility | head -n 1) "
                     "-- bash -c '. /root/openrc ; ")


def get_git_branch():
    """Retrieve current git branch name of calling repo

    Returns:
        str: current git branch name
    """

    git = sh.git.bake(_cwd='.')
    return git('rev-parse', '--abbrev-ref', 'HEAD')


def get_osa_version_tuple():
    """Get tuple of OpenStack version (code_name, major_version) as raw
    strings.

    This data is based on the git branch of the test suite being executed
    Returns:
        tuple: (code_name, major_version) as raw strings of OpenStack version
    """

    cur_branch = get_git_branch()

    if cur_branch in ['newton', 'newton-rc']:
        return (r'Newton', r'14')
    elif cur_branch in ['pike', 'pike-rc']:
        return (r'Pike', r'16')
    elif cur_branch in ['queens', 'queens-rc']:
        return (r'Queens', r'17')
    elif cur_branch == 'master-rc':
        return (r'Queens', r'17')
    else:
        return (r'\w+', r'\d+')


def get_id_by_name(service_type, service_name, run_on_host):
    """Get the id associated with name

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object instance to query
                            for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Returns:
        string: Id of Openstack object instance. None if result not found.
    """
    cmd = "{} openstack {} show \'{}\' -f json'".format(utility_container,
                                                        service_type,
                                                        service_name)
    output = run_on_host.run(cmd)
    try:
        result = json.loads(output.stdout)
    except ValueError:
        return

    if 'id' in result:
        return result['id']
    else:
        return


def create_bootable_volume(data, run_on_host):
    """Create a bootable volume using a json file

    Args:
        data (dictionary): Dictionary in the following format:
                           { 'volume': { 'size': '',
                                         'imageRef': '',
                                         'name': '',
                                         'zone': '',
                                       }
                           }
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Raises:
        AssertionError: If operation unsuccessful.
    """

    volume_size = data['volume']['size']
    imageRef = data['volume']['imageRef']
    volume_name = data['volume']['name']
    zone = data['volume']['zone']

    cmd = "{} openstack volume create \
           --size {} \
           --image {} \
           --availability-zone {} \
           --bootable {}'".format(utility_container, volume_size, imageRef,
                                  zone, volume_name)
    run_on_host.run_expect([0], cmd)


def openstack_name_list(name, run_on_host):
    """Get a list of OpenStack object instances of given type.

    Args:
        name (str): The OpenStack object type to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Returns:
        string: List of OpenStack object instances in table format.
    """
    cmd = "{} openstack {} list'".format(utility_container, name)
    output = run_on_host.run(cmd)
    return output.stdout


def delete_volume(volume_name, run_on_host):
    """Delete OpenStack volume

    Args:
        volume_name (str): OpenStack volume identifier (name or id).
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.

    Raises:
        AssertionError: If operation unsuccessful.
    """
    volume_id = get_id_by_name('volume', volume_name, run_on_host)
    cmd = "{} openstack volume delete --purge {}'".format(utility_container,
                                                          volume_id)
    run_on_host.run_expect([0], cmd)

    assert (asset_not_in_the_list('volume', volume_name, run_on_host))


def parse_table(ascii_table):
    """Parse an OpenStack ascii table

    Args:
        ascii_table (str): OpenStack ascii table.

    Returns:
        list: List of column headers from table.
        list: List of column rows from table.
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
        string: Random string of specified length (maximum of 32 characters)
    """
    random_str = str(uuid.uuid4())
    random_str = random_str.upper()
    random_str = random_str.replace("-", "")
    return random_str[0:string_length]  # Return the random_str string.


def get_expected_value(service_type, service_name, key, expected_value,
                       run_on_host, retries=10):
    """Getting an expected status after retries

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object instance to query
                            for.
        key (str): The OpenStack object instance parameter to check against.
        expected_value (str): The expected value for the given key.
        run_on_host (testinfra.Host): Testinfra host object to execute the
                                      action on.
        retries (int): The maximum number of retry attempts.

    Returns:
        boolean: Whether the expected value was found or not.
    """
    for i in range(0, retries):
        sleep(6)
        cmd = "{} openstack {} show \'{}\' -f json'".format(utility_container,
                                                            service_type,
                                                            service_name)
        output = run_on_host.run(cmd)
        try:
            result = json.loads(output.stdout)
        except ValueError as e:
            result = str(e)
            continue

        if key in result:
            if result[key] == expected_value:
                return True
            else:
                continue
        else:
            print("\n Key not found: {}\n".format(key))
            break

    # Printing out logs if failed
    print("\n===== Debug: get_expected_value logs =====")
    print("\ncmd = {}".format(cmd))
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
    instance_id = get_id_by_name('server', instance_name, run_on_host)
    cmd = "{} openstack server delete {}'".format(utility_container,
                                                  instance_id)
    run_on_host.run_expect([0], cmd)

    assert (asset_not_in_the_list('server', instance_name, run_on_host))


def create_instance(data, run_on_host):
    """Create an instance from source (a glance image or a snapshot)

    Args:
        data (dict): a dictionary of data. A sample of data as below:
                    data = {
                        "instance_name": 'instance_name',
                        "from_source": 'image',
                        "source_name": 'image_name',
                        "flavor": 'flavor',
                        "network_name": 'network',
                    }
        run_on_host (testinfra.host.Host): A hostname where the command is being executed.

    Raises:
        AssertionError: If operation is unsuccessful.

    Example:
    `openstack server create --image <image_id> flavor <flavor> --nic <net-id=network_id> server/instance_name`
    `openstack server create --snapshot <snapshot_id> flavor <flavor> --nic <net-id=network_id> server/instance_name`
    """
    source_id = get_id_by_name(data['from_source'], data['source_name'], run_on_host)
    network_id = get_id_by_name('network', data['network_name'], run_on_host)

    cmd = "{} openstack server create --{} {} --flavor {} --nic net-id={} {}'"\
        .format(utility_container, data['from_source'], source_id, data['flavor'], network_id, data['instance_name'])

    run_on_host.run_expect([0], cmd)


def _asset_in_list(service_type, service_name, expected_asset, run_on_host, retries=10):
    """Verify if a volume/server/image is existing

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        expected_asset (bool): Whether or not the asset is expected in the list
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.
        retries (int): The maximum number of retry attempts.

    Returns:
        bool: Whether the expected asset was found or not.
    """

    for i in range(0, retries):

        output = openstack_name_list(service_type, run_on_host)

        # Expecting that asset is in the list, for example after creating an asset, it is not shown in the list until
        # several seconds later, retry every 2 seconds until reaching max retries (default = 10) to ensure the expected
        # asset seen in the list.
        # TODO: Create unit tests for this scenario
        if expected_asset:
            if service_name in output:
                return True
            else:
                sleep(2)

        # Expecting that asset is NOT in the list, for example after deleting an asset, it is STILL shown in the list
        # until several seconds later, retry every 2 seconds until reaching max retries (default = 10) to ensure the
        # asset is removed from the list
        # TODO: Create unit tests for this scenario
        else:
            if service_name not in output:
                return True
            else:
                sleep(2)
    return False


def asset_is_in_the_list(service_type, service_name, run_on_host):
    """ Verify if the asset is IN the list

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.

    Returns:
        bool: True if the asset is IN the list, False if the asset is not in the list

    """
    return _asset_in_list(service_type, service_name, True, run_on_host)


def asset_not_in_the_list(service_type, service_name, run_on_host):
    """ Verify if the asset in NOT in the list

        Args:
            service_type (str): The OpenStack object type to query for.
            service_name (str): The name of the OpenStack object to query for.
            run_on_host (testinfra.Host): Testinfra host object to execute the action on.

        Returns:
            bool: True if the asset is NOT in the list, False if the asset is in the list

        """
    return _asset_in_list(service_type, service_name, False, run_on_host)


def stop_server_instance(instance_name, run_on_host):
    """Stop an OpenStack server/instance

    Args:
        instance_name (str): The name of the OpenStack instance to be stopped.
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.
    """
    instance_id = get_id_by_name('server', instance_name, run_on_host)

    cmd = "{} openstack server stop {}'".format(utility_container, instance_id)
    run_on_host.run_expect([0], cmd)


def create_snapshot_from_instance(snapshot_name, instance_name, run_on_host):
    """Create snapshot on an instance

    Args:
        snapshot_name (str): The name of the OpenStack snapshot to be created.
        instance_name (str): The name of the OpenStack instance from which the snapshot is created.
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.
    """
    instance_id = get_id_by_name('server', instance_name, run_on_host)
    cmd = "{} openstack server image create --name {} {}'".format(utility_container, snapshot_name, instance_id)

    run_on_host.run_expect([0], cmd)


def delete_it(service_type, service_name, run_on_host):
    """Delete an OpenStack object

    Args:
        service_type (str): The OpenStack object type to query for.
        service_name (str): The name of the OpenStack object to query for.
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.

    Raises:
        AssertionError: If operation is unsuccessful. """

    service_id = get_id_by_name(service_type, service_name, run_on_host)
    cmd = "{} openstack {} delete {}'".format(utility_container, service_type, service_id)
    run_on_host.run_expect([0], cmd)

    assert (asset_not_in_the_list(service_type, service_name, run_on_host))


def create_floating_ip(network_name, run_on_host):
    """Create floating IP on a network

    Args:
        network_name (str): The name of the OpenStack network object on which the floating IP is created.
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.

    Raises:
        AssertionError: If operation is unsuccessful.

    Returns:
        str: The newly created floating ip name
        None: If failed to create the floating IP
    """

    network_id = get_id_by_name('network', network_name, run_on_host)
    assert network_id is not None

    cmd = "{} openstack floating ip create {} -f json'".format(utility_container, network_id)
    output = run_on_host.run(cmd)

    assert (output.rc == 0)

    try:
        result = json.loads(output.stdout)
    except ValueError:
        return

    if 'name' in result:
        return result['name']


def ping_ip_from_utility_container(ip, run_on_host):
    """Verify the IP address can be pinged from utility container on a host

    Args:
        ip (str): The string of the pinged IP address
        run_on_host (testinfra.Host): Testinfra host object to execute the action on.

    Returns:
        boolean: Whether the IP address can be pinged or not
    """

    cmd = "{} ping -c1 {}'".format(utility_container, ip)
    output = run_on_host.run(cmd)

    if output.rc == 0:
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
    ===============================================================================
    --> Starting reconnaissance on 3 hosts (object)
    ===============================================================================
    [2018-07-19 15:36:40] Checking ring md5sums
    3/3 hosts matched, 0 error[s] while checking hosts.
    ===============================================================================
    [2018-07-19 15:36:40] Checking swift.conf md5sum
    3/3 hosts matched, 0 error[s] while checking hosts.
    ===============================================================================
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
        dictionary: Swift ring data. Empty dictionary if parse fails.

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
