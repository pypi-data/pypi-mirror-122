__version__ = '0.5.1'
git_version = '8b4908b3e6235ea6641ba13be5cebfb9536420d3'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
