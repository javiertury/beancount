"""Lex, flex, reflex, yacc, Bison, scanners & parser generators."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")


def setup_parser():
    if not native.existing_rule("m4"):
        http_archive(
            name = "rules_m4",
            urls = ["https://github.com/jmillikin/rules_m4/releases/download/v0.2/rules_m4-v0.2.tar.xz"],
            sha256 = "c67fa9891bb19e9e6c1050003ba648d35383b8cb3c9572f397ad24040fb7f0eb",
        )

    # http_archive(
    #     name = "flex",
    #     build_file_content = all_content,
    #     strip_prefix = "flex-2.6.4",
    #     sha256 = "e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995",
    #     urls = ["https://github.com/westes/flex/releases/download/v2.6.4/flex-2.6.4.tar.gz"],
    # )

    # Reflex.
    # Create a target of the headers, because generated code needs to include
    # and links against a reflex library.
    all_content = """
filegroup(
  name = "all",
  srcs = glob(["**"]),
  visibility = ["//visibility:public"]
)
    """
    headers_content = """
filegroup(
  name = "headers",
  srcs = glob(["include/reflex/*.h"]),
  visibility = ["//visibility:public"]
)
    """
    http_archive(
        name = "reflex",
        build_file_content = all_content + headers_content,
        strip_prefix = "RE-flex-3.0.1",
        sha256 = "f07188377bb8dfde54c6b19f219c1c60d43d501f5458936c686bd29d684cce19",
        urls = ["https://github.com/Genivia/RE-flex/archive/v3.0.1.zip"],
    )

    # 2020-11-21
    http_archive(
        name = "bison",
        build_file_content = all_content,
        strip_prefix = "bison-3.7.3",
        sha256 = "104fe912f2212ab4e4a59df888a93b719a046ffc38d178e943f6c54b1f27b3c7",
        urls = ["https://ftp.gnu.org/gnu/bison/bison-3.7.3.tar.gz"],
    )
