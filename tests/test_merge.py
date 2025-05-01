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
    assert result == "grid grid-cols-4 grid-rows-2"

def test_padding_sub_groups():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "p-4 pt-2 pb-3 px-3",
        "pt-1 pb-4 px-2"
    )
    assert result == "p-4 pt-1 pb-4 px-2"

def test_margin_sub_groups():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "m-4 mt-2 mb-3 mx-3",
        "mt-1 mb-4 mx-2"
    )
    assert result == "m-4 mt-1 mb-4 mx-2"

def test_conflicting_stubs():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "text-xl text-red-500 text-left",
        "text-sm text-blue-500 text-center"
    )
    assert result == "text-sm text-blue-500 text-center"

def test_with_modifiers():
    twmerge = TailwindMerge()
    result = twmerge.merge(
        "hover:text-red-500",
        "hover:text-green-500"
    )
    assert result == "hover:text-green-500"