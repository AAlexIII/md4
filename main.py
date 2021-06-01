import struct


class MD4:
    width = 32
    # единичный бит
    mask = 0xFFFFFFFF

    # начальные значения A B C D
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]

    def __init__(self, mes=None):
        """mes: сообщение для шифровки"""

        if mes is None:
            mes = b""

        self.mes = mes

        # длина сообщения в битах
        ml = len(mes) * 8
        # обязательный 1 бит
        mes += b"\x80"
        # добавляем 0 биты до нужной кратности
        mes += b"\x00" * (-(len(mes) + 8) % 64)
        # 64-битное представление длины сообщения перед добавлением набивочных битов
        mes += struct.pack("<Q", ml)

        # передаём масив разбитый по 64 байта для дальнейших шагов
        self._process([mes[i: i + 64] for i in range(0, len(mes), 64)])

    def __str__(self):
        return self.hexdigest()

    def __eq__(self, other):
        return self.h == other.h

    def bytes(self):
        """Возвращает хэш в битовом представление"""
        return struct.pack("<4L", *self.h)

    def hexbytes(self):
        """перевод в байты"""
        return self.hexdigest().encode

    def hexdigest(self):
        """хэш в строчку"""
        return "".join(f"{value:02x}" for value in self.bytes())

    def _process(self, groups):
        for group in groups:
            X, h = list(struct.unpack("<16I", group)), self.h.copy()

            # раунд 1
            # цикл для упрощения кода
            Xi = [3, 7, 11, 19]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))  # игра с индексами
                K, S = n, Xi[n % 4]
                hn = h[i] + F(h[j], h[k], h[l]) + X[K]
                h[i] = lrot(hn & MD4.mask, S)

            # раунд 2
            Xi = [3, 5, 9, 13]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n % 4 * 4 + n // 4, Xi[n % 4]
                hn = h[i] + G(h[j], h[k], h[l]) + X[K] + 0x5A827999
                h[i] = lrot(hn & MD4.mask, S)

            # раунд 3
            Xi = [3, 9, 11, 15]
            Ki = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = Ki[n], Xi[n % 4]
                hn = h[i] + H(h[j], h[k], h[l]) + X[K] + 0x6ED9EBA1
                h[i] = lrot(hn & MD4.mask, S)

            """
            A = A + AA
            B = B + BB
            C = C + CC
            D = D + DD
            """
            self.h = [((v + n) & MD4.mask) for v, n in zip(self.h, h)]


# вспомогательные операции
def F(x, y, z):
    return (x & y) | (~x & z)


def G(x, y, z):
    return (x & y) | (x & z) | (y & z)


def H(x, y, z):
    return x ^ y ^ z


def lrot(value, n):
    lbits, rbits = (value << n) & MD4.mask, value >> (MD4.width - n)
    return lbits | rbits


def main():
    messages = ["ГЭУ", "СПбГЭУ", "ИБ"]

    known_hashes = [
        "f68768d323b98ecff599214772577e93",
        "017630f6dada7539e80fb7fa1c73b327",
        "0e80e59b9f32eb85f497e2c8dde023da"
    ]

    print("Test  MD4")
    print()

    for message, expected in zip(messages, known_hashes):
        print("Сообщение: ", message)
        print("Проверка:  ", expected)
        print("Результат: ", MD4(message.encode()).hexdigest())
        print()


if __name__ == "__main__":
    main()
