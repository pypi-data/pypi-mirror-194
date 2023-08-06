
import pathlib


def iter_tree_func(tree_root, node_func, delta='.') :
    tree_root = pathlib.Path(tree_root).resolve()
    tree_current = tree_root.joinpath(delta).resolve()
    for node in tree_current.iterdir() :
        delta = str(node.relative_to(tree_root))
        if not node_func(delta) :
            continue
        if node.is_dir() :
            iter_tree_func(tree_root, node_func, delta)
        pass
    return

#def clone_tree_struct(src_root, dst_root, delta='.') :
#    """Clones a file tree structure."""
#    src_root = pathlib.Path(src_root).resolve()
#    dst_root = pathlib.Path(dst_root).resolve()
#    src_current = src_root.joinpath(delta).resolve()
#    dst_current = dst_root.joinpath(delta).resolve()
#    dst_current.mkdir(parents=True, exist_ok=True)
#    for child in src_current.iterdir() :
#        delta = str(child.relative_to(src_root))
#        print(src_root, dst_root, delta)
#        if child.is_dir() :
#            clone_tree_struct(src_root, dst_root, delta)
#            continue
#        pass
#    return

def copy_file(src, dst) :
    print('COPY', src, dst)
    return

def link_file(src, dst) :
    #print('LINK', src, dst)
    dst.symlink_to(src)
    return

def fallback_allow(delta) :
    return True

def clone_tree(src_root, dst_root, allow_func=fallback_allow, file_func=link_file) :
    # todo: allow fnc return file handle fnc
    def node_func(delta) :
        src_path = src_root.joinpath(delta).resolve()
        dst_path = dst_root.joinpath(delta).resolve()
        if not allow_func(delta) :
            return False
        if src_path.is_file() :
            file_func(src_path, dst_path)
            return True
        if src_path.is_dir() :
            dst_path.mkdir(parents=True, exist_ok=True)
            return True
        return True
    iter_tree_func(src_root, node_func)
    return





