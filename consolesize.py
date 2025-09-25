import shutil, sys



while True:

    sys.stdout.write(f"\r{shutil.get_terminal_size().columns},{shutil.get_terminal_size().lines}")
    sys.stdout.flush()