import socket
import random
import math
import heapq

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

# Converts a hex string to char
def hex_to_char(hex_string):
    hex_string = space_remover(hex_string)
    byte_array = bytearray.fromhex(hex_string)  
    ascii_string = byte_array.decode("ASCII")  
    return ascii_string
    # print(ascii_string) 

# Converts a string to hex
def convert_to_hex_ascii(input_string):
    parts = input_string.split('.')
    first_part_length = len(parts[0])
    second_part_length = len(parts[1])
    
    hex_first_part_length = format(first_part_length, '02x')
    hex_second_part_length = format(second_part_length, '02x')

    first_part = parts[0].replace('.', '')
    
    hex_first_part = first_part.encode('ascii').hex()
    hex_second_part = parts[1].encode('ascii').hex()
    
    result = f"{hex_first_part_length} {hex_first_part} {hex_second_part_length} {hex_second_part}"
    result = space_remover(result) + "00"
    return result

# Creates the initial header for the query
def query_header_creator():
    # ID - generate randomly 16 bit ID
    random_id = random.randint(0, 65535)
    hex_id = format(random_id, '04x')
    # print("Random 16-bit ID:", hex_id)

    # Flag values
    QR = 0
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
    # print("16-bit Hexadecimal Flag:", hex_flags)

    # QDCOUNT - 1
    hex_qdcount = format(1, '04x')
    # print("16-bit Hexadecimal QDCOUNT:", hex_qdcount)

    # ANCOUNT - an unsigned 16-bit integer specifying the number of resource records in the answer section
    # * Set ANCOUNT based on message type.
    hex_ancount = format(0, '04x')

    # NSCOUNT - 0
    hex_nscount = format(0, '04x')

    # ARCOUNT - 0
    hex_arcount = format(0, '04x')

    # Combine the lot
    combined_hex = hex_id + hex_flags + hex_qdcount + hex_ancount + hex_nscount + hex_arcount
    # print("Combined Header Hex Values:", combined_hex)
    return combined_hex

# Creates the initial question for the query
def query_question_creator(requested_domain_name):

    # QNAME - domain name to octet
    qname = convert_to_hex_ascii(requested_domain_name)
    # QTYPE - query type (two octect)
    qtype = "0001"
    # QCLASS - Set QCLASS field as IN (00 01) (hex value) for the Internet.
    qclass = "0001"
    # Combine
    combined_hex = qname + qtype + qclass
    # print("Combined Question Hex Values:", combined_hex)
    return combined_hex

# The final query sent to the server
def client_query(domain_req):
    dns_query_header = query_header_creator()
    dns_query_question = query_question_creator(domain_req)
    dns_query = dns_query_header + dns_query_question
    dns_query = hex_spacer(dns_query)
    return dns_query

# Used in 'response_parsing' for the case there are multiple IP addresses
def split_array_into_chunks(array, x):
    # Check if the array length is divisible by the chunk size
    if len(array) % x != 0:
        raise ValueError("Array length is not divisible by x")

    # Calculate the size of each subarray
    subarray_size = len(array) // x

    # Use list comprehension to split the array into X parts
    result = [array[i:i + subarray_size] for i in range(0, len(array), subarray_size)]

    return result

# Parses the response sent by the server and outputs an array with the details
def response_parsing(array):
    array = space_remover(array)
    header = array[:24]
    header_parted = [header[:4], header[4:8], header[8:12], header[12:16], header[16:20], header[20:24]]
    
    question = array[24:]
    question_parted = [question[i:i+2] for i in range(0, len(question), 2)]
    
    domain_len = question_parted[0]
    decimal_domain_len = int(domain_len, 16)
    sliced_array = question_parted[1:decimal_domain_len+1]
    hex_domain_name = " ".join(sliced_array)
    domain_name = hex_to_char(hex_domain_name)
    
    domain_type_len = question_parted[decimal_domain_len+1]
    decimal_domain_type_len = int(domain_type_len, 16)
    sliced_type_array = question_parted[decimal_domain_len+2:decimal_domain_len+decimal_domain_type_len+2]
    hex_domain_type_name = " ".join(sliced_type_array)
    domain_type_name = hex_to_char(hex_domain_type_name)
    
    full_domain_name = domain_name + "." + domain_type_name

    response_answer_array = question_parted[decimal_domain_len+decimal_domain_type_len+7:]

    number_of_ip_addresses = len(response_answer_array)//16
    server_response_list = []
        
    type = " ".join(question_parted[decimal_domain_len+decimal_domain_type_len+3:decimal_domain_len+decimal_domain_type_len+5])
    type = space_remover(type)
    qtype = ""

    if (type == "0001"):
        qtype = "A"
    elif (type == "0002"):
        qtype = "NS"
    elif (type == "0003"):
        qtype = "MD"
    elif (type == "0004"):
        qtype = "MF"
    
    ttl = response_answer_array[6:10]
    ttl = "".join(ttl)
    ttl = int(ttl, 16)
    
    result = split_array_into_chunks(response_answer_array, number_of_ip_addresses)

    server_response_list =[]
    for i in range(number_of_ip_addresses):
        ip_address = result[i][-4:]
        ip_address = "".join(ip_address)
        ip_address = socket.inet_ntoa(bytes.fromhex(ip_address))
        temp = full_domain_name + ": type " + qtype + ", class IN, TTL " + str(ttl) + ", addr (4) " + str(ip_address)
        server_response_list.append(temp)
    
    return server_response_list

# Server address and port
server_ip = '127.0.0.1'
server_port = 10000

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("\n")

while True:
    print("Input from the user: ")
    domain_name = input("Enter Domain Name: ")
    domain_name = domain_name.lower()
    if domain_name == "end":
        print("Session ended")
        break
    
    if "." in domain_name:
        client_req = client_query(domain_name)

        # Send the DNS query to the server
        client_socket.sendto(client_req.encode(), (server_ip, server_port))

        response, _ = client_socket.recvfrom(1024)
        response = response.decode()

        if (response == "Not found"):
            print("Not found")
        else :
            output_array = response_parsing(response)
            # Output
            print("Output:")
            for i in range(len(output_array)):
                print(output_array[i])
            print("\n")
    else:
        print("Not found \n")