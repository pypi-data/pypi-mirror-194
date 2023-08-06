import akiwi.app as kiwi
import sys

def main():
    app = kiwi.Application()
    return 0 if app.run_with_command() else 100

if __name__ == "__main__":
    sys.exit(main())