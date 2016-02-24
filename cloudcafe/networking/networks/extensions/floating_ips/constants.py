
COMMON_ROOT_TAG = 'floatingip'


class FloatingIPStates(object):
    ACTIVE = 'ACTIVE'
    DOWN = 'DOWN'
    ERROR = 'ERROR'


class FLIPResponseCodes(object):
    CREATE_SUCCESS = 201
    LIST_SUCCESS = 200
    UPDATE_SUCCESS = 202
    DELETE_SUCCESS = 204

    NOT_FOUND = 404
