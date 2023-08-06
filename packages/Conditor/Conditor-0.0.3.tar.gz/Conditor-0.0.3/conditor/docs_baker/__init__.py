
import pathlib
import subprocess
import os
import collections.abc
import json

import conditor.config
import conditor.compose.file_tree
import conditor.compose.sfs


class Fragment (collections.abc.Mapping) :
    def __init__(self, name, parent=None) :
        self.name = name
        self.parent = parent
        self.illegal_fragment_names = ['_*', '.*']
        return
    def __str__(self) :
        return f'{type(self).__name__}({self.ref})'
    def __repr__(self) :
        return f'{type(self).__name__}({repr(self.doc)}, {repr(self.index)}))'
    def __getitem__(self, frag_name) :
        return Fragment(frag_name, self)
    def __iter__(self) :
        return iter(self.list_child_fragments())
    def __len__(self) :
        return len(self.list_child_fragments())
    def list_child_fragments(self) :
        child_fragments = []
        for node in self.path.iterdir() :
            if node.is_dir() :
                for illegal_match in self.illegal_fragment_names :
                    print('CHECK ILLEGAL', node)
                    if node.match(illegal_match) :
                        print('ILLEGAL', node)
                        continue
                child_fragments.append(node.name)
            pass
        return child_fragments
    def list_file_names(self, suffix=False) :
        files = []
        for node in self.path.iterdir() :
            if node.is_file() :
                name = node.name
                if not suffix :
                    name = node.with_suffix('').name
                    pass
                files.append(name)
                pass
            pass
        return files
    def get(self, ref, rel=False) :
        """Get absolute fragment"""
        if rel :
            return self[ref]
        relrefs = ref.split('/')
        frag = self.root
        for relref in relrefs :
            frag = frag[relref]
            pass
        return frag
    @property
    def resources(self) :
        resources_path = self.path.joinpath('resources.json')
        if not resources_path.exists() :
            return []
        resource_globs = json.loads(resources_path.read_text())
        resources = []
        for rel, resource_glob in resource_globs :
            base_path = self.path
            if not rel :
                base_path = self.root.path
                pass
            for node in base_path.glob(resource_glob) :
                resources.append(node)
                pass
            pass
        return resources
    @property
    def root(self) :
        if self.parent is None :
            return self
        return self.parent.root
    @property
    def path(self) :
        return self.parent.path.joinpath(self.name).resolve()
    @property
    def relpath(self) :
        return self.path.relative_to(self.root.path)
    @property
    def ref(self) :
        return f'{self.parent.ref}/{self.name}'
    @property
    def ref_list(self) :
        return self.ref.split('/')
    @property
    def level(self) :
        return self.parent.level + 1
    @property
    def title(self) :
        title_path = self.path.joinpath('title')
        if title_path.exists() :
            return title_path.read_text().split('\n')[0]
        return None
    @property
    def content(self) :
        content_path = self.path.joinpath('content.rst').resolve()
        if content_path.exists() :
            return content_path.read_text()
        return ''
    @property
    def contents(self) :
        contents_path = self.path.joinpath('contents.json').resolve()
        if contents_path.exists() :
            return json.loads(contents_path.read_text())
        return []
    @property
    def pages(self) :
        pages_path = self.path.joinpath('pages.json').resolve()
        if pages_path.exists() :
            return json.loads(pages_path.read_text())
        return []
    pass

class Document (Fragment) :
    def __init__(self, path, name='_') :
        super().__init__(name)
        self._path = pathlib.Path(path).resolve()
        return
    @property
    def path(self) :
        return self._path
    @property
    def ref(self) :
        return self.name
    @property
    def level(self) :
        return 0
    pass

