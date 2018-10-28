def solve(courses):
    """
    Analyse courses for possibility of completion
    :param courses: list of courses [requirement, auxilliary]
    """
    # print("---")
    c2r = dict() # course to requirements
    r2c = dict() # requirement to courses
    for [r, c] in courses:
        if r not in r2c:
            r2c[r] = set()
        r2c[r].add(c)
        if c not in c2r:
            c2r[c] = set()
        c2r[c].add(r)
    # courses with no requirements can be taken
    n_courses = r2c.keys() - c2r.keys()
    v_courses = set()
    count = 0
    while n_courses:
        # next set of courses that can be taken
        p_courses = set()
        for r in n_courses:
            # get courses that required this one
            for c in r2c.get(r, []):
                count += 1
                # remove this course from pending requirements
                c2r[c].remove(r)
                # if course has no more requirements
                if not c2r[c]:
                    # add to set of courses to take next
                    p_courses.add(c)
        v_courses.update(n_courses)
        n_courses = p_courses

    # print(count, v_courses, c2r)
    return not sum(map(len, c2r.values()))


# some tests
print(solve([[1, 0], [2, 0], [2, 1]]), True)
print(solve([[1, 0], [0, 2], [2, 1], [3, 1]]), False)
print(solve([[1, 0], [2, 0], [2, 1], [3, 1]]), True)
print(solve([[1, 0], [2, 0], [3, 1], [1, 2]]), True)
print(solve([[1, 0], [2, 0], [3, 0], [2, 1], [3, 1], [3, 2]]), True)
print(
    solve(
        [
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [2, 1],
            [3, 1],
            [4, 1],
            [3, 2],
            [4, 2],
            [5, 2],
            [4, 3],
            [5, 4],
        ]
    ),
    True,
)
print(solve([[1, 0], [3, 2], [5, 4], [7, 6], [8, 9], [11, 10]]), True)
