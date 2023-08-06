import conditor.compose.file_tree
import conditor.compose

def clone_tree(context, src_root, dst_root,
    allow_func=conditor.compose.file_tree.fallback_allow,
    clone_func=conditor.compose.file_tree.link_file,
    ignore_patterns=[]) :
    # File handle.
    def handle_file(delta) :
        if not allow_func(delta) :
            return False
        path = src_root.joinpath(delta).resolve()
        # Ignored patterns.
        for pattern in ignore_patterns :
            if path.match(pattern) :
                return False
            pass
        # Clone file from project root to this file.
        def sfs_clone_root_this() :
            src = context['__PROJECT__'].path.joinpath(read_sfs(path)[0]).resolve()
            dst = dst_root.joinpath(delta).with_suffix('').resolve()
            clone_func(src, dst)
            print('SFS: clone', src, '>', dst)
            return False
        sfs = {
                '.__sfs__file_clone_root_this__': sfs_clone_root_this
        }
        if path.suffix in sfs :
            return sfs[path.suffix]()
        return True
    # Run tree clone
    conditor.compose.file_tree.clone_tree(src_root, dst_root, handle_file, clone_func)
    return


def read_sfs(path) :
    text = path.read_text()
    return text.split('\n')