class Composer :
    def __init__(self, doc, path) :
        self.doc = doc
        """Document to compose from."""
        self.path = path
        """Document output path."""
        self.struct = {}
        """Custom document structure."""
        self.headings = [
            ('#', '#'),
            ('=', '='),
            ('*', '*'),
            ('+', '+'),
            ('-', '-'),
            ('`', '`'),
            ('#', ''),
            ('=', ''),
            ('*', ''),
            ('-', ''),
            ('`', '')
        ]
        self.clone_fnc = conditor.compose.file_tree.link_file
        return

    def struct_fix_relatives(self) :
        def sfr() :
            for entry in self.struct :
                if entry == '/' :
                    self.struct[f'{self.doc.ref}'] = self.struct.pop(entry)
                    return True
                if entry[0] == '/' :
                    self.struct[f'{self.doc.ref}{entry}'] = self.struct.pop(entry)
                    return True
                pass
            return False
        while sfr() :
            pass
        return
    def struct_has(self, fragment, entry) :
        if fragment.ref in self.struct :
            return entry in self.struct[fragment.ref]
        return False
    def struct_get(self, fragment, entry, fallback) :
        if self.struct_has(fragment, entry) :
            return self.struct[fragment.ref][entry]
        return fallback

    def compose_fragment_anchor(self, fragment) :
        ref = self.struct_get(fragment, 'ref', fragment.ref)
        return self.cspx_anchor(ref)
    def compose_fragment_heading(self, fragment) :
        title = self.struct_get(fragment, 'title', fragment.title)
        level = self.struct_get(fragment, 'level', fragment.level)
        return self.cspx_heading(title, level)
    def compose_fragment(self, fragment, is_page=False) :
        # Fragment base string
        s = ''
        s += self.compose_fragment_anchor(fragment)
        s += self.compose_fragment_heading(fragment)
        s += '\n'
        s += self.struct_get(fragment, 'content', fragment.content)
        s += '\n'
        # Fragment resources.
        self.clone_fragment_resources(fragment)
        # Fragment contents
        for rel, ref in self.struct_get(fragment, 'contents', fragment.contents) :
            child_fragment = fragment.get(ref, rel)
            s += self.compose_fragment(child_fragment)
            pass
        # Compose a toctree if fragment contains pages.
        if not is_page and len(self.struct_get(fragment, 'pages', fragment.pages)) > 0 :
            s += self.compose_page_toctree(fragment)
            self.compose_child_pages(fragment)
            pass
        return s

    def compose_page_toctree(self, fragment) :
        name = self.struct_get(fragment, 'name', fragment.name)
        locations = []
        for rel, ref in self.struct_get(fragment, 'pages', fragment.pages) :
            page_fragment = fragment.get(ref, rel)
            #page_location = '/'.join(['', *page_fragment.ref_list[1:]])
            locations.append(f'/{self.compose_page_relpath(page_fragment).with_suffix("")}')
            pass
        return self.cspx_toctree(locations, name)
    def compose_page_path(self, fragment) :
        page_path = self.path.joinpath(fragment.relpath).resolve()
        if (
            len(self.struct_get(fragment, 'pages', fragment.pages)) > 0 or
            len(self.struct_get(fragment, 'resources', fragment.resources)) > 0
        ) :
            return page_path.joinpath('index.rst').resolve()
        return page_path.with_suffix('.rst').resolve()
    def compose_page_relpath(self, fragment) :
        return self.compose_page_path(fragment).relative_to(self.path)
    def compose_page(self, fragment) :
        # Compose page content string.
        p = ''
        p += self.compose_fragment(fragment, True)
        # Generate page toctree
        p += self.compose_page_toctree(fragment)
        # Write page content.
        page_path = self.compose_page_path(fragment)
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.touch(exist_ok=True)
        page_path.write_text(p)
        # Generate child pages.
        self.compose_child_pages(fragment)
        return
    def compose_child_pages(self, fragment) :
        for rel, ref in self.struct_get(fragment, 'pages', fragment.pages) :
            child_page = fragment.get(ref, rel)
            self.compose_page(child_page)
            pass
        return

    def clone_fragment_resources(self, fragment) :
        for src_path in fragment.resources :
            delta_path = src_path.relative_to(self.doc.path)
            dst_path = self.path.joinpath(delta_path).resolve()
            if dst_path.exists() :
                continue
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            self.clone_fnc(src_path.resolve(), dst_path)
            pass
        return

    def compose(self, root_fragment=None) :
        if root_fragment is None :
            root_fragment = self.doc
            pass
        # Endure base resources are present.
        self.clone_fragment_resources(self.doc)
        # Compose fragments.
        self.struct_fix_relatives()
        self.compose_page(root_fragment)
        return

    def cspx_toctree(self, locations, name='__unnamed_toctree__') :
        if len(locations) == 0 :
            return ''
        s = f'\n.. toctree::'
        s += f'\n   :name: {name}'
        s += f'\n'
        for location in locations :
            s += f'\n   {location}'
            pass
        s += f'\n'
        return s
    def cspx_anchor(self, ref) :
        s = '\n'.join([
            f'',
            f'.. {ref}:',
            f''
        ])
        return s
    def cspx_heading(self, title, level) :
        if title is None or len(title) == 0:
            return ''
        s = '\n'.join([
            f'',
            f'{self.headings[level][1]}'*len(title),
            f'{title}',
            f'{self.headings[level][0]}'*len(title),
            f''
        ])
        return s
    pass





