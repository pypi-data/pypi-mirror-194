
import pathlib
import subprocess
import os

import conditor.recipe
import conditor.compose.file_tree

import conditor.sphinx.build

DEFAULT_RECIPE = 'Document'


class Document (conditor.recipe.Recipe) :
    STAGES = ['init', 'configure', 'deploy', 'compose', 'build']
    NAME = 'conditor.sphinx.Document'
    def init(self, build, flavour) :
        return
    def configure(self, build, flavour) :
        return
    def deploy(self, build, flavour) :
        doc = conditor.sphinx.build.Document(build)
        doc.deploy_build_tree()
        return
    def compose(self, build, flavour) :
        source_path = pathlib.Path(build.get('path.source_origin', str(self.project.path.joinpath('./docs').resolve()), True))
        doc = conditor.sphinx.build.Document(build)
        doc.clone_source(source_path)
        conf_dst = doc.src_path.joinpath('./conf.py')
        conf_src = build.get('path.conf_origin', str(self.project.path.joinpath('./decs/conf.py').resolve()))
        conditor.compose.file_tree.link_file(conf_src, conf_dst)
        return
    def build(self, build, flavour) :
        doc = conditor.sphinx.build.Document(build)
        doc.build_document()
        return
    pass

class HTML (Document) :
    NAME = 'conditor.sphinx.HTML'
    def _build(self, build, flavour) :
        return
    pass


class _Document (conditor.recipe.Recipe) :
    STAGES = ['configure', 'deploy', 'build']
    NAME = 'conditor.sphinx.Document'
    def configure(self, build, flavour) :
        build['path.docs_source'] = str(self.project.path.joinpath('./docs').resolve())
        build['paths.python_source_dirs'] = [str(self.project.path.joinpath('./src').resolve())]
        build['relpath.build.src_tree'] = './src'
        build['relpath.build.out_tree'] = './out'
        return
    def deploy(self, build, flavour) :
        docs_source = pathlib.Path(build['path.docs_source']).resolve()
        src_tree = build.path.joinpath(build['relpath.build.src_tree']).resolve()
        out_tree = build.path.joinpath(build['relpath.build.out_tree']).resolve()
        # Create directories.
        src_tree.mkdir(parents=True, exist_ok=True)
        out_tree.mkdir(parents=True, exist_ok=True)
        # Clone source tree.
        conditor.composer.file_tree.clone_tree(docs_source, src_tree)
        return
    def build(self, build, flavour) :
        print('BUILD BASE')
        return
    pass

class _HTML (_Document) :
    NAME = 'conditor.sphinx.HTML'
    def build(self, build, flavour) :
        src_tree = build.path.joinpath(build['relpath.build.src_tree']).resolve()
        out_tree = build.path.joinpath(build['relpath.build.out_tree']).resolve()
        #Compose Build Command
        p_cmd = ['sphinx-build', '-a',
            '-b', 'html',
            '-c', src_tree, #Location of conf.py
            src_tree,
            out_tree
        ]
        #Modify build environment.
        p_env = os.environ.copy()
        p_env['PYTHONPATH'] = ' '.join(build['paths.python_source_dirs'])
        #Execute build.
        p = subprocess.run(p_cmd,
            cwd = build.path,
            env = p_env
        )
        #print(p)
        return
    pass

