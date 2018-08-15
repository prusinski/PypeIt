"""
Version checking.
"""

from __future__ import absolute_import, division, print_function

import pkg_resources

requirements_file = pkg_resources.resource_filename('pypeit', 'requirements.txt')
install_requires = [line.strip().replace('==', '>=') for line in open(requirements_file)
                    if not line.strip().startswith('#') and line.strip() != '']
for requirement in install_requires:
    pkg, version = requirement.split('>=')
    try:
        pv = pkg_resources.get_distribution(pkg).version
    except pkg_resources.DistributionNotFound:
        raise ImportError("Package: {:s} not installed!".format(pkg))
    else:
        if pkg_resources.parse_version(pv) < pkg_resources.parse_version(version):
            print("Version of package {:s} = {:s}".format(pkg, pv))
            raise ImportError("You need version >= {:s}".format(version))
