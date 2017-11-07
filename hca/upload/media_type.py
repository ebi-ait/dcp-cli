import operator
import os
import re
import sys


class MediaType:

    DCP_METADATA_JSON_FILES = ('assay', 'project', 'sample')
    RFC7320_TOKEN_CHARSET = r"!#$%&'*+\-.^_`|~\w"
    _TYPE_REGEX = re.compile(
        r"(?P<top_level_type>.+)"  # 'application'
        r"/"                       # '/'
        r"(?P<subtype>[^+]+)"      # 'json'
        r"("                       # stat of suffix group
        r"\+(?P<suffix>.+)"        # '+zip'
        r")?"                      # end optional suffix group
    )
    _PARAM_REGEX = re.compile(
        r"\s*"                               # optional whitespace
        r"(?P<key>"                          # start of group 'key'
        r"[" + RFC7320_TOKEN_CHARSET + "]+"  # key
        r")"                                 # end of group 'key'
        r"\s*=\s*"                           # '='
        r"(?P<value>"                        # start of group 'value'
        r'"[^"]*"'                           # Any doublequoted string
        r"|"                                 # or
        "[" + RFC7320_TOKEN_CHARSET + "]*"   # A word of token-chars (doesn't need quoting)
        r")"                                 # end of group 'value'
        r"\s*(;|$)"                          # Ending either at semicolon, or EOS.
    )

    @classmethod
    def from_string(cls, media_type):
        first_semi_position = media_type.find(';')
        if first_semi_position == -1:
            type_info = media_type
            parameters = {}
        else:
            type_info = media_type[0:first_semi_position]
            parameters = MediaType._parse_parameters(media_type[first_semi_position + 1:])

        type_info = MediaType._TYPE_REGEX.match(type_info)

        return cls(
            type_info.group('top_level_type'), type_info.group('subtype'),
            suffix=type_info.group('suffix'), parameters=parameters)

    @staticmethod
    def _parse_parameters(params_string):
        parameters = {}
        cursor = 0
        string_length = len(params_string)

        while 0 <= cursor < string_length:
            match = MediaType._PARAM_REGEX.match(params_string, cursor)
            if not match:
                break
            parameters[match.group('key')] = match.group('value').strip('"')
            cursor = match.end(0)
        return parameters

    @classmethod
    def from_file(cls, file_path, dcp_type=None):
        media_type_string = cls._media_type_from_magic(file_path)
        media_type = cls.from_string(media_type_string)
        if dcp_type:
            media_type.parameters['dcp-type'] = dcp_type
        else:
            media_type.parameters['dcp-type'] = cls._dcp_media_type_param(media_type, os.path.basename(file_path))
        return media_type

    def __init__(self, top_level_type, subtype, suffix=None, parameters={}):
        self.top_level_type = top_level_type
        self.subtype = subtype
        self.suffix = suffix
        self.parameters = parameters

    def __str__(self):
        result = [self.main_type]
        if self.parameters:
            sorted_params = sorted(self.parameters.items(), key=operator.itemgetter(0))
            for k, v in sorted_params:
                result.append('{key}={value}'.format(key=k, value=self._properly_quoted_parameter_value(v)))
        return '; '.join(result)

    @property
    def main_type(self):
        maintype = "{type}/{subtype}".format(type=self.top_level_type, subtype=self.subtype)
        if self.suffix:
            maintype += "+" + self.suffix
        return maintype

    @staticmethod
    def _media_type_from_magic(file_path):
        """
        Use libmagic to generate a media-type for the file, then correct its mistakes.
        """
        libmagic = MediaType._load_libmagic()
        media_type = libmagic.from_file(file_path, mime=True)
        if media_type == 'text/plain':  # libmagic doesn't recognize JSON
            if file_path.endswith('.json'):
                media_type = 'application/json'
        elif media_type == 'application/x-gzip':  # deprecated
            media_type = 'application/gzip'
        return media_type

    @staticmethod
    def _load_libmagic():
        try:
            import magic
        except ImportError:
            sys.stderr.write("\nThe 'hca upload file' command requires the 'libmagic' library to be installed.\n"
                             "Please install it, e.g. on Mac OS X: brew install libmagic\n\n")
            sys.exit(1)
        return magic

    @staticmethod
    def _dcp_media_type_param(media_type, filename):
        if media_type.main_type == 'application/json':
            (filename_without_extension, ext) = os.path.splitext(filename)
            if filename_without_extension in MediaType.DCP_METADATA_JSON_FILES:
                return "metadata/{filename}".format(filename=filename_without_extension)
            else:
                return "metadata"
        else:
            return "data"

    @staticmethod
    def _properly_quoted_parameter_value(value):
        """
        Per RFC 7321 (https://tools.ietf.org/html/rfc7231#section-3.1.1.1):
        Parameters values don't need to be quoted if they are a "token".
        Token characters are defined by RFC 7320 (https://tools.ietf.org/html/rfc7230#section-3.2.6).
        Otherwise, parameters values can be a "quoted-string".
        So we will quote values that contain characters other than the standard token characters.
        """
        if re.match("^[{charset}]*$".format(charset=MediaType.RFC7320_TOKEN_CHARSET), value):
            return value
        else:
            return '"{}"'.format(value)
