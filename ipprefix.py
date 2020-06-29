from typing import List
import ipaddress


class VerticalBytePrefixFinder:
    def find_subnet(self, ips: List[str]):
        if len(ips) == 0:
            return 0
        packs = [ipaddress.ip_address(ip).packed for ip in ips]
        byte_pos = self.find_first_byte_differ_position(packs)
        bytes_to_compare = [b[byte_pos] for b in packs]
        common_bits = self.find_common_bits_count(bytes_to_compare)
        prefix = byte_pos * 8 + common_bits

        return prefix

    def find_common_bits_count(self, bytes_to_compare: List[int]):
        common_bits = 0
        while common_bits < 8:
            mask = 1 << (7-common_bits)
            prefix = bytes_to_compare[0] & mask
            for b in bytes_to_compare[1:]:
                if prefix != (b & mask):
                    return common_bits
            common_bits += 1
        return common_bits

    def find_first_byte_differ_position(self, packs):
        i = 0
        for i, b in enumerate(packs[0]):
            for ip in packs[1:]:
                if b != ip[i]:
                    return i
        return i


class MinMaxPrefixFinder:
    def find_subnet(self, ips: List[str]):
        min_ip, max_ip = self.min_max(ips)
        return self.common_subnet(min_ip, max_ip)

    def min_max(self, ips):
        first = ipaddress.ip_address(ips[0])
        min_ip = max_ip = first
        for ip in [ipaddress.ip_address(ip) for ip in ips[1:]]:
            if min_ip > ip:
                min_ip = ip
            if max_ip < ip:
                max_ip = ip
        return min_ip, max_ip

    def common_subnet(self, min_ip, max_ip):
        shift_count = 0
        min_ip_int = int(min_ip)
        max_ip_int = int(max_ip)
        while min_ip_int != max_ip_int:
            min_ip_int >>= 1
            max_ip_int >>= 1
            shift_count += 1
        return min_ip.max_prefixlen - shift_count


def ip_subnet(ips: List[str]):
    if len(ips) == 0:
        return 0
    return MinMaxPrefixFinder().find_subnet(ips)
