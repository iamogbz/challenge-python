import random


def count_fields(patches):
    num_fields = 0
    num_rows = len(patches)
    num_cols = len(patches[0])
    for i in range(num_rows):
        for j in range(num_cols):
            if not patches[i][j]:
                continue
            left_field = int(patches[i][j - 1]) if j > 0 else 0
            top_field = int(patches[i - 1][j]) if i > 0 else 0
            if left_field or top_field:
                if left_field and top_field:
                    patches[i][j] = min(left_field, top_field)
                    if left_field != top_field:
                        num_fields = max(left_field, top_field) - 1
                else:
                    patches[i][j] = left_field or top_field
            else:
                num_fields += 1
                patches[i][j] = num_fields
    for _ in patches:
        print(_)
    return num_fields


print(count_fields([[random.choice([1, 0]) for __ in range(5)] for _ in range(5)]))
