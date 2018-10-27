def solve(courses):
    """
    Analyse courses for possibility of completion
    :param courses: list of courses [requirement, auxilliary]
    """
    print("---")
    # all auxillary courses
    x_courses = set()
    # build map of core to auxilliary
    m_courses = dict()
    for cs in courses:
        if cs[0] in m_courses:
            m_courses[cs[0]].add(cs[1])
        else:
            m_courses[cs[0]] = set([cs[1]])
        # keep track of all courses that have requirements
        x_courses.add(cs[1])
    # search through courses
    # take all required courses
    r_courses = m_courses.keys()
    # start with only required courses that have no requirements
    n_courses = r_courses - x_courses
    print("courses", m_courses)
    # keep track of required courses seen
    v_courses = set()
    count = 0
    while n_courses:
        print("next", n_courses, v_courses)
        l_courses = n_courses.intersection(v_courses)
        if l_courses:
            print(l_courses, "visited in", v_courses, count)
            return False
        # next set of required courses
        p_courses = set()
        for c in n_courses:
            count += 1
            p_courses.update(m_courses.get(c, set()))
        for p in set(p_courses):
            count += 1
            p_courses.difference_update(m_courses.get(p, set()))
        print("pending", p_courses)
        # mark last required courses as seen
        v_courses.update(n_courses)
        # only queue next courses that are required and were not just checked
        n_courses = p_courses.intersection(r_courses) - n_courses

    print("visited", v_courses, count)
    return v_courses == r_courses

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
