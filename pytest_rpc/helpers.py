import sh


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
