"""
Inner Ralph Loop — generate prompts and rewrite sub-package imports.

Usage:
    uv run inner_ralph.py generate-prompt --context ctx.json --top-package litellm --sub-package annotated-types
    uv run inner_ralph.py rewrite-sub-imports --sub-package annotated-types --target-dir diy_litellm
"""

import argparse
import json
import re
from pathlib import Path


TEMPLATE_FILE = Path(__file__).parent / "inner_ralph_loop.md"


def generate_prompt(args):
    ctx = json.loads(Path(args.context).read_text())
    template = TEMPLATE_FILE.read_text()

    sub_pkg = args.sub_package.replace("-", "_")
    top_pkg = args.top_package.replace("-", "_")

    replacements = {
        "top_package": top_pkg,
        "sub_package": sub_pkg,
        "category": ctx.get("category", "Unknown"),
        "strategy": ctx.get("strategy", "Study reference and reimplement"),
        "reference_material": ctx.get("reference_material", f".slash_diy/reference/{sub_pkg}/"),
        "acceptable_sub_dependencies": ", ".join(ctx.get("acceptable_sub_dependencies", [])) or "none",
        "max_iterations": str(args.max_iterations),
    }

    prompt = template
    for key, value in replacements.items():
        prompt = prompt.replace(f"{{{key}}}", value)

    print(prompt)


def rewrite_sub_imports(args):
    sub_pkg = args.sub_package.replace("-", "_")
    target = f"diy_{sub_pkg}"
    target_dir = Path(args.target_dir)

    if not target_dir.is_dir():
        print(f"Error: {target_dir} does not exist")
        raise SystemExit(1)

    count = 0
    for f in target_dir.rglob("*.py"):
        # Skip test files — they import from diy_<top_pkg>, not the sub-package
        if "tests" in f.parts:
            continue
        content = f.read_text(errors="replace")
        new_content = re.sub(rf"\bfrom {sub_pkg}\b", f"from {target}", content)
        new_content = re.sub(rf"\bimport {sub_pkg}\b", f"import {target}", new_content)
        if new_content != content:
            f.write_text(new_content)
            count += 1

    print(f"Rewrote imports in {count} files ({sub_pkg} -> {target}) within {target_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Inner Ralph Loop utilities")
    sub = parser.add_subparsers(dest="command")

    gp = sub.add_parser("generate-prompt", help="Generate inner ralph loop prompt")
    gp.add_argument("--context", required=True, help="Path to decomposition context JSON")
    gp.add_argument("--top-package", required=True, help="Top-level package name")
    gp.add_argument("--sub-package", required=True, help="Sub-package to build")
    gp.add_argument("--max-iterations", type=int, default=30, help="Max loop iterations")

    rw = sub.add_parser("rewrite-sub-imports", help="Rewrite sub-package imports in source")
    rw.add_argument("--sub-package", required=True, help="Sub-package to rewrite")
    rw.add_argument("--target-dir", required=True, help="Directory to rewrite imports in")

    args = parser.parse_args()
    if args.command == "generate-prompt":
        generate_prompt(args)
    elif args.command == "rewrite-sub-imports":
        rewrite_sub_imports(args)
    else:
        parser.print_help()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
