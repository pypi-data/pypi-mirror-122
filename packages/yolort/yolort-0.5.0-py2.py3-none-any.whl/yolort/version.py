__version__ = '0.5.0'
git_version = '9e6198c7197d01e336997fb7154b244006e52d0f'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
