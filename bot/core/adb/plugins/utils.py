from subprocess import Popen

class Plugin:
    def shell(self, cmd, handler=None, timeout=None):
        pass


class Utils(Plugin):

    def open_app(self, app):
        Popen(app)

    def get_top_activity(self):
        activities = self.get_top_activities()
        if activities:
            return activities[-1]
        else:
            return

    def get_top_activities(self):
        cmd = "dumpsys activity top | grep ACTIVITY"
        result = self.shell(cmd)

        activities = []
        activity = False
        for line in result.split(' '):
            if line == "ACTIVITY":
                activity = True
                continue

            if activity:
                activities.append(line)
                activity = False
        return activities
