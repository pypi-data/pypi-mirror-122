# coding: utf-8

"""More documentation coming soon !"""

from ..tool import DISVE as VE
from .camera import Camera
from .._global import OptionalModule

try:
  import cv2
except (ModuleNotFoundError, ImportError):
  cv2 = OptionalModule("opencv-python")


class DISVE(Camera):
  def __init__(self,
               camera: str,
               patches: list,
               fields: list = None,
               labels: list = None,
               alpha: float = 3,
               delta: float = 1,
               gamma: float = 0,
               finest_scale: int = 1,
               iterations: int = 1,
               gditerations: int = 10,
               patch_size: int = 8,
               patch_stride: int = 3,
               show_image: bool = False,
               border: float = .1,
               **kwargs) -> None:
    self.niceness = -5
    self.cam_kwargs = kwargs
    Camera.__init__(self, camera, **kwargs)
    self.patches = patches
    self.show_image = show_image
    self.fields = ["x", "y", "exx", "eyy"] if fields is None else fields
    if labels is None:
      self.labels = ['t(s)'] + sum(
          [[f'p{i}x', f'p{i}y'] for i in range(len(self.patches))], [])
    else:
      self.labels = labels
    self.ve_kw = {"alpha": alpha,
                  "delta": delta,
                  "gamma": gamma,
                  "finest_scale": finest_scale,
                  "iterations": iterations,
                  "gditerations": gditerations,
                  "patch_size": patch_size,
                  "patch_stride": patch_stride,
                  "border": border}

  def prepare(self, *_, **__) -> None:
    Camera.prepare(self, send_img=False)
    if self.show_image:
      try:
        flags = cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO
      except AttributeError:
        flags = cv2.WINDOW_NORMAL
      cv2.namedWindow("DISVE", flags)

  def begin(self) -> None:
    t, self.img0 = self.camera.read_image()
    self.ve = VE(self.img0, self.patches, **self.ve_kw)

  def loop(self) -> None:
    t, img = self.get_img()
    if self.inputs and not self.input_label and self.inputs[0].poll():
      self.inputs[0].clear()
      self.ve.img0 = img
      self.img0 = img
      print("[DISVE block] : Resetting L0")
    d = self.ve.calc(img)
    if self.show_image:
      cv2.imshow("DISVE", img)
      cv2.waitKey(5)
    self.send([t - self.t0] + d)

  def finish(self) -> None:
    if self.show_image:
      cv2.destroyAllWindows()
    Camera.finish(self)
