"""
Run the extracted test suite against yoink_<package>/ and compute score.

Auto-detects the test directory by looking for yoink_*/tests/.

Usage:
    uv run run_tests.py --project-dir /path/to/project
    uv run run_tests.py --project-dir /path/to/project --summary-only
"""

import argparse
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def find_test_dir(project_dir: Path) -> str:
    for d in sorted(project_dir.glob("yoink_*/tests/generated")):
        if d.is_dir():
            return str(d)
    return str(project_dir / "tests")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Suppress pytest output, print only the results summary",
    )
    args = parser.parse_args()
    project_dir = args.project_dir.resolve()

    test_dir = find_test_dir(project_dir)

    with tempfile.TemporaryDirectory() as tmp_dir:
        junit_xml_path = Path(tmp_dir) / "results.xml"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                test_dir,
                "-v",
                "--tb=short",
                f"--junitxml={junit_xml_path}",
            ],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=project_dir,
        )

        if not args.summary_only:
            print(result.stdout)
            print(result.stderr)

        # Parse structured results from JUnit XML instead of scraping output.
        # pytest wraps <testsuite> inside a <testsuites> root, so we need to
        # find the actual <testsuite> element(s) and sum their attributes.
        passed = failed = errors = 0
        tree = ET.parse(junit_xml_path)
        root = tree.getroot()

        testsuite_elements = (
            root.findall("testsuite") if root.tag == "testsuites" else [root]
        )
        total_tests = 0
        for testsuite in testsuite_elements:
            total_tests += int(testsuite.attrib.get("tests", 0))
            failed += int(testsuite.attrib.get("failures", 0))
            errors += int(testsuite.attrib.get("errors", 0))
        passed = total_tests - failed - errors

    total = passed + failed + errors
    score = passed / total if total > 0 else 0.0

    print("\n--- Results ---")
    print(f"score:          {score:.6f}")
    print(f"passed:         {passed}")
    print(f"failed:         {failed}")
    print(f"errors:         {errors}")
    print(f"total:          {total}")


if __name__ == "__main__":
    main()
