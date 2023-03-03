from bot.manager import Manager


def mainloop():
    manager = Manager()
    client = manager.AdbClient
    client.start_adb_server()

    try:
        while manager.queue:
            bot = manager.bot()
            print(bot.instance_title)
            bot.run()
            bot.stop()
    finally:
        print('stop adb server')
        client.kill()
        print('done')


if __name__ == '__main__':
    mainloop()
