from tailwind_merge import TailwindMerge


def test_basic_merge():
    merger = TailwindMerge()
    result = merger.merge("p-4 w-6", "w-8")
    assert result == "p-4 w-8"

def test_multiple_conflicts():
    merger = TailwindMerge()
    result = merger.merge(
        "p-4 w-6 text-blue-500",
        "w-8 text-red-500"
    )
    assert result == "p-4 w-8 text-red-500"

def test_custom_pattern():
    merger = TailwindMerge()
    merger.add_rule('custom', ['custom-'])
    result = merger.merge("custom-1", "custom-2")
    assert result == "custom-2"

def test_display():
    merger = TailwindMerge()
    result = merger.merge(
        "block",
        "inline"
    )
    assert result == "inline"

def test_arbitrary_overwrite():
    merger = TailwindMerge()
    result = merger.merge(
        "bg-red-500",
        "bg-[#000]"
    )
    assert result == "bg-[#000]"

def test_complete_arbitrary_overwrite():
    merger = TailwindMerge()
    result = merger.merge(
        "bg-[#ff0000]",
        "bg-[#000]"
    )
    assert result == "bg-[#000]"

def test_no_conflict():
    merger = TailwindMerge()
    result = merger.merge(
        "p-4 w-6",
        "text-blue-500"
    )
    assert result == "p-4 w-6 text-blue-500"

def test_no_conflict_similar():
    merger = TailwindMerge()
    result = merger.merge(
        "grid grid-cols-3 grid-rows-3",
        "grid-cols-4 grid-rows-2"
    )
    print(result)
    assert result == "grid grid-cols-4 grid-rows-2"