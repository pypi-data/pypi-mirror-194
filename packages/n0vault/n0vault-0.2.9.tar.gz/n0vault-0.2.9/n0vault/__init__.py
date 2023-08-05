# 0.01 = 2021-03-06 = Initial version
# 0.02 = 2021-07-19 = Added functionality to enter sensitive data without easy retrieving
# 0.03 = 2021-08-04 Impossible easely adopt for 3.6, only for 3.7, because of some modules (for example: immutables) 
#                   are not precompiled for 3.6 at pypi.org. So installing of Visual C/C++ (or MinGW) is required.
# 0.04 = 2023-02-25 = AES.MODE_CBC -> AES.MODE_GCM accoding sonarcloud.io: Use secure mode and padding scheme.
import os
import base64

from Crypto.Cipher import AES
import Crypto.Util.Padding
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pbkdf2 import PBKDF2
# ##################################################################################################
from n0struct import *
# ##################################################################################################
class n0Vault(dict):
    _encrypted = False
    # Not crypted file format: ordinary json
    _encrypted = True  # Comment current line for not-crypted file format
    __vault_file_is_encrypted = None
    __password = None   # Used in case of _encrypted == True
    # Encrypted file format:
    #>> __sign   8 bytes: constant
    __sign = "n0Vault1"
    #>> flags    4 bytes: variable
    # File:     zzzz_zzzz_yyyy_yyyy_xxxx_xxxx_wwww_wwww
    # -> 'little endian' according to x86 architecture ->
    #     Native byte order is big-endian or little-endian, depending on the host system.
    #     For example, Intel x86 and AMD64 (x86-64) are little-endian;
    #     Motorola 68000 and PowerPC G5 are big-endian;
    #     ARM and Intel Itanium feature switchable endianness (bi-endian).
    #     Use sys.byteorder to check the endianness of your system.
    __flags = 0b0000_0000_0000_0000_0000_0000_0000_0000
    # Memory:   wwww_wwww_xxxx_xxxx_yyyy_yyyy_zzzz_zzzz
    #           ││││ ││││ ││││ ││││ ││││ ││││ ││││ ││││
    #           └┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┤│└┤
    #                                              ││ │
    #                                              ││ └─── 00 = AES encryption without password:
    #                                              ││               static 256-bit Key (self.__key)
    #                                              ││               + variable 128-bit Initialization Vector
    #                                              ││      01 = AES encryption WITH password:
    #                                              ││               static 256-bit Key (self.__key)
    #                                              ││               + variable 128-bit Initialization Vector
    #                                              │└───── 0  = possible to view and decrypt
    #                                              │       1  = viewing/decryption is not allowed
    #                                              └────── reserved for future usage
    #>> iv      16 bytes unique 16 bytes, generated every time during saving
    #>> sha256  32 bytes control sum of iv+buffer before encryption
    #   __vault .. bytes encrypted with AES
    _vault = None  # n0dict()
    # **********************************************************************************************
    # 32 bytes / 256-bit Key: key is used for encryption or like salt in case of encryption with password
    __key = 0xf1d0f3b89f3cf706af3303fb549e18ce22e1bc744d8994da859e4d4e7700ae7b.to_bytes(32, 'big')  # 'little endian' or 'big endian' is no different in this case
    vault_file_name = None
    # **********************************************************************************************
    def __init__(
        self,
        vault_file_name: str = None,
        encrypted = True,
        password: str = None,
        key = None
    ):
        """
        Constructor for n0Vault
        
        vault_file_name: str = None,    storage file name
        encrypted = True,               save as encrypted by default
        password: str = None,           password will be used during saving
        key = None                      256-bit Key encrypted with base64
        """
        if not vault_file_name:
            vault_file_name = os.path.splitext(os.path.split(__file__)[1])[0] + ".vault"
        self._encrypted = encrypted
        self.__password = password
        if key:
            self.__key = base64.b64decode(key)[:32]  # 256-bit Key encrypted with base64
        self.load(vault_file_name)
    # **********************************************************************************************
    def __setitem__(self, xpath: str, new_value):
        """
        Public operator: isntance[xpath] = new_value
        
        Update isntance._vault with {xpath:new_value}
        """
        self._vault[xpath] = new_value
        return new_value
    # **********************************************************************************************
    def update(self, xpath: typing.Union[dict, str], new_value: str = None) -> dict:
        """
        Public method: isntance.update(xpath: typing.Union[dict, str], new_value: str = None)
        
        Update isntance._vault with {xpath:new_value} or {xpath as a dictionary}
        """
        if isinstance(xpath, (dict, n0dict)):
            self._vault.update(xpath)
        elif isinstance(xpath, str):
            self._vault.update({xpath: new_value})
        else:
            raise TypeError(f"Expected: xpath: typing.Union[dict, str], new_value: str\nReceived: xpath:{type(xpath)}, new_value:{type(new_value)}")
            
        return self._vault
    # **********************************************************************************************
    def delete(self, xpath) -> dict:
        """
        Public method: isntance.delete(xpath)
        
        Delete item 'xpath' from isntance._vault
        """
        return self._vault.delete(xpath)
    # **********************************************************************************************
    def pop(self, xpath) -> dict:
        """
        Public method: isntance.pop(xpath)
        
        Return value associated with 'xpath' and delete item 'xpath' from isntance._vault
        """
        return self._vault.pop(xpath)
    # **********************************************************************************************
    def show(self, start_from = None) -> dict:
        """
        Public method: isntance.show(start_from = None)
        
        Return json structure of isntance._vault or isntance._vault[start_from]
        """
        return json.dumps(self._vault[start_from] if start_from else self._vault, indent = 4)
    # **********************************************************************************************
    def set_bits(self, bytes_array: int, bits_value: int, bits_len: int = 1, bits_offset: int = 0, bits_in_bytes: int = 32) -> int:
        """
        Public method: isntance.set_bits(bytes_array: int, bits_value: int, bits_len: int = 1, bits_offset: int = 0, bits_in_bytes: int = 32)
        
        Apply bits_value to bits_offset of bytes_array
        
        1) Prepare all bits mask depends of bits_in_bytes (bytes_array size): 0xFF, 0xFFFF, 0xFFFFFFFF
            bits_in_bytes =  8              => bits_mask = b0000_0000__0000_0000___0000_0000__1111_1111
            bits_in_bytes = 16              => bits_mask = b0000_0000__0000_0000___1111_1111__1111_1111
            bits_in_bytes = 32              => bits_mask = b1111_1111__1111_1111___1111_1111__1111_1111
        
        2) Prepare the mask for bits place clearing, depends of bits_len and bits_offset
            bits_len = 1, bits_offset = 0   => b0000_0000__0000_0000___0000_0000__0000_0001 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__1111_1110
            bits_len = 2, bits_offset = 0   => b0000_0000__0000_0000___0000_0000__0000_0011 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__1111_1100
            bits_len = 3, bits_offset = 0   => b0000_0000__0000_0000___0000_0000__0000_0111 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__1111_1000
            bits_len = 8, bits_offset = 0   => b0000_0000__0000_0000___0000_0000__1111_1111 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__0000_0000
                                                                                                                                                             
            bits_len = 1, bits_offset = 4   => b0000_0000__0000_0000___0000_0000__0001_0000 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__1110_1111
            bits_len = 2, bits_offset = 4   => b0000_0000__0000_0000___0000_0000__0011_0000 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__1100_1111
            bits_len = 3, bits_offset = 4   => b0000_0000__0000_0000___0000_0000__0111_0000 => clear_bits_mask = b1111_1111__1111_1111___1111_1111__1000_1111
            bits_len = 8, bits_offset = 4   => b0000_0000__0000_0000___0000_1111__1111_0000 => clear_bits_mask = b1111_1111__1111_1111___1111_0000__0000_1111
            
        3) Clearing the bits place 
        
        4) Update the cleared place with bits_value
        """
        all_bits_mask = (1 << bits_in_bytes) - 1
        clear_bits_mask = all_bits_mask ^ (( (1 << bits_len) - 1) << bits_offset)
        bytes_array &= clear_bits_mask
        bytes_array |= bits_value << bits_offset
        return bytes_array
    # **********************************************************************************************
    def is_bit_set(
        self,
        bit_offset: int = 0,
        binary_mask: int = 0b1,
        bytes_array: int = None
    ) -> int:
        """
        Public method: isntance.is_bit_set(bit_offset: int = 0, binary_mask: int = 0b1, bytes_array: int = None) -> int:
        
        Return bits' set from bit_offset of bytes_array/self.__flags and applied binary_mask
        """
        return ((bytes_array or self.__flags) >> bit_offset) & binary_mask
    # **********************************************************************************************
    def load(self, vault_file_name: str):
        """
        Public method: isntance.load(vault_file_name: str):

        Load 'vault_file_name' and decrypt it if it was encrypted.
        """
        def read_buffer(len_to_read = None, name = None):
            return in_file.read(len_to_read)

        self.vault_file_name = vault_file_name
        if os.path.exists(self.vault_file_name):
            with open(self.vault_file_name, "rb") as in_file:
                sign = read_buffer(1)
                if sign == b'{':
                    # Not-crypted storage
                    self.__vault_file_is_encrypted = False
                    self._vault = n0dict((sign + read_buffer()).decode("utf-8"))
                else:
                    # Encrypted storage
                    self.__vault_file_is_encrypted = True
                    sign += read_buffer(7, "sign")
                    if sign.decode("utf-8") != self.__sign:
                        raise Exception(f"File '{vault_file_name}' is not n0Vault storage")
                    # 4 bytes/32-bits flag
                    self.__flags = int.from_bytes(read_buffer(4, "flags"), 'little')
                    cipher_iv = read_buffer(16, "cipher_iv")
                    control_sum = read_buffer(32, "control_sum")
                    # ******************************************************************************
                    # ******************************************************************************
                    if self.is_bit_set(0, 0b11) == 0b00:
                        cipher = AES.new(self.__key, AES.MODE_GCM, cipher_iv)
                    elif self.is_bit_set(0, 0b11) == 0b01:
                        if not self.__password:
                            raise Exception(f"Password for loading is required")
                        cipher = AES.new(
                            PBKDF2(self.__password, self.__key[:16]).read(32),    # 256-bit key
                            AES.MODE_GCM,
                            cipher_iv
                        )
                    else:
                        raise Exception(f"Unknown format of encryption for n0Vault storage")
                    # ******************************************************************************
                    try:
                        buffer = Crypto.Util.Padding.unpad(
                                    cipher.decrypt(
                                            read_buffer(None, "encrypted buffer")
                                        ),
                                    AES.block_size
                        )
                    except:
                        raise Exception(f"Incorrect password for n0Vault storage")
                    # ******************************************************************************
                    # ******************************************************************************
                    calculated_control_sum = SHA256.new(data=cipher_iv + buffer).digest()
                    if control_sum != calculated_control_sum:
                        raise Exception(f"Incorrect control sum of n0Vault storage")
                    self._vault = n0dict(buffer.decode("utf-8"))

                if self._vault.get("__sign") != self.__sign:
                    raise Exception(f"Incorrect format of n0Vault storage")
        else:
            self._vault = n0dict({"__sign": self.__sign})
        return self._vault
    # **********************************************************************************************
    def save(self, new_vault_file_name: str = None, forbid_next_saving = False):
        """
        Public method: isntance.save(new_vault_file_name: str = None, forbid_next_saving = False):

        Save file depends of self._encrypted flag into encrypted or decrypted format.
        if 3rd bit in self.__flags is already set previously, then Exception will be raised -- saving is forbidden.
        """
        if self.is_bit_set(2, 0b1):
            raise Exception(f"Saving of such n0Vault storage is forbidden")
        # ******************************************************************************************
        def write_buffer(buffer: typing.Union[str, int, bytes], name_of_buffer: str):
            n0debug_calc(buffer, name_of_buffer)
            if isinstance(buffer, str):
                buffer = buffer.encode("utf-8")             # str -> bytes
            elif isinstance(buffer, int):
                buffer = buffer.to_bytes(4, 'little')       # int32 -> bytes
            elif not isinstance(buffer, bytes):
                raise(Exception(f"Expected type str or int for '{buffer}', but got {type(buffer)}"))
            out_file.write(buffer)
        # ******************************************************************************************
        with open(new_vault_file_name or self.vault_file_name, "wb") as out_file:
            if self._encrypted is None:
                self._encrypted = self.__vault_file_is_encrypted
            if self._encrypted:
                if self.__password:
                    self.__flags = self.set_bits(bytes_array = self.__flags, bits_value = 0b01, bits_len = 2, bits_offset = 0)
                    cipher = AES.new(
                        PBKDF2(self.__password, self.__key[:16]).read(32),          # Generate 256-bit key
                        AES.MODE_GCM
                    )
                else:
                    cipher = AES.new(self.__key, AES.MODE_GCM)
                write_buffer(self.__sign,  "sign")
                if forbid_next_saving:
                    self.__flags = self.set_bits(bytes_array = self.__flags, bits_value = 0b1, bits_len = 1, bits_offset = 2)
                write_buffer(self.__flags, "flags")
                write_buffer(cipher.iv,    "cipher.iv")
                buffer = n0pretty(self._vault, show_type=False, __indent_size = 0).encode("utf-8") # str -> bytes
                write_buffer(SHA256.new(data=cipher.iv + buffer).digest(), "control_sum")
                write_buffer(
                            cipher.encrypt(
                                    Crypto.Util.Padding.pad(
                                        buffer,
                                        AES.block_size
                                    )
                            ),
                            "encrypted buffer"
                )
            else:
                buffer = self.show().replace('\n', "\r\n").encode("utf-8")  # str -> bytes
                write_buffer(buffer, "notcrypted buffer")
    # **********************************************************************************************
    def __getitem__(self, xpath):
        """
        Public operator: isntance[xpath]
        return isntance._vault[where1/where2/.../whereN]
            AKA
        return isntance._vault[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        return self._vault._get(xpath, raise_exception = True)
    def get(self, xpath: str, if_not_found = None):
        """
        Public method: isntance.get(xpath: str, if_not_found = None)
        return _vault[where1/where2/.../whereN]
            AKA
        return _vault[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        return self._vault._get(xpath, raise_exception = False, if_not_found = if_not_found)
    # **********************************************************************************************
# ##################################################################################################
