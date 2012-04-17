import subprocess, socket
from httplib import HTTPConnection
import urllib2
from urllib2 import *

class PipeSocket:
    def __init__(self, proc):
        self.proc = proc
        self.filecount = 0

    def write(self, data):
        return self.proc.stdin.write(data)

    def read(self, amt=None):
        return self.proc.stdout.read(amt)

    def readline(self, length=None):
        if length:
            return self.proc.stdout.readline(length)
        return self.proc.stdout.readline()

    def sendall(self, data):
        return self.write(data)

    def makefile(self, mode, buffering=0):
        self.filecount += 1
        return self

    def close(self):
        if self.filecount:
            self.filecount -= 1
            return
        self.proc.stdout.close()
        self.proc.stdin.close()
        self.proc.wait()

class HTTPSSHConnection(HTTPConnection):
    def __init__(self, host, **kw):
        self.user, self.host = host.split('@')
        HTTPConnection.__init__(self, self.host, **kw)

    def connect(self):
        p = subprocess.Popen(['ssh', '-T', '-l', self.user, self.host],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.sock = PipeSocket(p)

class HTTPSSHHandler(AbstractHTTPHandler):
    def httpssh_open(self, req):
        return self.do_open(HTTPSSHConnection, req)

# upload.py in 2.7 insists on only supporting http and https URLs
# Fake one, and make urlopen replace that with a httpssh URL
_goodprefix = 'httpssh://submit@pypi.python.org/pypi'
_badprefix = 'http://submit@pypi.python.org/pypi'
class PyPIOpenerDirector(OpenerDirector):
    def open(self, req, data=None):
        if isinstance(req, basestring):
            req = Request(req, data)
        else:
            if data is not None:
                req.add_data(data)
        if req.get_full_url().startswith(_badprefix):
            # parse type, then overwrite
            req.get_type()
            req.type = 'httpssh'
        return OpenerDirector.open(self, req, data=data)

# upload.py in 2.6 and earlier didn't use urllib, but httplib directly,
# so we have to patch the entire upload_file implementation
if sys.version_info < (2,7):
    from distutils import log
    from hashlib import md5
    from base64 import standard_b64encode
    import cStringIO as StringIO
    # copy based on 2.6.5
    def ssh_upload_file(self, command, pyversion, filename):
        assert self.repository == _badprefix
        # Sign if requested
        if self.sign:
            gpg_args = ["gpg", "--detach-sign", "-a", filename]
            if self.identity:
                gpg_args[2:2] = ["--local-user", self.identity]
            spawn(gpg_args,
                  dry_run=self.dry_run)

        # Fill in the data - send all the meta-data in case we need to
        # register a new release
        content = open(filename,'rb').read()
        meta = self.distribution.metadata
        data = {
            # action
            ':action': 'file_upload',
            'protcol_version': '1',

            # identify release
            'name': meta.get_name(),
            'version': meta.get_version(),

            # file content
            'content': (os.path.basename(filename),content),
            'filetype': command,
            'pyversion': pyversion,
            'md5_digest': md5(content).hexdigest(),

            # additional meta-data
            'metadata_version' : '1.0',
            'summary': meta.get_description(),
            'home_page': meta.get_url(),
            'author': meta.get_contact(),
            'author_email': meta.get_contact_email(),
            'license': meta.get_licence(),
            'description': meta.get_long_description(),
            'keywords': meta.get_keywords(),
            'platform': meta.get_platforms(),
            'classifiers': meta.get_classifiers(),
            'download_url': meta.get_download_url(),
            # PEP 314
            'provides': meta.get_provides(),
            'requires': meta.get_requires(),
            'obsoletes': meta.get_obsoletes(),
            }
        comment = ''
        if command == 'bdist_rpm':
            dist, version, id = platform.dist()
            if dist:
                comment = 'built for %s %s' % (dist, version)
        elif command == 'bdist_dumb':
            comment = 'built for %s' % platform.platform(terse=1)
        data['comment'] = comment

        if self.sign:
            data['gpg_signature'] = (os.path.basename(filename) + ".asc",
                                     open(filename+".asc").read())

        # set up the authentication
        auth = "Basic " + standard_b64encode(self.username + ":" +
                                             self.password)

        # Build up the MIME payload for the POST data
        boundary = '--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'
        sep_boundary = '\n--' + boundary
        end_boundary = sep_boundary + '--'
        body = StringIO.StringIO()
        for key, value in data.items():
            # handle multiple entries for the same name
            if type(value) != type([]):
                value = [value]
            for value in value:
                if type(value) is tuple:
                    fn = ';filename="%s"' % value[0]
                    value = value[1]
                else:
                    fn = ""

                body.write(sep_boundary)
                body.write('\nContent-Disposition: form-data; name="%s"'%key)
                body.write(fn)
                body.write("\n\n")
                body.write(value)
                if value and value[-1] == '\r':
                    body.write('\n')  # write an extra newline (lurve Macs)
        body.write(end_boundary)
        body.write("\n")
        body = body.getvalue()

        self.announce("Submitting %s to %s" % (filename, self.repository), log.INFO)

        # Start of patched block: unconditionally create HTTPSSHConnection
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(self.repository)
        http = HTTPSSHConnection(netloc)
        # end of patched block

        data = ''
        loglevel = log.INFO
        try:
            http.connect()
            http.putrequest("POST", url)
            http.putheader('Content-type',
                           'multipart/form-data; boundary=%s'%boundary)
            http.putheader('Content-length', str(len(body)))
            http.putheader('Authorization', auth)
            http.endheaders()
            http.send(body)
        except socket.error, e:
            self.announce(str(e), log.ERROR)
            return

        r = http.getresponse()
        if r.status == 200:
            self.announce('Server response (%s): %s' % (r.status, r.reason),
                          log.INFO)
        else:
            self.announce('Upload failed (%s): %s' % (r.status, r.reason),
                          log.ERROR)
        if self.show_response:
            print '-'*75, r.read(), '-'*75

def build_opener(*handlers):
    opener = urllib2.build_opener(HTTPSSHHandler, *handlers)
    # Monkey-patch class
    opener.__class__ = PyPIOpenerDirector
    return opener

_opener = None
def urlopen(req, data=None):
    global _opener
    if _opener is None:
        _opener = build_opener()
    return _opener.open(req, data)

def monkeypatch():
    import pypissh # ourselves
    from distutils.command import register, upload
    try:
        from distutils.config import PyPIRCCommand
    except ImportError:
        pass
    else:
        PyPIRCCommand.DEFAULT_REPOSITORY = _badprefix
    register.urllib2 = pypissh
    upload.urlopen = urlopen
    if sys.version_info < (2,7):
        upload.upload.upload_file = ssh_upload_file
    else:
        upload.urlopen = urlopen

if __name__=='__main__':
    f = urlopen('httpssh://submit@pypi.python.org/pypi')
    print f.read()
