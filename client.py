import sys, socket, random
import hamming as ham

def main(argv):
    server = argv[1]
    to_do_err = int(argv[2])
    one_err = False
    more_err = False
    if to_do_err > 0:
        one_err = True
    if to_do_err > 1:
        more_err = True
    lenWord = 81
    sock = socket.socket()
    sock.connect((server, 12345))

    f = open("text.txt", "r")
    mess = f.read()

    countCorrect = 0
    countFail = 0
    batch = ''
    for i, m in enumerate(mess):
        b = ham.text_to_bits(m)
        if len(batch) + len(b) > lenWord:
            for _ in range(lenWord - len(batch)):
                batch = '0' + batch
            bin_mess = ham.str_to_bin_list(batch)
            control_mess = ham.add_ctrl_bits(bin_mess)
            if one_err:
                if bool(round(random.random())):
                    index = round(random.random() * (lenWord-1))
                    control_mess[index] = int(not control_mess[index])
                    countCorrect += 1
                    if more_err:
                        if bool(round(random.random())):
                            index = round(random.random() * (lenWord-1))
                            control_mess[index] = int(not control_mess[index])
                            countCorrect -= 1
                            countFail += 1
                
            sock.send(bytes(control_mess))
            batch = b
        else:
            batch += b
            
    if batch != '':
        for _ in range(lenWord - len(batch)):
            batch = '0' + batch
        bin_mess = ham.str_to_bin_list(batch)
        control_mess = ham.add_ctrl_bits(bin_mess)
        sock.send(bytes(control_mess))

    report = 'Corrected errors: ' + str(countCorrect) + '\t Batches with more than one error: ' + str(countFail)
    response = sock.recv(1024)
    print(report)
    print(response.decode())
    sock.close()


if __name__ == "__main__":
    main(sys.argv)
