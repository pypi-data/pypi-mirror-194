from setuptools import setup
from setuptools.command.install import install


class install_failure(install):
    """Fail to install."""

    def run(self):
        raise RuntimeError(
            """\

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unfortunately, you tried to install Sciagraph on an
unsupported platform.

You can see the current list of supported platforms,
as well as workarounds like Docker and WSL, at:
https://www.sciagraph.com/docs/reference/supported-platforms/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
        )


def read(path):
    with open(path) as f:
        return f.read()


setup(
    cmdclass={"install": install_failure},
    name="sciagraph",
    version="2022.1.2",
    description=(
        "A production-speed performance and memory profiler "
        + "for data batch processing applications."
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="Proprietary",
    maintainer="Hyphenated Enterprises LLC",
    maintainer_email="itamar@pythonspeed.com",
    url="http://sciagraph.com",
)
