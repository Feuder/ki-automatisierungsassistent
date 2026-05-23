import threading
import time
import sys
from contextlib import contextmanager


def _ladeanimation(stop_event, text, geschwindigkeit=0.1, pause=1):
    while not stop_event.is_set():
        ausgabe = ""

        for buchstabe in text:
            if stop_event.is_set():
                break

            ausgabe += buchstabe
            sys.stdout.write(ausgabe + "\r")
            sys.stdout.flush()
            time.sleep(geschwindigkeit)

        if stop_event.is_set():
            break

        time.sleep(pause)

        sys.stdout.write(" " * len(text) + "\r")
        sys.stdout.flush()

    sys.stdout.write(" " * len(text) + "\r")
    sys.stdout.flush()


@contextmanager
def ladeanzeige(text="Aufgaben werden erstellt...", geschwindigkeit=0.1, pause=1):
    stop_event = threading.Event()

    thread = threading.Thread(
        target=_ladeanimation,
        args=(stop_event, text, geschwindigkeit, pause),
        daemon=True
    )

    thread.start()

    try:
        yield

    finally:
        stop_event.set()
        thread.join()