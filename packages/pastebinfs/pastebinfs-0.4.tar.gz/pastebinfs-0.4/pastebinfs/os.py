from pastebinfs.parse_path import parse_path
from pastebinfs.pastebin import pastebinapi
from dataclasses import dataclass

@dataclass(init=False)
class patebin_stat_result:
    st_size: int  # size of file, in bytes please remind: Binary files are base64 encoded so this might be off
    st_updatetime: int  # time of file creation(or last update)
    st_mode: int  # protection modes, public = 0, unlisted = 1, private = 2
    st_key: str  # the paste key

def stat(path: str, api_key: str, user_key: str) -> patebin_stat_result:
    """Get infos to a file at ``path``

    Return a ``patebin_stat_result`` that give information's about the file at ``path``.
    If there are multiple pastes with the same name, the first one is used.

    Arguments:
        path {str} -- path of the file

        api_key {str} -- the api_key of the application.

        username {str} -- the username of the user that wants to login.

        password {str} -- the password of the user that wants to login.

    Returns:
        file_info {patebin_stat_result} -- A Object of ``patebin_stat_result`` containing infos about the queried file.

    Raises:
        FileNotFoundError: If the file at ``path`` can't be found.
    """
    path = parse_path(path)
    pastes_metadata = pastebinapi.get_meta_data_for_path(path, api_key, user_key)    
    if not pastes_metadata:
        raise FileNotFoundError("cant find file")

    first_paste = pastes_metadata[0]

    stat_result = patebin_stat_result()
    stat_result.st_size = int(first_paste['paste_size'])
    stat_result.st_updatetime = int(first_paste['paste_date'])
    stat_result.st_mode = int(first_paste['paste_private'])
    stat_result.st_key = first_paste['paste_key']
    return stat_result


def cp(from_path: str, to_path: str, api_key: str, user_key: str) -> str:
    """Copy a file form ``from_path`` to ``to_path``

    Copy a file form ``from_path`` to ``to_path`` and return new file id.

    Arguments:
        from_path {str} -- path of the file to copy from.

        to_path {str} -- path where the file will be copied to.

        api_key {str} -- the api_key of the application.

        username {str} -- the username of the user that wants to login.

        password {str} -- the password of the user that wants to login.

    Returns:
        file_id {patebin_stat_result} -- the id of the new file.

    Raises:
        FileNotFoundError: If the file at ``from_path`` can't be found.        
    """
    raise NotImplementedError("copy is not yet supported")


def move(from_path: str, to_path: str, api_key: str, user_key: str) -> int:  
    """Moves a file form ``from_path`` to ``to_path``

    Moves a file form ``from_path`` to ``to_path`` and return new file id.

    Arguments:
        from_path {str} -- path of the file to move from.

        to_path {str} -- path where the file will be moved to.

        api_key {str} -- the api_key of the application.

        username {str} -- the username of the user that wants to login.

        password {str} -- the password of the user that wants to login.

    Returns:
        file_id {patebin_stat_result} -- the id of the new file.

    Raises:
        FileNotFoundError: If the file at ``from_path`` can't be found.        
    """
    raise NotImplementedError("move is not yet supported")
