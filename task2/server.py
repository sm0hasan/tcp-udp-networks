import socket

# Spaces any hex code to the appropriate format
def hex_spacer(str):
    # remove spaces
    array_str = space_remover(str)
    # add spaces after every second indice
    array_str = ' '.join(array_str[i:i+2] for i in range(0, len(array_str), 2))
    # print(array_str)
    return array_str

# Removes any extra spaces within a string
def space_remover(str):
    array_str = str.replace(" ", "")
    return array_str

# Parses the query header into an array
def query_header(str):
    str = space_remover(str)
    header = str[:24]
    header_parted = [header[:4], header[4:8], header[8:12], header[12:16], header[16:20], header[20:24]]
    # print(header)
    # print(header_parted)
    return header_parted

# Parses the query question into an array
def query_question(str):
    str = space_remover(str)
    question = str[24:]
    question_parted = [question[i:i+2] for i in range(0, len(question), 2)]
    # print(question)
    # print(question_parted)
    return question_parted

# Converts a hex string to char
def hex_to_char(hex_string):
    hex_string = space_remover(hex_string)
    byte_array = bytearray.fromhex(hex_string)  
    ascii_string = byte_array.decode("ASCII")  
    return ascii_string
    # print(ascii_string)

# Takes an query question array and outputs the domain name
def recieved_domain_name(question_section):
    domain_len = question_section[0]
    decimal_domain_len = int(domain_len, 16)
    sliced_array = question_section[1:decimal_domain_len+1]
    hex_domain_name = " ".join(sliced_array)
    domain_name = hex_to_char(hex_domain_name)
    
    domain_type_len = question_section[decimal_domain_len+1]
    decimal_domain_type_len = int(domain_type_len, 16)
    sliced_type_array = question_section[decimal_domain_len+2:decimal_domain_len+decimal_domain_type_len+2]
    hex_domain_type_name = " ".join(sliced_type_array)
    domain_type_name = hex_to_char(hex_domain_type_name)
    
    full_domain_name = domain_name + "." + domain_type_name

    return full_domain_name

# Creates the response header, changing two values
def response_header_creator(arr, length):
    # Flag values
    QR = 1
    OPCODE = 0
    AA = 1
    TC = 0
    RD = 0
    RA = 0
    Z = "000"
    RCODE = 0

    # Combine flag values
    flags = f"{QR}{OPCODE:04b}{AA}{TC}{RD}{RA}{Z}{RCODE:04b}"
    # Convert the binary string
    hex_flags = format(int(flags, 2), '04x')

    arr[1] = hex_flags    
    arr[3] = format(length, '04x')
    head = " ".join(arr)

    return head

# Creates the response answer
def response_answer_creator(question_arr, domain_info_arr, ip_address):
    # Name - c00c
    rname = "c00c"
    # TYPE - query type (two octect)
    rtype = "".join(question_arr[-4:-2])
    # CLASS - Set QCLASS field as IN (00 01) (hex value) for the Internet.
    rclass = "".join(question_arr[-2:])
    # TTL
    ttl = format(domain_info_arr[3], '08x')
    # RDATA
    # ip_address = domain_info_arr[4]
    ip_hex = socket.inet_aton(ip_address).hex()
    # RDLENGTH
    rdlength = format(len(ip_hex)//2, '04x')
    # Combine
    combined_hex = rname + rtype + rclass + ttl + rdlength + ip_hex
    # print("Combined Question Hex Values:", combined_hex)
    combined_hex = hex_spacer(combined_hex)
    
    return combined_hex


# Define server address and port
server_ip = '127.0.0.1'
server_port = 10000

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address and port
server_socket.bind((server_ip, server_port))

# Predefined DNS records
dns_records = {
    "google.com": ["google.com", "A", "IN", 260, ["192.165.1.1", "192.165.1.10"]],
    "youtube.com": ["youtube.com", "A", "IN", 160, ["192.165.1.2"]],
    "uwaterloo.ca": ["uwaterloo.ca", "A", "IN", 160, ["192.165.1.3"]],
    "wikipedia.org": ["wikipedia.org", "A", "IN", 160, ["192.165.1.4"]],
    "amazon.ca": ["amazon.ca", "A", "IN", 160, ["192.165.1.5"]],
}

while True:
    print("Server is listening...")
    data, client_address = server_socket.recvfrom(1024)

    # Parse the received query
    query = data.decode()
    # query = data
    print(f"Request: \n{query}")
    
    qheader = query_header(query)
    qquestion = query_question(query)
    query_domain_name = recieved_domain_name(qquestion)

    if query_domain_name in dns_records:
        # print(dns_records[query_domain_name])
        response = " ".join(map(str, dns_records[query_domain_name]))
        response_header = response_header_creator(qheader, len(dns_records[query_domain_name][4]))
        response_answer = ""
        ip_address_array = dns_records[query_domain_name][4]
        
        # Deals with multiple ip_addresses
        for x in ip_address_array:
            response_answer += response_answer_creator(qquestion, dns_records[query_domain_name], x)
        
        # Response output
        response = response_header + space_remover(query)[24:] + response_answer
        response = space_remover(response)
        response = hex_spacer(response)
        print("Response: \n", response)
    else:
        response = "Not found"

    # Send the response to the client
    server_socket.sendto(response.encode(), client_address)
