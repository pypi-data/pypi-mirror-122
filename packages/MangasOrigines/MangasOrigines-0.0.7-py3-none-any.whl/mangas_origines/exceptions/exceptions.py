class ScanNotFound(Exception):
    def __init__(self, scan: str):
        super().__init__(f"I can't find {scan}!")


class WrongDomain(Exception):
    def __init__(self):
        super().__init__('This program only work with mangas-origines.fr.')


class BadScanIdFormat(Exception):
    def __init__(self):
        super().__init__("I can't get scan ID.")


class ChapterDoesNotExist(Exception):
    def __init__(self, chapter_url):
        super().__init__(f"The chapter: {chapter_url} doesn't exist.")


class LoginError(Exception):
    def __init__(self):
        super().__init__(f'Your credentials are probably wrong.')


class MangasOriginesNotAvailable(Exception):
    def __init__(self, error_code: int):
        self.error_code = str(error_code)
        super().__init__(f'Mangas Origines is not available, error: {self.error_code}!')
