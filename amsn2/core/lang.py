
from os import path
import re

class aMSNLang(object):
    lang_keys = {}
    lang_dirs = []
    base_lang = 'en'
    lang_code = base_lang

    default_encoding = 'utf-8'

    lineRe  = re.compile('\s*([^\s]+)\s+(.+)', re.UNICODE)  # whitespace? + key + whitespace + value
    langRe  = re.compile('(.+)-.+', re.UNICODE)             # code or code-variant

    def load_lang(self, lang_code, force_reload=False):
        if self.lang_code is lang_code and force_reload is False:
            # Don't reload the same lang unless forced.
            return

        hasVariant = (self.langRe.match(lang_code) is not None)

        # Check for lang variants.
        if hasVariant:
            root = str(self.langRe.split(lang_code)[1])
        else:
            root = lang_code

        if lang_code is self.base_lang:
            # Clear the keys if we're loading the base lang.
            self.clearKeys()

        if root is not self.base_lang:
            # If it's not the default lang, load the base first.
            self.load_lang(self.base_lang)

        if hasVariant:
            # Then we have a variant, so load the root.
            self.load_lang(root)

        # Load the langfile from each langdir.
        fileWasLoaded = False
        for dir in self.get_lang_dirs():
            try:
                f = file(path.join(dir, 'lang' + lang_code), 'r')
                fileWasLoaded = True
            except IOError:
                # file doesn't exist.
                continue

            line = f.readline()
            while line:
                if self.lineRe.match(line) is not None:
                    components = self.lineRe.split(line)
                    self.set_key(unicode(components[1], self.default_encoding), unicode(components[2], self.default_encoding))

                # Get the next line...
                line = f.readline()

            f.close()

        # If we've loaded a lang file, set the new lang code.
        if fileWasLoaded:
            self.lang_code = lang_code

    def add_lang_dir(self, lang_dir):
        self.lang_dirs.append(str(lang_dir))
        self.reload_keys()

    def remove_lang_dir(self, lang_dir):
        try:
            # Remove the lang_dir from the lang_dirs list, and reload keys.
            self.lang_dirs.remove(str(lang_dir))
            self.reload_keys()
            return True
        except ValueError:
            # Dir not in list.
            return False

    def get_lang_dirs(self):
        # Return a copy for them to play with.
        return self.lang_dirs[:]

    def clear_lang_dirs(self):
        self.lang_dirs = []
        self.clear_keys()

    def reload_keys(self):
        self.load_lang(self.lang_code, True)

    def set_key(self, key, val):
        self.lang_keys[key] = val

    def get_key(self, key, replacements=[]):
        try:
            r = self.lang_keys[key]
        except KeyError:
            # Key doesn't exist.
            return key

        # Perform any replacements necessary.
        if type(replacements) is dict:
            # Replace from a dictionary.
            for key, val in replacements.iteritems():
                r = r.replace(key, val)
        else:
            # Replace each occurence of $i with an item from the replacements list.
            i = 1
            for replacement in replacements:
                r = r.replace('$' + str(i), replacement)
                i += 1

        return r

    def clear_keys(self):
        self.lang_keys = {}

    def print_keys(self):
        print self.lang_code
        print '{'
        for key, val in self.lang_keys.iteritems():
            print "\t[" + key + '] =>' + "\t" + '\'' + val + '\''
        print '}'

lang = aMSNLang()
