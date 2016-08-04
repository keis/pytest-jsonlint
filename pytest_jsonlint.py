import pytest
import demjson


def pytest_collect_file(path, parent):
    if path.ext == '.json':
        return JSONFile(path, parent)


class JSONFile(pytest.File):
    def collect(self):
        yield JSONItem(self.fspath.strpath, self)


class JSONError(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


class JSONItem(pytest.Item):
    def runtest(self):
        with self.fspath.open() as fp:
            data = fp.read()
        results = demjson.decode(data, return_errors=True)
        if len(results.errors) > 0:
            raise JSONError(results.errors)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(JSONError):
            return '\n'.join(
                '%s - %s' % (err.message,err.position)
                for err in excinfo.value.errors[:10]
            )
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, 0, "jsonlint: %s" % self.name
