"""Class to represent a Virtual Machine object.

All VM specifics are self-contained and the class provides methods to
operate on the VM: boot, shutdown, etc.
"""

import os

from perfkitbenchmarker import flags
from perfkitbenchmarker import package_managers
from perfkitbenchmarker import virtual_machine
from perfkitbenchmarker import vm_util
from perfkitbenchmarker.nifty import nifty_disk
from perfkitbenchmarker.nifty import util

FLAGS = flags.FLAGS
REMOTE_KEY_PATH = '.ssh/id_rsa'
DEFAULT_USERNAME = 'root'
SSH_RETRIES = 10
STRIPED_DEVICE = '/dev/md0'
LOCAL_MOUNT_PATH = '/local'

  #def __init__(self, project, zone, machine_type, image, network):

class NiftyVirtualMachine(virtual_machine.BaseVirtualMachine):

  #def __init__(self, vm_spec):
  #def _Create(self):
  def _Delete(self):
      """ Delete a VM instance """
      delete_cmd = [ os.path.join(util.NIFTY_PATH,
          "/bin/nifty-terminate-instances"), 
          ]
  #def __repr__(self):
  #def __str__(self):
  #def CreateScratchDisk(self, disk_spec):
  #def DeleteScratchDisks(self):
  #def WaitForBootCompletion(self):
  #def FormatDisk(self, device_path):
  #def MountDisk(self, device_path, mount_path):
  #def RenderTemplate(self, template_path, remote_path, context, remote_port=22):
  #def RemoteCopy(self, file_path, remote_path='', copy_to=True, remote_port=22):
  #def LongRunningRemoteCommand(self, command, remote_port=22):
  #def RemoteCommand(self, command, remote_port=22,
  #def PushFile(self, source_path, remote_path=''):
  #def PullFile(self, source_path, remote_path=''):
  #def MoveFile(self, target, source_path, remote_path=''):
  #def AuthenticateVm(self):
  #def PushDataFile(self, data_file):
  #def CheckJavaVersion(self):
  #def RemoveFile(self, filename):
  #def GetDeviceSizeFromPath(self, path):
  #def total_memory_kb(self):
  #def DropCaches(self):
  #def GetScratchDir(self, disk_num=0):
  #def num_cpus(self):
  #def TimeToBoot(self):
  #def IsReachable(self, target_vm):
  #def StripeDrives(self, devices, striped_device):
  #def GetLocalDrives(self):
  #def SetupLocalDrives(self, mount_path=LOCAL_MOUNT_PATH):

