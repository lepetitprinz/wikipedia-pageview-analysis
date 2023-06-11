import os

def get_context(context: None):
    print(context)
    print("finished")

if __name__ == "__main__":
    context = os.environ.get('EXECUTE_DATE')
    get_context(context=context)
