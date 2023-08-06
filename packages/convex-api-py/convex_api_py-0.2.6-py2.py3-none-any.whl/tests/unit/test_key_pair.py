"""

    Test KeyPair class

"""
import os
import pytest
import secrets


from convex_api.key_pair import KeyPair
from convex_api.utils import (
    to_bytes,
    remove_0x_prefix
)



SIGN_HASH_TEXT = '5bb1ce718241bfec110552b86bb7cccf0d95b8a5f462fbf6dff7c48543622ba5'
SIGN_TEXT = '0x7eceffab47295be3891ea745838a99102bfaf525ec43632366c7ec3f54db4822b5d581573aecde94c420554f963baebbf412e4304ad8636886ddfa7b1049f70e'
def test_key_pair_create_new():
    key_pair = KeyPair()
    assert(key_pair)
    assert(key_pair.public_key)


def test_key_pair_create_from_bytes(test_key_pair_info):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key == test_key_pair_info['public_key'].lower())

def test_key_pair_address_bytes(test_key_pair_info):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key_bytes == to_bytes(hexstr=test_key_pair_info['public_key']))

def test_key_pair_address_api(test_key_pair_info):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key_api == remove_0x_prefix(test_key_pair_info['public_key']))

def test_key_pair_address_checksum(test_key_pair_info):
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    assert(key_pair)
    assert(key_pair.public_key_checksum == test_key_pair_info['public_key'])

def test_key_pair_sign(test_key_pair_info):
    hash_text = SIGN_HASH_TEXT
    key_pair = KeyPair.import_from_bytes(test_key_pair_info['private_bytes'])
    sign_data = key_pair.sign(hash_text)
    assert(sign_data == SIGN_TEXT)


def test_key_pair_import_export_to_text(test_key_pair):
    password = 'secret'
    text = test_key_pair.export_to_text(password)
    import_key_pair = KeyPair.import_from_text(text, password)
    assert(import_key_pair)
    assert(import_key_pair.public_key == test_key_pair.public_key)


def test_key_pair_import_export_to_file(test_key_pair):
    filename = '/tmp/private_key.pem'
    password = 'secret'
    if os.path.exists(filename):
        os.remove(filename)

    text = test_key_pair.export_to_file(filename, password)
    assert(os.path.exists(filename))
    import_key_pair = KeyPair.import_from_file(filename, password)
    assert(import_key_pair)
    assert(import_key_pair.public_key == test_key_pair.public_key)
    os.remove(filename)

def test_key_pair_export_to_mnemonic(test_key_pair):
    words = test_key_pair.export_to_mnemonic
    assert(words)
    new_key_pair = KeyPair.import_from_mnemonic(words)
    assert(new_key_pair)
    assert(test_key_pair.public_key == new_key_pair.public_key)
    assert(test_key_pair.export_to_mnemonic == new_key_pair.export_to_mnemonic)

def test_key_pair_is_equal(test_key_pair):
    key_pair = KeyPair()
    assert(test_key_pair.is_equal(test_key_pair))
    assert(test_key_pair.is_equal(test_key_pair.public_key_api))
    assert(test_key_pair.is_equal(test_key_pair.public_key))
    assert(not key_pair.is_equal(test_key_pair.public_key_checksum))
    assert(not key_pair.is_equal(test_key_pair))
    with pytest.raises(TypeError):
        assert(not key_pair.is_equal(test_key_pair.public_key_bytes))
