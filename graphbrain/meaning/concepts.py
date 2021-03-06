def strip_concept(edge):
    """Strip away nesting edges with connectors such as triggers and
    subpredicates, to expose the outmost and leftmost concept that can be
    found. May be the edge itself.

    For example:

    (against/t (the/m (of/b treaty/c paris/c)))

    becomes

    (the/m (of/b treaty/c paris/c))
    """
    if edge.type()[0] == 'c':
        return edge
    elif not edge.is_atom():
        return strip_concept(edge[1])
    else:
        return None


def has_proper_concept(edge):
    """Check if the concept either is a proper edge, or contains one."""
    if edge.is_atom():
        return edge.type()[:2] == 'cp'
    else:
        for subedge in edge[1:]:
            if has_proper_concept(subedge):
                return True
        return False


def all_concepts(edge):
    """Recursively search for all concepts contained in the edge, returning
    a set that can also contain itself."""
    concepts = set()
    if edge.type()[0] == 'c':
        concepts.add(edge)
    if not edge.is_atom():
        for item in edge:
            concepts |= all_concepts(item)
    return concepts
