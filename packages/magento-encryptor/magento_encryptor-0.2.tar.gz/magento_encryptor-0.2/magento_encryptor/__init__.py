import hashlib
import nacl.pwhash.argon2id
import re
from itertools import cycle, islice
from functools import reduce

HASH_VERSION_MD5 = 0
HASH_VERSION_SHA256 = 1
HASH_VERSION_ARGON2ID13 = 2
HASH_VERSION_ARGON2ID13_AGNOSTIC = 3

algo = {
    HASH_VERSION_MD5: "md5",
    HASH_VERSION_SHA256: "sha256",
}

SODIUM_CRYPTO_PWHASH_SALTBYTES = 16

AGNOSTIC_ARGON_REGEX = re.compile(
    r'^' +
    str(HASH_VERSION_ARGON2ID13_AGNOSTIC) +
    r'\_(?P<seed>\d+)\_(?P<ops>\d+)\_(?P<mem>\d+)$'
)

def do_hash(version, data, salt):
    version_id = int(version.split("_", 1)[0])
    if version_id == HASH_VERSION_ARGON2ID13_AGNOSTIC:
        argon_match = AGNOSTIC_ARGON_REGEX.match(version)
        settings = argon_match.groupdict()
        salt = bytes(islice(cycle(salt.encode()), 0, nacl.pwhash.argon2id.SALTBYTES))
        return nacl.pwhash.argon2id.kdf(
            int(settings["seed"]),
            data.encode(),
            salt,
            int(settings["ops"]),
            int(settings["mem"]),
        ).hex()

    if version_id == HASH_VERSION_ARGON2ID13:
        salt = bytes(islice(cycle(salt.encode()), 0, nacl.pwhash.argon2id.SALTBYTES))
        return nacl.pwhash.argon2id.kdf(
            32,
            data.encode(),
            salt,
            nacl.pwhash.argon2id.OPSLIMIT_INTERACTIVE,
            nacl.pwhash.argon2id.MEMLIMIT_INTERACTIVE,
        ).hex()

    if version_id not in algo:
        raise ValueError("Unknown hash version: " + str(version))

    hasher = hashlib.new(algo[version_id])
    hasher.update(salt.encode() + data.encode())
    return hasher.hexdigest()


def _explode_hash(hash_):
    hash_, salt, version = hash_.split(":", 2)
    if not version:
        version = "1"
    versions = version.split(":")
    return hash_, salt, versions


def verify(password, hash_):
    recreated = password
    hash_, salt, versions = _explode_hash(hash_)
    password_hash = reduce(lambda h, v: do_hash(v, h, salt), versions, password)

    return password_hash == hash_
