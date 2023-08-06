import os
import traceback
import zipfile
import io
import urllib.request

import distro

# List is based on this workflow:
# https://github.com/Traceableai/libtraceable/blob/main/.github/workflows/build.yaml#L14-L43
from traceableai.filter import build

supported_platform_version = {
    "debian": {
        "os": "ubuntu",
        "versions": {
            "10": "18.04"
        }
    },
    "ubuntu": {
        "os": "ubuntu",
        "versions": {
            "18.04": "18.04",
            "20.04": "20.04"
        }
    },
    "centos": {
        "os": "centos",
        "versions": {
            "7": "7",
            "8": "8"
        }
    },
    # Disable alpine support for now
    # "alpine": {
    #     "os": "alpine",
    #     "versions": {
    #         "3.9": "3.9",
    #         "3.12": "3.12",
    #     }
    # },
    "amzn": {
        "os": "centos",
        "versions": {
            "2": "7"
        }
    }
}

LIBTRACEABLE_VERSION = "0.1.97"
SOURCE_BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'filter')
DEFAULT_URL = "https://downloads.traceable.ai/install/libtraceable"
if 'TA_LIBTRACEABLE_URL' in os.environ:
    if len(os.environ['TA_LIBTRACEABLE_URL']) > 0:
        URL = os.environ['TA_LIBTRACEABLE_URL']
    else:
        URL = DEFAULT_URL
else:
    URL = DEFAULT_URL


def download_authenticated(platform, version, directory):
    libtraceable_name = f"libtraceable_{platform}_{version}_x86_64"
    filename = f"{libtraceable_name}-{LIBTRACEABLE_VERSION}.zip"
    url = f"{URL}/{libtraceable_name}/{LIBTRACEABLE_VERSION}/{filename}"

    username = os.environ["TA_BASIC_AUTH_USER"]
    password = os.environ["TA_BASIC_AUTH_TOKEN"]

    pass_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    pass_manager.add_password(None, url, username, password)
    authhandler = urllib.request.HTTPBasicAuthHandler(pass_manager)

    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)

    response = urllib.request.urlopen(url)  # pylint:disable=R1732
    return _extract_library_files(response, directory)


def download(platform, version, directory):
    print('downloading from public repo')
    libtraceable_name = f"libtraceable_{platform}_{version}_x86_64"
    filename = f"{libtraceable_name}-{LIBTRACEABLE_VERSION}.zip"
    url = f"{URL}/{libtraceable_name}/{LIBTRACEABLE_VERSION}/{filename}"
    response = urllib.request.urlopen(url)  # pylint:disable=R1732
    return _extract_library_files(response, directory)


def install_lib_traceable(directory=SOURCE_BUILD_DIR):
    try:
        platform = distro.id()
        version = distro.version()
        print(f"Platform: {platform}")
        print(f"Version: {version}")

        support_dict = supported_platform_version.get(platform, None)
        if support_dict is None:
            print(f"libtraceable is not supported on this platform - {platform}-{version}")
            return

        download_version = supported_version(version, support_dict)
        if download_version is None:
            print(f"libtraceable is not supported on this version of this platform {platform}-{version}")
            return

        platform = support_dict["os"]
        print(f"Attempting to download libtraceable for {platform}_{download_version}")
        if "TA_BASIC_AUTH_USER" in os.environ and "TA_BASIC_AUTH_TOKEN" in os.environ:
            download_authenticated(platform, download_version, directory)
        else:
            download(platform, download_version, directory)
        build(directory)
        print("Done downloading - attempting build")
    except:  # pylint:disable=W0702
        print("Failed to download libtraceable %s", traceback.format_exc())
        # if we fail to install or build we don't want to break pip install


def supported_version(actual_version, support_dict):
    supported_versions = support_dict['versions']
    for version_key in supported_versions:
        if actual_version.startswith(version_key):
            return supported_versions[version_key]

    return supported_versions[list(supported_versions.keys())[0]]


def _extract_library_files(response, directory):
    print("extracting library files")
    with zipfile.ZipFile(io.BytesIO(response.read())) as archive:
        for zip_info in archive.infolist():
            if zip_info.filename[-1] == '/':
                continue
            print(f"extracted: {zip_info.filename}")
            zip_info.filename = os.path.basename(zip_info.filename)
            archive.extract(zip_info, directory)
