import subprocess
import sys


def main():
    print("🚀 Starting all tests (Unit + Integration)...")

    # Run pytest.
    # Unit tests are fast, integration tests take longer (LLM/Embeddings).
    cmd = [sys.executable, "-m", "pytest"]

    # Add any extra args if passed to this script
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Some tests failed (Exit code: {result.returncode})")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
