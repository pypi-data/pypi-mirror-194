
# 重复迭代
movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
          ["Graham Chapman", ["Michael Pailin", "John Cleese",
                              "Terry Gilliam", "Eric Idle", "Terry Joines"]]]
print(movies)

# 递归


def print_lol(the_list):

    for item in the_list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)


print_lol(movies)
