import argparse
import inspect
import os
from queue import Queue
import sys
import threading
from time import sleep
from appsetupscripts.driver_manager import DriverManager

from appsetupscripts.setup import AnalyzedApp
from appium.webdriver.appium_service import AppiumService
from appsetupscripts.setup import *


def find_subclasses(module, clazz):
    return [
        cls
        for name, cls in inspect.getmembers(module)
        if inspect.isclass(cls) and issubclass(cls, clazz) and (cls is not clazz)
    ]


def run_analysis_of_app(analyzed_app_cls: type, thread_index: int, apk_directory: str, output_file: str, args: argparse.Namespace):

    # Start driver
    print(analyzed_app_cls)

    analyzed_app_cls

    driver_manager = DriverManager(thread_index, args.headless)

    app: AnalyzedApp = analyzed_app_cls(driver_manager.driver, apk_directory)

    if(app.needs_google_account):
        try:
            # TODO: Add real username + password
            driver_manager.log_in_with_google_2(
                args.google_username, args.google_password)
        except:
            driver_manager.driver.get_screenshot_as_file(filename="error.png")
            source = driver_manager.driver.page_source
            open("error-screen.xml", "w").write(source)
            # Try for a second time
            try:
                # TODO: Add real username + password
                driver_manager.log_in_with_google_2(
                    args.google_username, args.google_password)
            except:
                return f'Failed analyzing {analyzed_app_cls}, could not log in to google'

    driver_manager.set_swipe_lock_screen()
    driver_manager.silence_ringer()

    app.install()
    app.setup()

    sleep(3)

    app.perform_analysis(numbers, output_file)

    driver_manager.finish()

    return f'Succesfully analyzed {analyzed_app_cls}'


if __name__ == '__main__':

    # Command Line Arguments
    parser = argparse.ArgumentParser(
        description='Test numbers on Android Spam Call Blocking Applications')
    parser.add_argument('--google_username', action='store',
                        required=True, help="A google account's username")
    parser.add_argument('--google_password', action='store',
                        required=True, help="A google account's password")
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--threads', action='store', default=1, type=int)
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                     default=sys.stdin)
    args = parser.parse_args()

    if args.infile.isatty():
        parser.print_help()
        quit()

    # GENERAL CONSTANTS
    current_directory = os.path.dirname(os.path.abspath(__file__))
    apk_directory = current_directory + '/apks'

    time.strftime("%Y%m%d-%H%M%S")

    os.makedirs('out', exist_ok=True)
    output_file = 'out/results'+time.strftime("%Y%m%d-%H%M%S")+'.csv'
    open(output_file, 'w').truncate(0)
    csv_line = f"number,package_name,status,delta,accuracy"
    with open(output_file, 'a') as fd:
        fd.write(f'{csv_line}\n')

    numbers = args.infile.read().splitlines()

    appium_service = AppiumService()
    appium_service.start(args=['--allow-insecure=emulator_console'])

    classes_to_analyze = [
        AllInOneCallerID,
        CallAppContacts,
        CallerIDBlock,
        Telguarder,
        MistergroupShouldianswer,
        MglabScm,
        WebascenderCallerID
    ]

    threads = 1

    if(threads == 1):
        for cls in classes_to_analyze:
            print(run_analysis_of_app(cls, 0, apk_directory, output_file, args))

    else:
        def worker(q, thread_index: int):
            while True:
                cls = q.get()
                run_analysis_of_app(cls, thread_index,
                                    apk_directory, output_file, args)
                q.task_done()

        q: Queue[type] = Queue()
        for i in range(2):
            t = threading.Thread(target=worker, args=[q, i])
            t.daemon = True
            t.start()

        for cls in classes_to_analyze:
            q.put(cls)

        q.join()       # block until all tasks are done

    appium_service.stop()


   