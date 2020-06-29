import ipaddress
import unittest
import ipprefix
from itertools import product
import timeit


class Test(unittest.TestCase):
    def test_ip4_prefix(self):
        testcases = (
            ([f'192.168.0.{i}' for i in range(255)], 24),

            ([f'192.168.0.{128 + 64}', '192.168.0.128'], 25),
            ([
                 f'192.168.0.{128}',
                 f'192.168.0.{128 + 64}',
                 f'192.168.0.{128 + 64 + 32}',
             ], 25),
            ([
                 '192.168.64.123',
                 '192.168.128.123',
             ], 16),
            (['192.168.0.254', '192.168.0.254'], 32),
            (['10.0.0.1', '192.168.0.128'], 0),
            (['ff::f0', 'ff::f1'], 127),
            (['ff::', 'ff::'], 128),

        )
        for tc in testcases:
            self.assertEqual(ipprefix.ip_subnet(tc[0]), tc[1], f'expected {tc[1]} prefix for ips: {tc[0]}')

    def test_MinMaxPrefixFinder_performance(self):
        """
        16   0.00012
        81   0.0006
        256  0.0019
        625  0.0047
        1296 0.012
        2401 0.018
        4096 0.031
        6561 0.049
        :return:
        """
        for n in range(1, 4):
            ints = range(n)
            ips = ['.'.join(map(str, i)) for i in product(ints, ints, ints, ints)]
            print(
                len(ips),
                timeit.timeit(lambda: ipprefix.MinMaxPrefixFinder().find_subnet(ips), number=1000) / 1000,
                timeit.timeit(lambda: ipprefix.VerticalBytePrefixFinder().find_subnet(ips), number=1000) / 1000
            )
        # print(ipprefix.ip_subnet(ips))

    def test_one_family(self):
        with self.assertRaises(BaseException):
            ipprefix.ip_subnet(['ff::', '127.0.0.1'])
