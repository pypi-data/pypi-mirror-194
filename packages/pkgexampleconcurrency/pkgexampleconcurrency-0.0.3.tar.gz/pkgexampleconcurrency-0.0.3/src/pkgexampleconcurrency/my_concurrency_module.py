import argparse
from .mythreading import MyThreading
from .mymultiprocessing import MyMultiprocessing


def my_threading():
    my_threading_main_parser = argparse.ArgumentParser(
        description="Run default threading example"
    )
    my_threading_parser = my_threading_main_parser.add_mutually_exclusive_group()
    my_threading_parser.add_argument(
        "--nd-concurrent",
        action="store_true",
        help="'Non daemon' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--nd-nj-concurrent",
        action="store_true",
        help="'Non daemon' 'non-join' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--nd-serial", action="store_true", help="'Non daemon' serial thread example."
    )
    my_threading_parser.add_argument(
        "--d-concurrent",
        action="store_true",
        help="'Daemon' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--d-nj-concurrent",
        action="store_true",
        help="'Daemon' 'non-join' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--i-printalpha",
        action="store_true",
        help="Thread by inheritence example. Define own class that prints alphabet.",
    )
    my_threading_parser.add_argument(
        "--qexample",
        action="store_true",
        help="Threading queue example",
    )
    my_threading_parser.add_argument(
        "--qlexample",
        action="store_true",
        help="Threading queue with lock example",
    )
    my_threading_parser.add_argument(
        "--qjexample",
        action="store_true",
        help="Threading 'queue join' example",
    )
    my_threading_parser.add_argument(
        "--qdqexample",
        action="store_true",
        help="Threading with deque example",
    )

    my_args = my_threading_main_parser.parse_args()
    mythreadingexamples = MyThreading()
    if my_args.nd_concurrent == True:
        mythreadingexamples.non_daemon_concurrent_example()
    if my_args.nd_serial == True:
        mythreadingexamples.non_daemon_serial_example()
    if my_args.nd_nj_concurrent == True:
        mythreadingexamples.non_daemon_no_join_concurrent_example()
    if my_args.d_concurrent == True:
        mythreadingexamples.daemon_concurrent_example()
    if my_args.d_nj_concurrent == True:
        mythreadingexamples.daemon_no_join_concurrent_example()
    if my_args.i_printalpha == True:
        mythreadingexamples.print_alpha()
    if my_args.qexample == True:
        mythreadingexamples.threading_queue_example()
    if my_args.qlexample == True:
        mythreadingexamples.threading_queue_lock_example()
    if my_args.qjexample == True:
        mythreadingexamples.threading_queue_join_example()
    if my_args.qdqexample == True:
        mythreadingexamples.threading_using_a_deque()


def my_multiprocessing():
    my_main_multiprocessing_parser = argparse.ArgumentParser(
        description="Run default multiprocessing example"
    )
    my_multiprocessing_parser = (
        my_main_multiprocessing_parser.add_mutually_exclusive_group()
    )

    my_multiprocessing_parser.add_argument(
        "--cpu-count", action="store_true", help="What is your machine CPU count?"
    )
    my_multiprocessing_parser.add_argument(
        "--nd-concurrent",
        action="store_true",
        help="'Non Daemon' concurrent process example ",
    )
    my_multiprocessing_parser.add_argument(
        "--i-printalpha",
        action="store_true",
        help="Multiprocess by inheritence example. Define own class that prints alphabet.",
    )
    my_multiprocessing_parser.add_argument(
        "--poolexample",
        action="store_true",
        help="Multiprocess by pool square example.",
    )
    my_multiprocessing_parser.add_argument(
        "--poolcontextexample",
        action="store_true",
        help="Multiprocess by context pool square example.",
    )
    my_multiprocessing_parser.add_argument(
        "--poolcontextexampleadd",
        action="store_true",
        help="Multiprocess by context pool add example.",
    )
    my_multiprocessing_parser.add_argument(
        "--qexample",
        action="store_true",
        help="Multiprocess with queue example.",
    )
    my_multiprocessing_parser.add_argument(
        "--qlexample",
        action="store_true",
        help="Multiprocess with queue and a lock example.",
    )
    my_multiprocessing_parser.add_argument(
        "--qjexample",
        action="store_true",
        help="Multiprocess with joinable queue.",
    )
    my_multiprocessing_parser.add_argument(
        "--qdqexample",
        action="store_true",
        help="Multiprocess with a dequeue.",
    )

    my_args = my_main_multiprocessing_parser.parse_args()
    mymultiprocessingexamples = MyMultiprocessing()
    if my_args.cpu_count == True:
        mymultiprocessingexamples.count_cpu()
    if my_args.nd_concurrent == True:
        mymultiprocessingexamples.non_daemon_concurrent_example()
    if my_args.i_printalpha == True:
        mymultiprocessingexamples.print_alpha()
    if my_args.poolexample == True:
        mymultiprocessingexamples.pool_example_square()
    if my_args.poolcontextexample == True:
        mymultiprocessingexamples.pool_context_example_square()
    if my_args.poolcontextexampleadd == True:
        mymultiprocessingexamples.pool_context_example_add()
    if my_args.qexample == True:
        mymultiprocessingexamples.multiprocessing_queue_example()
    if my_args.qlexample == True:
        mymultiprocessingexamples.multiprocessing_queue_lock_example()
    if my_args.qjexample == True:
        mymultiprocessingexamples.multiprocessing_joinable_queue()
    if my_args.qdqexample == True:
        mymultiprocessingexamples.multiprocessing_using_a_dequeue()


def my_concurrentfutures():
    my_concurrentfutures_parser = argparse.ArgumentParser(
        description="Run default concurrent futures example"
    )
    my_concurrentfutures_parser.add_argument(
        "--run", action="store_true", help="Run default concurrent futures example"
    )
    my_args = my_concurrentfutures_parser.parse_args()
    print(my_args.run)


def my_asyncio():
    my_asyncio_parser = argparse.ArgumentParser(
        description="Run default asyncio example"
    )
    my_asyncio_parser.add_argument(
        "--run", action="store_true", help="Run default asyncio example"
    )
    my_args = my_asyncio_parser.parse_args()
    print(my_args.run)
