import struct


class PacketParser:
    def __init__(self, data):
        self.data = data
        self.header = self.parse_header()
        self.flags = '0' * (16 - len(bin(self.header[1])) + 2) + str(bin(self.header[1]))[2:]
        self.is_answer = self.flags[0]
        self.qname, self.qtype, position = self.parse_question()
        self.question_len = position
        self.info = None
        if self.is_answer:
            self.info = self.parse_body(position)

    def parse_header(self):
        header = struct.unpack("!6H", self.data[:12])
        return header

    def parse_question(self):
        name, end = self.parse_domain(12)
        q_type, q_class = struct.unpack("!HH", self.data[end: end + 4])
        return name, q_type, end + 4

    def parse_domain(self, start):
        domain_list = []
        position = start
        end = start
        flag = False
        while True:
            if self.data[position] > 63:
                if not flag:
                    end = position + 2
                    flag = True
                position = ((self.data[position] - 192) << 8) + self.data[position + 1]
                continue
            else:
                length = self.data[position]
                if length == 0:
                    if not flag:
                        end = position + 1
                        flag = True
                    break
                position += 1
                domain_list.append(self.data[position: position + length])
                position += length
        domain = ".".join([i.decode('ascii') for i in domain_list])
        return domain, end

    def parse_body(self, start):
        answer, an_offset = self.parse_rr(start, 3)
        authority, auth_offset = self.parse_rr(an_offset, 4)
        additional = self.parse_rr(auth_offset, 5)[0]
        return answer + authority + additional

    def parse_rr(self, start, number):
        offset = start
        rr_list = []
        for i in range(self.header[number]):
            name, end = self.parse_domain(offset)
            offset = end
            r_type, r_class, r_ttl, rd_length = struct.unpack("!2HIH", self.data[offset: offset + 10])
            offset += 10
            if r_type == 1:
                ip = struct.unpack("!4B", self.data[offset: offset + 4])
                offset += 4
                rr_list.append((name, r_type, r_ttl, ip))
            elif r_type == 2:
                dns_server_name, dns_name_end = self.parse_domain(offset)
                offset = dns_name_end
                rr_list.append((name, r_type, r_ttl, dns_server_name))
            else:
                offset += rd_length
        return rr_list, offset

    def get_response(self, data):
        length = 0
        item = b''
        ttl = data[2]
        value = data[0]
        header = list(self.header[:12])
        header[1] = 2 ** 15
        header[3] = 1
        question = self.data[12: self.question_len]
        name = self.data[12: self.question_len - 4]
        if self.qtype == 1:
            item = struct.pack("!4B", *value)
            length = 4
        if self.qtype == 2:
            octets = (name.decode()).split(".")
            result = []
            for o in octets:
                result.append(len(o))
                for l in o:
                    result.append(ord(l))
            result.append(0)
            item = struct.pack("!" + str(len(result)) + "B", *result)
            length = len(item)

        tail = struct.pack("!HHIH", self.qtype, 1, ttl, length)
        response = struct.pack("!6H", *header) + question + name + tail + item
        return response
