
import pathlib
import subprocess
import os

import conditor.config
import conditor.compose.file_tree
import conditor.compose.sfs
import conditor.docs_baker

class Document :
    """Ongoing document build."""
    def __init__(self, build) :
        self.build = build
        """Reference to build building this package."""
        return
    @property
    def project(self) :
        return self.build.project
    @property
    def src_path(self) :
        """Path of package source tree."""
        return self.build.path.joinpath(self.build.get('relpath.src_tree', './src')).resolve()
    @property
    def out_path(self) :
        return self.build.path.joinpath(self.build.get('relpath.out_tree', './out')).resolve()
    #def doc_name(self) :
    #    return self.build.get('doc_baker.doc_name', '_', True)
    #@doc_name.setter
    #def doc_name(self, doc_name) :
    #    self.build['doc_baker.doc_name'] = doc_name
    #    return

    def deploy_build_tree(self) :
        """Deploy document build environment."""
        # Source and output directory.
        self.src_path.mkdir(parents=True, exist_ok=True)
        self.out_path.mkdir(parents=True, exist_ok=True)
        return

    def clone_source(self, origin_path) :
        """Clone source tree."""
        ignore_patterns = [
        ]
        conditor.compose.sfs.clone_tree(self.build.context,
            origin_path, self.src_path,
            ignore_patterns=ignore_patterns)
        return
    def build_document(self) :
        """Executes package build."""
        p_cmd = ['sphinx-build', '-a',
            '-b', 'html',
            '-c', self.src_path,
            self.src_path,
            self.out_path
        ]
        #Modify build environment.
        p_env = os.environ.copy()
        pythonpath_list = []
        if 'PYTHONPATH' in p_env :
            pythonpath_list.append(p_env['PYTHONPATH'])
            pass
        pythonpath_list.extend(self.build.get('path.include_pythonpath_roots'))
        p_env['PYTHONPATH'] = os.pathsep.join(pythonpath_list)
        #Execute build.
        p = subprocess.run(p_cmd,
            cwd = self.build.path,
            env = p_env
            )
        return
    pass

