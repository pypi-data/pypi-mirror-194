import pkg_resources
from distutils.version import StrictVersion
import json
import requests


def warn_if_old(mod_name):
    this_version = pkg_resources.get_distribution(mod_name).version



    # https://stackoverflow.com/a/27239645/6596010
    def versions(package_name):
        url = "https://pypi.org/pypi/%s/json" % (package_name,)
        data = json.loads(requests.get(url).text)
        versions = list(data["releases"].keys())
        versions.sort(key=StrictVersion)
        return versions


    online_versions = versions(mod_name)
    latest_version = online_versions[len(online_versions) - 1]
    if (this_version != latest_version):
        print(
            f"WARNING: You are using {mod_name} {this_version} but the latest version is {latest_version}. In the terminal use `python -m pip install {mod_name} --upgrade` to update."
        )
