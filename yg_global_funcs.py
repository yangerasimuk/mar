import sys

def progressbar(it, prefix="", size=60, out=sys.stdout):  # Python3.3+
    # mared_files = []
    # print("#3. Search mared files...")
    # for i in progressbar(range(len(non_empty_folders)), "Computing: ", 40):
    #     folder = non_empty_folders[i]
    #     files = folder.get_files()
    #     for file in files:
    #         name_resolver = LegacyNameResolver(file.full_name())
    #         if name_resolver.isValid() and name_resolver.hasMeta():
    #             mared_files.append(file)
    count = len(it)

    def show(j):
        x = int(size * j / count)
        print("{}[{}{}] {}/{}".format(prefix, "#" * x, "." * (size - x), j, count),
              end='\r', file=out, flush=True)

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("\n", flush=True, file=out)
