import os
import sys


def test():
    try:
        context = os.environ.get('EXECUTE_DATE', "None")
        day, time = context.split("T")
        print(f"Day: {day}")
        print(f"Time: {time}")
        return 0
    except:
        return 1

if __name__ == "__main__":
    result = test()
    sys.exit(result)
