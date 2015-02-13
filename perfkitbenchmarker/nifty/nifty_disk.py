from perfkitbenchmarker import disk
from perfkitbenchmarker import flags
from perfkitbenchmarker import vm_util
from perfkitbenchmarker.nifty import util
from perfkitbenchmarker import resource

import threading
import os

class NiftyDisk(disk.BaseDisk):
  """Object representing an NIFTY Cloud Disk."""

  _lock = threading.Lock()
  vm_devices = {}

  def __init__(self, disk_spec, zone):
    super(NiftyDisk, self).__init__(disk_spec)
    self.id = None
    self.zone = zone
    self.region = zone[:-1]
    self.attached_vm_id = None

  def _Create(self):
    """Creates the disk."""
    create_cmd = [os.path.join(util.NIFTY_PATH, 'bin/nifty-create-volume'),
                  '--size=%s' % self.disk_size,
                  '--volume-type=%s' % self.disk_type]
    stdout, _ = vm_util.IssueRetryableCommand(create_cmd)
    response = json.loads(stdout)
    self.id = response['VolumeId']
    util.AddDefaultTags(self.id, self.region)

  def _Delete(self):
    """Deletes the disk."""
    delete_cmd = [os.path.join(util.NIFTY_PATH, 'bin/nifty-delete-volume'),
                  '--volume-id=%s' % self.id]
    vm_util.IssueRetryableCommand(delete_cmd)

  def Attach(self, vm):
    """Attaches the disk to a VM.

    Args:
      vm: The NiftyVirtualMachine instance to which the disk will be attached.
    """
    with self._lock:
      self.attached_vm_id = vm.id
      if self.attached_vm_id not in NiftyDisk.vm_devices:
        NiftyDisk.vm_devices[self.attached_vm_id] = set(
            string.ascii_lowercase)
        NiftyDisk.vm_devices[self.attached_vm_id].remove('a')
      self.device_letter = min(NiftyDisk.vm_devices[self.attached_vm_id])
      NiftyDisk.vm_devices[self.attached_vm_id].remove(self.device_letter)
    attach_cmd = [os.path.join(util.NIFTY_PATH, 'bin/nifty-attach-volume'),
                  self.id, '--instance=%s' % self.attached_vm_id]
    vm_util.IssueRetryableCommand(attach_cmd)

  def Detach(self):
    """Detaches the disk from a VM."""
    detach_cmd = [os.path.join(util.NIFTY_PATH, 'bin/nifty-detach-volume'),
                  self.id]
    vm_util.IssueRetryableCommand(detach_cmd)

    with self._lock:
      assert self.attached_vm_id in NiftyDisk.vm_devices
      NiftyDisk.vm_devices[self.attached_vm_id].add(self.device_letter)
      self.attached_vm_id = None
      self.device_letter = None

  def GetDevicePath(self):
    """Returns the path to the device inside the VM."""
    return '/dev/sd%s' % self.device_letter
