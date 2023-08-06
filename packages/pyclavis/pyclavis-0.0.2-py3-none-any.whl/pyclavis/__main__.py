from .gui import startup, ask_startup_passphrase, check_instance_or_die


# keep rc, otherwise socket gets closed by garbage collection
rc = check_instance_or_die()

ask_startup_passphrase()

startup()
