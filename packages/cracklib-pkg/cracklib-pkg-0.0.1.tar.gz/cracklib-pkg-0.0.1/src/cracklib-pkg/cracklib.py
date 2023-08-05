# use import Hashlib for crack

import hashlib


class Cracker:
    def __init__(self, string):
        self.string = string
        self.md5hash = hashlib.md5(self.string.encode('utf-8')).hexdigest()
        self.sha1hash = hashlib.sha1(self.string.encode('utf-8')).hexdigest()
        self.sha224hash = hashlib.sha224(
            self.string.encode('utf-8')).hexdigest()
        self.sha512hash = hashlib.sha512(
            self.string.encode('utf-8')).hexdigest()
        self.sha256hash = hashlib.sha256(
            self.string.encode('utf-8')).hexdigest()
        self.sha384hash = hashlib.sha384(
            self.string.encode('utf-8')).hexdigest()
        self.sha3_224hash = hashlib.sha3_224(
            self.string.encode('utf-8')).hexdigest()
        self.sha3_256hash = hashlib.sha3_256(
            self.string.encode('utf-8')).hexdigest()
        self.sha3_384hash = hashlib.sha3_384(
            self.string.encode('utf-8')).hexdigest()
        self.sha3_512hash = hashlib.sha3_512(
            self.string.encode('utf-8')).hexdigest()

    def crackHash(self, cracker):
        # md5 Hash
        if cracker == self.md5hash:
            return True

        # sha1 Hash
        if cracker == self.sha1hash:
            return True

        # sha224 Hash
        if cracker == self.sha224hash:
            return True

        # sha512 Hash
        if cracker == self.sha512hash:
            return True

        # sha384 Hash
        if cracker == self.sha384hash:
            return True

        # sha256 Hash
        if cracker == self.sha256hash:
            return True

        # sha3_224 Hash
        if cracker == self.sha3_224hash:
            return True

        # sha3_256
        if cracker == self.sha3_256hash:
            return True

        # sha3_384 Hash
        if cracker == self.sha3_384hash:
            return True

        # sha3_512 Hash
        if cracker == self.sha3_512hash:
            return True
        return False


# Thx Spooky Sec
