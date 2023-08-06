# type: ignore
import re
from typing import AnyStr


def blank(pattern, string):
    res = re.search(pattern, string)
    if not res:
        return string
    matchsize = len(res.group(0))
    return re.sub(pattern, " " * matchsize, string)


def remove_comments(content):
    in_cxx_comment = False
    prepared_content = ""
    line: AnyStr  # pylance runs into performance issues without this hint
    for line in [c + "\n" for c in content.split("\n")]:
        # remove C++-style comments
        if in_cxx_comment:
            if re.search(r"\*/", line):
                line = blank(r".*\*/", line)
                in_cxx_comment = False
            else:
                line = " " * len(line - 1) + "\n"
        else:
            line = blank(r"/\*.*?\*/", line)
        if re.search(r"/\*", line):
            line = blank(r"/\*.*", line)
            in_cxx_comment = True
        line = blank(r"//[^\r\n]*\n", line)
        prepared_content += line
    return prepared_content


def rewrite_cproblem(content: str) -> str:
    need_struct_body = False
    skip_asm = False
    in_attribute = False
    in_cxx_comment = False
    prepared_content = ""
    line: AnyStr  # pylance runs into performance issues without this hint
    for line in [c + "\n" for c in content.split("\n")]:
        # remove C++-style comments
        if in_cxx_comment:
            if re.search(r"\*/", line):
                line = blank(r".*\*/", line)
                in_cxx_comment = False
            else:
                line = " " * len(line - 1) + "\n"
        else:
            line = blank(r"/\*.*?\*/", line)
        if re.search(r"/\*", line):
            line = blank(r"/\*.*", line)
            in_cxx_comment = True
        # remove __attribute__
        line = blank(r"__attribute__\s*\(\(\s*[a-z_, ]+\s*\)\)\s*", line)
        # line = blank(r'__attribute__\s*\(\(\s*[a-z_, ]+\s*\(\s*[a-zA-Z0-9_, "\.]+\s*\)\s*\)\)\s*', line)
        # line = blank(r'__attribute__\s*\(\(\s*[a-z_, ]+\s*\(\s*sizeof\s*\([a-z ]+\)\s*\)\s*\)\)\s*', line)
        # line = blank(r'__attribute__\s*\(\(\s*[a-z_, ]+\s*\(\s*\([0-9]+\)\s*<<\s*\([0-9]+\)\s*\)\s*\)\)\s*', line)
        line = blank(r"__attribute__\s*\(\(.*\)\)\s*", line)
        if re.search(r"__attribute__\s*\(\(", line):
            line = blank(r"__attribute__\s*\(\(.*", line)
            in_attribute = True
        elif in_attribute:
            line = blank(r".*\)\)", line)
            in_attribute = False
        # rewrite some GCC extensions
        line = blank(r"__extension__", line)
        line = blank(r"__restrict", line)
        line = blank(r"__restrict__", line)
        line = blank(r"__inline__", line)
        line = blank(r"__inline", line)
        line = re.sub(r"__const", "  const", line)
        line = re.sub(r"__signed__", "  signed  ", line)
        line = re.sub(r"__builtin_va_list", (" " * 15) + "int", line)
        # a hack for some C-standards violating code in LDV benchmarks
        if need_struct_body and re.match(r"^\s*}\s*;\s*$", line):
            line = "int __dummy; " + line
            need_struct_body = False
        elif need_struct_body:
            need_struct_body = re.match(r"^\s*$", line) is not None
        elif re.match(r"^\s*struct\s+[a-zA-Z0-9_]+\s*{\s*$", line):
            need_struct_body = True
        # remove inline asm
        if re.match(r'^\s*__asm__(\s+volatile)?\s*\("([^"]|\\")*"[^;]*$', line):
            skip_asm = True
        elif skip_asm and re.search(r"\)\s*;\s*$", line):
            skip_asm = False
            line = "\n"
        if skip_asm or re.match(
            r'^\s*__asm__(\s+volatile)?\s*\("([^"]|\\")*"[^;]*\)\s*;\s*$', line
        ):
            line = "\n"
        # remove asm renaming
        line = blank(r'__asm__\s*\(""\s+"[a-zA-Z0-9_]+"\)', line)
        prepared_content += line
    return prepared_content
