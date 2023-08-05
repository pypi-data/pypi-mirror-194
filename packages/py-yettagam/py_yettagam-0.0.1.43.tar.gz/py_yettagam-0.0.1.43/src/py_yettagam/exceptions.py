class ServiceDoesNotExistError(Exception):
    pass

class ServiceInactiveError(Exception):
    pass

class StorageConnectionRefusedError(Exception):
    pass

class StorageClientAlreadyInitializedError(Exception):
    pass

class StorageError(Exception):
    pass