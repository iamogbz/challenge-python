def solve(courses):
    """
    Analyse courses for possibility of completion
    :param courses: list of courses [requirement, auxilliary]
    """
    c2r = dict() # course to requirements
    r2c = dict() # requirement to courses
    for [r, c] in courses:
        if r not in r2c:
            r2c[r] = set()
        r2c[r].add(c)
        if c not in c2r:
            c2r[c] = set()
        c2r[c].add(r)

    n_courses = r2c.keys() - c2r.keys()
    while n_courses:
        p_courses = set()
        for r in n_courses:
            for c in r2c.get(r, []):
                c2r[c].remove(r)
                if not c2r[c]:
                    p_courses.add(c)
        n_courses = p_courses

    return not sum(map(len, c2r.values()))
