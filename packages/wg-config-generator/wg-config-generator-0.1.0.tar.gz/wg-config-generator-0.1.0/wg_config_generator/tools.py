import subprocess


def get_pubkey(privkey):
    try:
        return (
            subprocess.run(
                ["wg", "pubkey"],
                input=privkey.encode("utf-8"),
                capture_output=True,
                check=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
    except:
        raise RuntimeError(f"could not read privkey '{privkey}'")


def gen_privkey():
    try:
        return (
            subprocess.run(["wg", "genkey"], capture_output=True, check=True)
            .stdout.decode("utf-8")
            .strip()
        )
    except:
        raise RuntimeError(f"could not generate privkey")
