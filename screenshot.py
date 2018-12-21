import Quartz
import LaunchServices
from Cocoa import NSURL
import Quartz.CoreGraphics as CG
from PIL import Image


TMP_PATH = '/tmp/screenshot_module_yaniv_delme.png'


def screenshot(region=None):
    """region should be something like: (0, 0, 100, 100).
    The default region is CG.CGRectInfinite (captures the full screen).
    """

    if region is None:
        region = CG.CGRectInfinite
    else:
        region = CG.CGRectMake(*region)

    # Create screenshot as CGImage
    image = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionOnScreenOnly,
        CG.kCGNullWindowID,
        CG.kCGWindowImageDefault)

    dpi = 221  # 72  # FIXME: Should query this from somewhere, e.g for retina displays

    url = NSURL.fileURLWithPath_(TMP_PATH)

    dest = Quartz.CGImageDestinationCreateWithURL(
        url,
        LaunchServices.kUTTypePNG,  # file type
        1,  # 1 image in file
        None
    )

    properties = {
        Quartz.kCGImagePropertyDPIWidth: dpi,
        Quartz.kCGImagePropertyDPIHeight: dpi,
    }

    # Add the image to the destination, characterizing the image with
    # the properties dictionary.
    Quartz.CGImageDestinationAddImage(dest, image, properties)

    # When all the images (only 1 in this example) are added to the destination,
    # finalize the CGImageDestination object.
    Quartz.CGImageDestinationFinalize(dest)

    return Image.open(TMP_PATH)
