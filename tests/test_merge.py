from tailwind_merge import TailwindMerge


def test_basic_merge():
    twmerge = TailwindMerge()
    result = twmerge.merge("p-4 w-6", "w-8")
    assert result == "p-4 w-8"

def test_multiple_conflicts():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "p-4 w-6 text-blue-500",
        "w-8 text-red-500"
    )
    assert result == "p-4 w-8 text-red-500"

def test_custom_pattern():
    twmerge = TailwindMerge()
    twmerge.add_rule('custom', ['custom-'])
    result = twmerge.merge("custom-1", "custom-2")
    assert result == "custom-2"

def test_display():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "block",
        "inline"
    )
    assert result == "inline"

def test_arbitrary_overwrite():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "bg-red-500",
        "bg-[#000]"
    )
    assert result == "bg-[#000]"

def test_complete_arbitrary_overwrite():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "bg-[#ff0000]",
        "bg-[#000]"
    )
    assert result == "bg-[#000]"

def test_no_conflict():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "p-4 w-6",
        "text-blue-500"
    )
    assert result == "p-4 w-6 text-blue-500"

def test_no_conflict_similar():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "grid grid-cols-3 grid-rows-3",
        "grid-cols-4 grid-rows-2"
    )
    print(result)
    assert result == "grid grid-cols-4 grid-rows-2"