
import pathlib
import subprocess
import os

import conditor.recipe
import conditor.compose.file_tree
import conditor.docs_baker
import conditor.docs_baker.build


DEFAULT_RECIPE='Document'

class Document (conditor.recipe.Recipe) :
    STAGES = ['init', 'configure', 'deploy', 'compose', 'build']
    NAME = 'conditor.docs_baker.Document'
    def init(self, build, flavour) :
        build['path.src_origin'] = str(self.project.path.joinpath('./docs').resolve())
        return
    def configure(self, build, flavour) :
        return
    def deploy(self, build, flavour) :
        doc = conditor.docs_baker.build.Document(build)
        doc.deploy_build_tree()
        return
    def compose(self, build, flavour) :
        doc = conditor.docs_baker.build.Document(build)
        doc.clone_source(pathlib.Path(build['path.src_origin']))
        return
    def build(self, build, flavour) :
        doc = conditor.docs_baker.build.Document(build)
        doc.build_document()
        return
    pass

class HTML (Document) :
    def __build(self, build, flavour) :
        return
    pass


