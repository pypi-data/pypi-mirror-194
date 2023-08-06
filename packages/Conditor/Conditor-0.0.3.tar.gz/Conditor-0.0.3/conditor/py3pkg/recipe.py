
import pathlib
import subprocess
import os
import re

import conditor.recipe
import conditor.compose.file_tree
import conditor.py3pkg.build


class Package (conditor.recipe.Recipe) :
    STAGES = ['init', 'configure', 'deploy', 'compose', 'build', 'install']
    NAME = 'conditor.py3pkg.Package'
    def init(self, build, flavour) :
        pkg = conditor.py3pkg.build.Package(build)
        return
    def configure(self, build, flavour) :
        return
    def configure_clone_locals(self, build, local_cfgmgr) :
        for entry in local_cfgmgr :
            if re.fullmatch('py3pkg\..*', entry) :
                build[entry] = local_cfgmgr[entry]
                pass
            pass
        return
    def deploy(self, build, flavour) :
        for entry in build :
            print('ENTRY:', entry, build[entry])
            pass
        pkg = conditor.py3pkg.build.Package(build)
        pkg.deploy_build_tree()
        return
    def compose(self, build, flavour) :
        pkg = conditor.py3pkg.build.Package(build)
        pkg_root = pathlib.Path(build['path.package_source']).resolve()
        pkg.clone_source(pkg_root)
        pkg.compose_pyproject_file()
        pkg.compose_setup_file()
        return
    def build(self, build, flavour) :
        pkg = conditor.py3pkg.build.Package(build)
        pkg.build_package()
        return
    def install(self, build, flavour) :
        pkg = conditor.py3pkg.build.Package(build)
        pkg.install_package()
        return
    pass

