
import pathlib
import subprocess
import os

import conditor.config
import conditor.compose.file_tree
import conditor.compose.sfs


def find_package_sources(*search_paths) :
    sources = []
    for search_path in search_paths :
        search_path = pathlib.Path(search_path).resolve()
        def node(delta) :
            path = search_path.joinpath(delta).resolve()
            if (path.is_dir()
                and conditor.config.LocalConfigManager.has_config_at_path(path)
                and True #has py3pkg entry
            ):
                sources.append(path)
                pass
            return True
        conditor.compose.file_tree.iter_tree_func(search_path, node)
        pass
    return sources


class Package :
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
    def package_path(self) :
        return self.src_path.joinpath('/'.join(self.namespace.split('.'))).resolve()
    @property
    def name(self) :
        return self.build.get('py3pkg.name', self.project.global_config['project.title'], True)
    @name.setter
    def name(self, name) :
        self.build['py3pkg.name'] = name
        return
    @property
    def namespace(self) :
        return self.build.get('py3pkg.namespace', self.project.global_config['project.codename'], True)
    @namespace.setter
    def namespace(self, name) :
        self.build['py3pkg.namespace'] = name
        return
    @property
    def version(self) :
        return self.build.get('py3pkg.version', self.project.global_config['project.version'], True)
    @version.setter
    def version(self, name) :
        self.build['py3pkg.version'] = name
        return
    @property
    def authors(self) :
        return self.build.get('py3pkg.authors', self.compose_authors(self.project.global_config['project.authors']), True)
    def compose_authors(self, conditor_authors, whitelist=None) :
        authors = []
        for author in conditor_authors :
            if whitelist is not None and author[0] not in whitelist :
                continue
            authors.append({'name':author[1], 'email':author[2]})
            pass
        return authors
    @authors.setter
    def authors(self, name) :
        self.build['py3pkg.authors'] = name
        return
    @property
    def scripts(self) :
        return self.build.get('py3pkg.scripts', {})
    @scripts.setter
    def scripts(self, scripts) :
        self.build['py3pkg.scripts'] = scripts
        return
    @property
    def explicit_packages(self) :
        return self.build.get('py3pkg.explicit_packages', [])
    @explicit_packages.setter
    def explicit_packages(self, explicit_packages) :
        self.build['py3pkg.explicit_packages'] = scripts
        return

    def compose_pyproject_str(self) :
        ts = ''
        # Project metadata
        authors = ''
        for author in self.authors :
            authors += ''.join([
                f'\n    {{ ',
                f'name = "{author["name"]}"',
                f' , ',
                f'email = "{author["email"]}"',
                f' }}'
            ])
            pass
        description = self.build.get('py3pkg.description', self.project.global_config['project.description'])
        ts += '\n' + '\n'.join([
            f'[project]',
            f'name = "{self.name}"',
            f'description = "{description}"',
            f'version = "{self.version}"',
            f'authors = [{authors}\n]',
            f'dependencies = [\n]',
        ]) + '\n'
        ts += '\n' + '\n'.join([
            '[tool.setuptools]',
        ])
        if len(self.explicit_packages) > 0 :
            ts += '\npackages = ['
            eps = []
            for ep in self.explicit_packages :
                eps.append(f'"{ep}"')
                pass
            ts += ', '.join(eps)
            ts += ']\n'
            pass
        if len(self.scripts) > 0 :
            script_entries = []
            for script in self.scripts :
                script_entries.append(f'{script} = "{self.scripts[script]}"')
                pass
            ts += '\n' + '\n'.join([
                '[project.scripts]',
                *script_entries
            ]) + '\n'
            pass
        print('#'*80, 'TOML config', '='*80, '\n', ts, '\n', '#'*80)
        return ts
    def compose_pyproject_file(self) :
        toml_path = self.src_path.joinpath('./pyproject.toml').resolve()
        toml_path.write_text(self.compose_pyproject_str())
        return
    def compose_setup_str(self) :
        ss = 'from setuptools import setup\nsetup()'
        return ss
    def compose_setup_file(self) :
        setup_path = self.src_path.joinpath('./setup.py').resolve()
        setup_path.write_text(self.compose_setup_str())
        return

    def deploy_build_tree(self) :
        """Deploy package build environment."""
        # Source and output directory.
        self.src_path.mkdir(parents=True, exist_ok=True)
        self.out_path.mkdir(parents=True, exist_ok=True)
        # Package directory.
        self.package_path.mkdir(parents=True, exist_ok=True)
        return
    def clone_source(self, origin_path) :
        """Clone source tree."""
        ignore_patterns = [
            '__pycache__'
        ]
        conditor.compose.sfs.clone_tree(self.build.context,
            origin_path, self.package_path,
            ignore_patterns=ignore_patterns)
        return
    def build_package(self) :
        """Executes package build."""
        # Build command.
        p_cmd = ['python3', '-m', 'build',
            '--outdir', self.out_path,
            self.src_path
        ]
        # Build environment.
        p_env = os.environ.copy()
        #for e in p_env :
        #    print(e, p_env[e])
        #    pass
        # run build.
        #p_env['DISTUTILS_DEBUG'] = '1'
        p = subprocess.run(p_cmd,
            cwd = self.build.path,
            env = p_env,
            #shell = True
        )
        print(p)
        # Search distribution files.
        for node in self.out_path.iterdir() :
            if node.match('*.whl') :
                self.build['path.build_dist'] = str(node.resolve())
                continue
            if node.match('*.tar.gz') :
                self.build['path.source_dist'] = str(node.resolve())
                continue
            pass
        return
    def install_package(self) :
        """Installs built package."""
        if 'path.build_dist' not in self.build :
            print('NO BUILD DIST'*20)
            return
        build_dist_path = pathlib.Path(self.build['path.build_dist']).resolve()
        # Build command.
        p_cmd = ['python3', '-m', 'pip', 'install',
            '--force-reinstall',
            build_dist_path
        ]
        # Build environment.
        p_env = os.environ.copy()
        # run build.
        p = subprocess.run(p_cmd,
            cwd = self.build.path,
            env = p_env
        )
        return
    pass





