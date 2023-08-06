
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
    @property
    def document(self) :
        return conditor.docs_baker.Document(self.src_path, self.doc_name)
    @property
    def composer(self) :
        return conditor.docs_baker.Composer(self.document, self.out_path)
    @property
    def doc_name(self) :
        return self.build.get('doc_baker.doc_name', '_', True)
    @doc_name.setter
    def doc_name(self, doc_name) :
        print('SETTING', doc_name)
        self.build['doc_baker.doc_name'] = doc_name
        return
    @property
    def doc_struct(self) :
        return self.build.get('doc_baker.doc_struct', {}, True)
    @doc_struct.setter
    def doc_struct(self, doc_struct) :
        self.build['doc_baker.doc_struct'] = doc_struct
        return

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
        composer = self.composer
        composer.struct = self.doc_struct
        composer.compose()
        self.build['path.out.sphinx'] = str(self.out_path)
        return
    pass

