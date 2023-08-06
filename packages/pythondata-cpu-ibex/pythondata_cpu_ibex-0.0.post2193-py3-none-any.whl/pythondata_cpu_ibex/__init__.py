import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/lowRISC/ibex"

# Module version
version_str = "0.0.post2193"
version_tuple = (0, 0, 2193)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post2193")
except ImportError:
    pass

# Data version info
data_version_str = "0.0.post2085"
data_version_tuple = (0, 0, 2085)
try:
    from packaging.version import Version as V
    pdata_version = V("0.0.post2085")
except ImportError:
    pass
data_git_hash = "873e2281cf9332e47119f61b2c1e32aa22c6d58e"
data_git_describe = "v0.0-2085-g873e2281"
data_git_msg = """\
commit 873e2281cf9332e47119f61b2c1e32aa22c6d58e
Author: zeeshanrafique23 <zeeshanrafique23@gmail.com>
Date:   Fri Sep 24 00:14:48 2021 +0500

    remove unused RD in branch insn from tracer

"""

# Tool version info
tool_version_str = "0.0.post108"
tool_version_tuple = (0, 0, 108)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post108")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_ibex."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_ibex".format(f))
    return fn
