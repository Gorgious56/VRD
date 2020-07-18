import bpy


class EventWatcher:
    # Set of watchers
    event_watchers = set()

    @staticmethod
    def add_watcher(watcher):
        EventWatcher.event_watchers.add(watcher)

    @staticmethod
    def remove_watcher(watcher):
        EventWatcher.event_watchers.remove(watcher)

    @staticmethod
    def remove_all_watchers():
        EventWatcher.event_watchers.clear()

    # From 'context', 'path' needs to exist
    # 'comparer' is to compare the previous value of context.path to its new value
    # 'callback' is the cb called if the value if changed
    # 'copyValue' indicates if the value needs to be copied (that can be needed as if not old and new value may point onto the same object)
    def __init__(self, context, path, copymethod, comparer, callback, callback_args, copyValue):
        self.context = context
        self.path = path
        self.copymethod = copymethod
        self.comparer = comparer
        self.callback = callback
        self.copyValue = copyValue
        self.callback_args = callback_args
        self.currentValue = self.get_value()

    def get_value(self):
        split_path = self.path.split(".")
        attr_path = split_path[0]
        if not hasattr(self.context, attr_path):
            print(f"Error : {self.context} does not have any attribute named {attr_path}")
            return None
        value = getattr(self.context, split_path[0])  # Access 1st member of the property path
        for depth in range(len(split_path[1::])):  # Iteratively access the other members
            attr_path = split_path[depth + 1]
            if not hasattr(value, attr_path):
                print(f"Error : {value} does not have any attribute named {attr_path}")
                break
            value = getattr(value, attr_path)
        if self.copyValue and hasattr(value, self.copymethod):
            value = getattr(value, self.copymethod)()
        return value

    def fire(self):
        newValue = self.get_value()
        if not self.comparer(self.currentValue, newValue):
            self.currentValue = newValue
            self.callback(self, self.callback_args)

    def cb_scene_update(context):
        for ew in EventWatcher.event_watchers:
            ew.fire()

    @classmethod
    def register(self):
        self.unregister()
        bpy.app.handlers.depsgraph_update_post.append(self.cb_scene_update)

    @classmethod
    def unregister(self):
        if self.cb_scene_update in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(self.cb_scene_update)
