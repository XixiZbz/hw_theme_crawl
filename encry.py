# -*- coding: utf-8 -*-

def encrypt_key(data_str):
    base64charStr = '1ORQFEHGJILKNM0ADCTS6UiWZYba3cfehg9Xlknmpo2qtsvu8wzyPBdr547Vjx+/0'
    base64char = bytearray(base64charStr.encode('utf-8'))
    base64char[0x40] = 0x00

    v1 = list(data_str.encode('utf-8'))
    v2 = len(v1)
    v3 = v2
    v4 = int(v2 / 3)
    if v3 - 3 * v4 > 0:
        v4 = v4 + 1

    v5 = bytearray(4 * v4 | 1)
    v6 = 0
    v7 = 0
    v8 = 0
    v9 = 0
    v10 = 0
    v11 = 0
    v12 = 0
    v13 = 0
    v14 = 0
    v15 = 0
    if v3 >= 1:
        v7 = 0
        v6 = 0
        while True:
            if v7 >= v3:
                v9 = 0
                v10 = 0
            else:
                v8 = 0
                v9 = 0
                while True:
                    v9 = v1[v7 + v8] | (v9 << 8)
                    v10 = v8 + 1
                    if v8 > 1:
                        break
                    v11 = v7 + v8
                    v8 = v8 + 1;
                    if v11 + 1 >= v3:
                        break
                v7 += v10
            v12 = 18
            v13 = v9 << (24 - 8 * v10)
            v14 = 0
            while True:
                if v10 < v14:
                    v15 = 0x40
                else:
                    v15 = (v13 >> v12) & 0x3F
                v12 -= 6
                v5[v6 + v14] = base64char[v15]
                v14 = v14 + 1
                if v14 == 4:
                    break
            v6 += 4
            if v7 >= v3:
                break
    v5[v6] = 0x00
    ret_str = v5.decode().strip().strip(b'\x00'.decode())
    return ret_str

if __name__ == '__main__':
    data_str = '{"o":"","resId":"900001184","tt":"9"}'
    ret = encrypt_key(data_str)
    print(ret)