import os

class base_case(object):
    # Parent class for case handlers
    
    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            handler.handle_error(msg)
    
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    
    def test(self, handler):
        assert False, 'Not implemented.'
    
    def act(self, handler):
        assert False, 'Not implemented.'

class case_no_file(base_case):
    # File or dir doesn't exist

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise Exception("'%s' not found" % handler.path)

class case_existing_file(base_case):
    # File exists

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)

class case_directory_index_file(base_case):
    # Serve index.html page for dir
    
    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))
    
    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

class case_directory_no_index_file(base_case):
    # Serve listing for dir without index page

    def test(self, handler):
        return os.path.isdir(handler.full_path) and not os.path.isfile(self.index_path(handler))
    
    def act(self, handler):
        handler.list_dir(handler.full_path)

class case_cgi_file(base_case):
    # Something runnable

    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')
    
    def act(self, handler):
        handler.run_cgi(handler.full_path)

class case_always_fail(base_case):
    # Base case if nothing else worked

    def test(self, handler):
        return True
    
    def act(self, handler):
        raise Exception("Unknown object %s" % handler.path)