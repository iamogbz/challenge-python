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
        return sorted(
            ((s, t, self._data.get((s, t))) for (s, t) in self._data), key=key
        )

    def insert(self, source, target, value, reverse=None):
        """Insert source vertex and directed edge to target with weight value"""
        key = (source, target)
        if self.is_bidirectional:
            key = tuple(sorted(key))
        self._data[key] = value
        if reverse is not None and not self.is_bidirectional:
            self._data[(target, source)] = reverse

    def remove(self, source, target):
        """Remove vertex edge from map including the reverse direction if bidirectional"""

        def _remove(k):
            if k in self._data:
                del self._data[k]

        _remove((source, target))
        if self.is_bidirectional:
            _remove((target, source))

    def retarget(self, old_target, new_target):
        """Replace all edges to previous target with new one"""
        for left, right in set(self._data.keys()):
            if right == old_target:
                self._data[(left, new_target)] = self._data[(left, right)]
                del self._data[(left, right)]
                right = new_target  # ensure next step keeps track of new keys

            if left == old_target:
                self._data[(new_target, right)] = self._data[(old_target, right)]
                del self._data[(old_target, right)]

    def get_adjacent(self, node=None):
        """Get all nodes/vertexes directly connected to this one or all when node is None"""
        conns = set()
        for s, t in self._data.keys():
            if node is None or s == node:
                conns.add(t)
            if node is None or (t == node and self.is_bidirectional):
                conns.add(s)

        return [*conns]

    def get_value(self, source, target):
        """Get weight value for source target edge connection"""
        k = (source, target)
        _k = tuple(reversed(k))
        if self.is_bidirectional and _k in self._data:
            return self._data.get(_k)
        return self._data.get(k, None)
