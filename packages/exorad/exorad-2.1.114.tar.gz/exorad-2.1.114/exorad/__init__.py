import os.path
from datetime import date

__pkg_name__ = 'exorad'
__title__ = "ExoRad2"
__summary__ = "The generic point source radiometric model"
__url__ = "https://github.com/ExObsSim/ExoRad2-public"

try:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    base_dir = None

__base_dir__ = base_dir
__branch__ = None
if base_dir is not None and os.path.exists(os.path.join(base_dir, ".git")):
    git_folder = os.path.join(base_dir, ".git")
    with open(os.path.join(git_folder, "HEAD")) as fp:
        ref = fp.read().strip()
    ref_dir = ref[5:]
    __branch__ = ref[16:]
    try:
        with open(os.path.join(git_folder, ref_dir)) as fp:
            __commit__ = fp.read().strip()
    except FileNotFoundError:
        __commit__ = None
else:
    __commit__ = None


__author__ = "Lorenzo V. Mugnai, Enzo Pascale"
__email__ = "lorenzo.mugnai@uniroma1.it"

__license__ = "BSD-3-Clause"
__copyright__ = '2020-{:d}, {}'.format(date.today().year, __author__)
__citation__ = "Mugnai et al., 2020, 'ArielRad: the ARIEL radiometric model', Exp. Astron, 50, 303-328"

from .exorad import standard_pipeline


from exorad.utils.version_control import VersionControl
VersionControl()