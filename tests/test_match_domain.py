"""Unit tests for match_domain specificity (no network, stdlib only)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from rico_bookmarks_manager import match_domain


def test_exact_domain_match():
    assert match_domain("figma.com") == ("设计", "设计工具", "Figma")
    assert match_domain("openai.com") == ("AI", "AI模型", "OpenAI / ChatGPT")


def test_specific_subdomain_rule_wins_over_parent():
    # DOMAIN_RULES lists dedicated entries for these subdomains; the generic
    # parent entry must not shadow them.
    assert match_domain("chat.openai.com") == ("AI", "AI工具", "ChatGPT")
    assert match_domain("platform.openai.com") == ("AI", "AI平台", "OpenAI API")
    assert match_domain("zhuanlan.zhihu.com") == ("博客", "技术博客", "知乎专栏")


def test_subdomain_still_matches_parent_rule():
    assert match_domain("docs.figma.com") == ("设计", "设计工具", "Figma")


def test_substring_only_host_is_not_matched():
    # "myfigma.com" merely contains "figma.com"; it is not Figma.
    assert match_domain("myfigma.com") is None
    assert match_domain("notion.software") is None


def test_unknown_and_empty_domains():
    assert match_domain("example.com") is None
    assert match_domain("") is None
