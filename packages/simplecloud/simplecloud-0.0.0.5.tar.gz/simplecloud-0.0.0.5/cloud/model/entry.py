def Entity(**kwargs):
    return {**kwargs}


def CloudEntry(path="", name="", is_directory=False, size=0):
        return Entity(**locals())


def CloudListContext(path="", current_page=0, total_pages=0, page_size=0):
        return Entity(**locals())


def CloudListResponse(entries: list[CloudEntry] = [], context: dict = None):
        return Entity(**locals())
