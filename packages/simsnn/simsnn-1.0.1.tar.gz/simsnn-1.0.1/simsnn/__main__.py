import argparse
from simsnn.examples import circuit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", default=5, metavar="N", type=int, help="The amount of steps to simulate"
    )
    parser.add_argument(
        "-f",
        default="circuit",
        metavar="F",
        type=str,
        help="The example network to run",
    )
    args = parser.parse_args()

    if args.f == "circuit":
        circuit.run(duration=args.d)


if __name__ == "__main__":
    main()
