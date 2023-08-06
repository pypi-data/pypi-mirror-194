from colorama  import Fore, init
from threading import Thread
from random    import randint
from requests  import get

init(autoreset=True)

def adr() -> str:
    return ".".join(
            [str(randint(1, 225)) for _ in range(4)]
        )

def search() -> None:
    ip = adr()
    try:
        get(
          "http://%s" % ip,
          timeout=15
        )
    except:
        print(
          "%s%s inactive." % (Fore.RED, ip)
        )
    else:
        print(
          "%s%s active." % (Fore.GREEN, ip)
        ); open('active.txt', 'a').write('%s\n' % ip)

def start(threads) -> None:
    for _ in range(threads):
        Thread(target=search).start()


if __name__ == "__main__":
    start(
     threads=1000000000,
    )