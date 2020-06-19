import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 69 # TFTP Protocol Port (69)

# header opcode is 2 bytes
TFTP_OPCODES = {
    1: 'RRQ',
    2: 'WRQ',
    3: 'DATA',
    4: 'ACK',
    5: 'ERROR'
}
TRANSFER_MODES = ['netascii', 'octet', 'mail']
STATE = dict()


def send_data(block, filename, mode, socket, address):
    data = bytearray()
    # append data opcode (03)
    data.append(0)
    data.append(3)

    # append block number (2 bytes)
    b = f'{block:02}'
    data.append(int(b[0]))
    data.append(int(b[1]))

    # append data (512 bytes max)
    f = open(filename, 'rb') # ensure file exists
    offset = (block - 1) * 512
    f.seek(offset, 0)
    content = f.read(512)
    f.close()
    data += content

    # print(f'data: {data}')
    socket.sendto(data, address)


# Get opcode from TFTP header
def get_opcode(bytes):
    opcode = int.from_bytes(bytes[0:2], byteorder='big')
    if opcode not in TFTP_OPCODES.keys():
            # send error packet
            pass
    return TFTP_OPCODES[opcode]


def main():
    sock = create_udp_socket()
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f'data: {data}')
        print(f'addr: {addr}')

        opcode = get_opcode(data)
        if opcode == 'RRQ':
            header = data[2:].split(b'\x00')
            filename = header[0].decode('utf-8');
            mode = header[1].decode('utf-8').lower()

            if mode not in TRANSFER_MODES:
                # send error packet
                pass

            STATE[port] = {'filename': filename, 'mode': mode}
            print(f'state: {STATE}')
            send_data(1, filename, mode, sock, addr)



if __name__ == '__main__':
    main()
