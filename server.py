import socket
import hamming as ham

def main():
    sock = socket.socket()
    sock.bind(('', 12345))
    sock.listen(1)
    conn, addr = sock.accept()
    conn.settimeout(2.0)
    print('connected: ' + str(addr))
    message = ''
    countCorrect = 0
    countFail = 0
    lenWord = 81
    while True:
        try:
            data = conn.recv(lenWord + len([1,2,4,8,16,32,64]) + 1)
        except:
            break
        get_control_list = list(data)
        print(len(data))
        get_correct, one_error, more_error = ham.check_bits(get_control_list)      
        if one_error:
            print('One error was corrected')
            countCorrect += 1
        if more_error:
            print('More than one error')
            countFail += 1
        else:
            get_control_mess = ham.del_control_bits(get_correct)
            batch = ham.text_from_bits(ham.bin_list_to_str(get_control_mess))
            print(batch)
            message += batch
    report = 'Corrected errors: ' + str(countCorrect) + '\t Batches with more than one error: ' + str(countFail)
    conn.send(report.encode(encoding='utf-8'))
    conn.close()
    print(message)

    
if __name__ == "__main__":
    main()
