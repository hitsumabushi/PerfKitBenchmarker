from perfkitbenchmarker import flags
from perfkitbenchmarker import network
from perfkitbenchmarker import resource
from perfkitbenchmarker import vm_util
from perfkitbenchmarker.nifty import util
import os

FLAGS = flags.FLAGS

class NiftyFirewall(network.BaseFirewall):
  """An object representing the NIFTY Cloud Firewall."""

  def __init__(self, project):
    """Initialize firewall class.

    Args:
      project: Firewall Policy Group
    """
    self.project = project
    self._lock = threading.Lock()
    self.firewall_ports = []
    self.firewall_name = re.sub(re.compile("[!-/:-@[-`{-~]"),'', project)

  def __getstate__(self):
    """Implements getstate to allow pickling (since locks can't be pickled)."""
    d = self.__dict__.copy()
    del d['_lock']
    return d

  def __setstate__(self, state):
    """Restores the lock after the object is unpickled."""
    self.__dict__ = state
    self._lock = threading.Lock()

  def _createSecurityGroup(self, firewall_name):
      pass
  def _deleteSecurityGroup(self):
      pass

  def AllowPort(self, vm, port):
    """Opens a port on the firewall.

    Args:
      vm: The BaseVirtualMachine object to open the port for.
      port: The local port to open.
    """
    if vm.is_static:
        return
    with self._lock:
        for protocol in ['TCP', 'UDP']:
            for inout in ['IN', 'OUT']:
                firewall_cmd = [os.path.join(util.NIFTY_PATH,
                    '/bin/nifty-authorize-security-group-ingress'),
                    'firewall_name', '-p', port, '-s', '0.0.0.0/0',
                    '-P', protocol, '-in-out', inout
                    ]
                vm_util.IssueRetryableCommand(firewall_cmd)
            self.firewall_ports.append(port)

  def DisallowAllPorts(self):
    """Closes all ports on the firewall."""
    for port in self.firewall_ports:
        for protocol in ['TCP', 'UDP']:
            for inout in ['IN', 'OUT']:
                firewall_cmd = [os.path.join(util.NIFTY_PATH,
                    '/bin/nifty-revoke-security-group-ingress'),
                    'firewall_name', '-p', port, '-s', '0.0.0.0/0',
                    '-P', protocol, '-in-out', inout
                    ]
                vm_util.IssueRetryableCommand(firewall_cmd)
        self.firewall_ports.remove(port)

class NiftyNetwork(network.BaseNetwork):
  """Object representing a NIFTY Cloud Network."""

  def Create(self):
    """Creates the actual network."""
    pass

  def Delete(self):
    """Deletes the actual network."""
    pass

