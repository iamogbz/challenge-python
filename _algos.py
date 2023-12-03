class Graph:
    """Graph tree data structure, bidirectional by default"""

    _bidi = True  # defaults to true for undirected graphs
    _data = {}

    def __repr__(self):
        return repr((">" + ("<" if self.is_bidirectional else ">"), self._data))

    def set_bidirectionality(self, enabled: "bool"):
        """Toggle if the graph operations should be bidirectional"""
        self._bidi = enabled

    @property
    def data(self):
        """Data getter"""
        return self._data

    @property
    def binarytree(self):
        """Sort the nodes in a list representing a binary tree"""
        return self.as_binarytree()

    @property
    def is_bidirectional(self):
        """Getter for graph bidirectionality"""
        return self._bidi

    def as_binarytree(self, key=None):
        """
        Get the nodes as an ordered list
        :param key: tree lookup mapping formula
        """
        return sorted(((s, t, v[t]) for s, v in self.data.items() for t in v), key=key)

    def insert(self, source, target, value, reverse=None):
        """Insert source vertex and directed edge to target with weight value"""
        if not self._data.get(source, None):
            self._data[source] = {}
        self._data[source][target] = value

        if reverse is not None:  # or self.is_bidirectional:
            if not self._data.get(target, None):
                self._data[target] = {}
            self._data[target][source] = value if reverse is None else reverse

    def remove(self, source, target):
        """Remove vertex edge from map including the reverse direction if bidirectional"""

        def _remove(s, t):
            if s not in self._data or t not in self._data[s]:
                return
            del self._data[s][t]
            if not self._data[s]:
                del self._data[s]

        _remove(source, target)
        if self.is_bidirectional:
            _remove(target, source)

    def retarget(self, old_target, new_target):
        """Replace all edges to previous source with new target"""
        for src, src_targets in self._data.items():
            if old_target in src_targets:
                self.insert(src, new_target, src_targets[old_target])
                self.remove(src, old_target)

        if self._data.get(old_target, None):
            self._data[new_target] = self._data[old_target]
            del self._data[old_target]

    def get_adjacent(self, node=None):
        """Get all nodes/vertexes directly connected to this one or all when node is None"""
        forward_conns = self._data.get(node, self._data if node is None else {}).keys()

        reverse_conns = set()
        if self.is_bidirectional or node is None:
            for src, src_targets in self._data.items():
                if node in src_targets:  # always false when None
                    reverse_conns.add(src)
                elif node is None:
                    reverse_conns.update(src_targets.keys())

        return [*reverse_conns.union(forward_conns)]

    def get_value(self, source, target):
        """Get weight value for source target edge connection"""
        branch_leaves = set(self._data.get(source, {}).keys())
        if not target in branch_leaves:
            if source in self._data.get(target, {}) and self.is_bidirectional:
                return self._data[target][source]
            return None
            # raise KeyError(
            #     f"[{target}] target does not exist at source [{source}]: {branch_leaves}"
            # )
        return self._data[source][target]
