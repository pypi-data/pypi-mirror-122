# a strong encryption library

def encrypt(message):
    final_text = ''
    for i in message:
        if str(i) == 'a':
            final_text = final_text + '/-'
        elif str(i) == 'b':
            final_text = final_text + '|)'
        elif str(i) == 'c':
            final_text = final_text + '(,'
        elif str(i) == 'd':
            final_text = final_text + '|?'
        elif str(i) == 'e':
            final_text = final_text + '=-'
        elif str(i) == 'f':
            final_text = final_text + '+-'
        elif str(i) == 'g':
            final_text = final_text + '?,'
        elif str(i) == 'h':
            final_text = final_text + '|*'
        elif str(i) == 'i':
            final_text = final_text + '*^'
        elif str(i) == 'j':
            final_text = final_text + 'j^'
        elif str(i) == 'k':
            final_text = final_text + '|<'
        elif str(i) == 'l':
            final_text = final_text + '|,'
        elif str(i) == 'm':
            final_text = final_text + ':*'
        elif str(i) == 'n':
            final_text = final_text + 'HP'
        elif str(i) == 'o':
            final_text = final_text + '*,'
        elif str(i) == 'p':
            final_text = final_text + '-*'
        elif str(i) == 'q':
            final_text = final_text + '_*'
        elif str(i) == 'r':
            final_text = final_text + '|_'
        elif str(i) == 's':
            final_text = final_text + '<!'
        elif str(i) == 't':
            final_text = final_text + '+,'
        elif str(i) == 'u':
            final_text = final_text + '{@'
        elif str(i) == 'v':
            final_text = final_text + '#-'
        elif str(i) == 'w':
            final_text = final_text + '&='
        elif str(i) == 'x':
            final_text = final_text + '*('
        elif str(i) == 'y':
            final_text = final_text + '^&'
        elif str(i) == 'z':
            final_text = final_text + '*]'
        elif str(i) == ' ':
            final_text = final_text + '  '
        elif str(i) == 'A':
            final_text = final_text + '-/'
        elif str(i) == 'B':
            final_text = final_text + '(|'
        elif str(i) == 'C':
            final_text = final_text + '),'
        elif str(i) == 'D':
            final_text = final_text + '?|'
        elif str(i) == 'E':
            final_text = final_text + '-='
        elif str(i) == 'F':
            final_text = final_text + '-+'
        elif str(i) == 'G':
            final_text = final_text + ',?'
        elif str(i) == 'H':
            final_text = final_text + '*|'
        elif str(i) == 'I':
            final_text = final_text + '^*'
        elif str(i) == 'J':
            final_text = final_text + '^,'
        elif str(i) == 'K':
            final_text = final_text + '<|'
        elif str(i) == 'L':
            final_text = final_text + ',|'
        elif str(i) == 'M':
            final_text = final_text + '*:'
        elif str(i) == 'N':
            final_text = final_text + 'hp'
        elif str(i) == 'O':
            final_text = final_text + ',*'
        elif str(i) == 'P':
            final_text = final_text + '*-'
        elif str(i) == 'Q':
            final_text = final_text + '*_'
        elif str(i) == 'R':
            final_text = final_text + '_|'
        elif str(i) == 'S':
            final_text = final_text + '!<'
        elif str(i) == 'T':
            final_text = final_text + ',+'
        elif str(i) == 'U':
            final_text = final_text + '@}'
        elif str(i) == 'V':
            final_text = final_text + '-#'
        elif str(i) == 'W':
            final_text = final_text + '=&'
        elif str(i) == 'X':
            final_text = final_text + '(*'
        elif str(i) == 'Y':
            final_text = final_text + '&^'
        elif str(i) == 'Z':
            final_text = final_text + '[*'
        elif str(i) == '0':
            final_text = final_text + 'or'
        elif str(i) == '1':
            final_text = final_text + 'en'
        elif str(i) == '2':
            final_text = final_text + 'ow'
        elif str(i) == '3':
            final_text = final_text + 'ee'
        elif str(i) == '4':
            final_text = final_text + 'ru'
        elif str(i) == '5':
            final_text = final_text + 'ev'
        elif str(i) == '6':
            final_text = final_text + 'xi'
        elif str(i) == '7':
            final_text = final_text + 'ne'
        elif str(i) == '8':
            final_text = final_text + 'th'
        elif str(i) == '9':
            final_text = final_text + 'in'
        else:
            final_text = final_text + str(i*2)
    return final_text


def decrypt(encrypted_message):
    val = [(encrypted_message[i:i+2]) for i in range(0, len(encrypted_message), 2)]
    decrypted_message = ''
    for i in val:
        if i == 'in':
            decrypted_message = decrypted_message + '9'
        elif i == 'th':
            decrypted_message = decrypted_message + '8'
        elif i == 'ne':
            decrypted_message = decrypted_message + '7'
        elif i == 'xi':
            decrypted_message = decrypted_message + '6'
        elif i == 'ev':
            decrypted_message = decrypted_message + '5'
        elif i == 'ru':
            decrypted_message = decrypted_message + '4'
        elif i == 'ee':
            decrypted_message = decrypted_message + '3'
        elif i == 'ow':
            decrypted_message = decrypted_message + '2'
        elif i == 'en':
            decrypted_message = decrypted_message + '1'
        elif i == 'or':
            decrypted_message = decrypted_message + '0'
        elif i == '/-':
            decrypted_message = decrypted_message + 'a'
        elif i == '|)':
            decrypted_message = decrypted_message + 'b'
        elif i == '(,':
            decrypted_message = decrypted_message + 'c'
        elif i == '|?':
            decrypted_message = decrypted_message + 'd'
        elif i == '=-':
            decrypted_message = decrypted_message + 'e'
        elif i == '+-':
            decrypted_message = decrypted_message + 'f'
        elif i == '?,':
            decrypted_message = decrypted_message + 'g'
        elif i == '|*':
            decrypted_message = decrypted_message + 'h'
        elif i == '*^':
            decrypted_message = decrypted_message + 'i'
        elif i == 'j^':
            decrypted_message = decrypted_message + 'j'
        elif i == '|<':
            decrypted_message = decrypted_message + 'k'
        elif i == '|,':
            decrypted_message = decrypted_message + 'l'
        elif i == ':*':
            decrypted_message = decrypted_message + 'm'
        elif i == 'HP':
            decrypted_message = decrypted_message + 'n'
        elif i == '*,':
            decrypted_message = decrypted_message + 'o'
        elif i == '-*':
            decrypted_message = decrypted_message + 'p'
        elif i == '_*':
            decrypted_message = decrypted_message + 'q'
        elif i == '|_':
            decrypted_message = decrypted_message + 'r'
        elif i == '<!':
            decrypted_message = decrypted_message + 's'
        elif i == '+,':
            decrypted_message = decrypted_message + 't'
        elif i == '{@':
            decrypted_message = decrypted_message + 'u'
        elif i == '#-':
            decrypted_message = decrypted_message + 'v'
        elif i == '&=':
            decrypted_message = decrypted_message + 'w'
        elif i == '*(':
            decrypted_message = decrypted_message + 'x'
        elif i == '^&':
            decrypted_message = decrypted_message + 'y'
        elif i == '*]':
            decrypted_message = decrypted_message + 'z'
        elif i == '  ':
            decrypted_message = decrypted_message + ' '
        elif i == '-/':
            decrypted_message = decrypted_message + 'A'
        elif i == '(|':
            decrypted_message = decrypted_message + 'B'
        elif i == '),':
            decrypted_message = decrypted_message + 'C'
        elif i == '?|':
            decrypted_message = decrypted_message + 'D'
        elif i == '-=':
            decrypted_message = decrypted_message + 'E'
        elif i == '-+':
            decrypted_message = decrypted_message + 'F'
        elif i == ',?':
            decrypted_message = decrypted_message + 'G'
        elif i == '*|':
            decrypted_message = decrypted_message + 'H'
        elif i == '^*':
            decrypted_message = decrypted_message + 'I'
        elif i == '^,':
            decrypted_message = decrypted_message + 'J'
        elif i == '<|':
            decrypted_message = decrypted_message + 'K'
        elif i == ',|':
            decrypted_message = decrypted_message + 'L'
        elif i == '*:':
            decrypted_message = decrypted_message + 'M'
        elif i == 'hp':
            decrypted_message = decrypted_message + 'N'
        elif i == ',*':
            decrypted_message = decrypted_message + 'O'
        elif i == '*-':
            decrypted_message = decrypted_message + 'P'
        elif i == '*_':
            decrypted_message = decrypted_message + 'Q'
        elif i == '_|':
            decrypted_message = decrypted_message + 'R'
        elif i == '!<':
            decrypted_message = decrypted_message + 'S'
        elif i == ',+':
            decrypted_message = decrypted_message + 'T'
        elif i == '@}':
            decrypted_message = decrypted_message + 'U'
        elif i == '-#':
            decrypted_message = decrypted_message + 'V'
        elif i == '=&':
            decrypted_message = decrypted_message + 'W'
        elif i == '(*':
            decrypted_message = decrypted_message + 'X'
        elif i == '&^':
            decrypted_message = decrypted_message + 'Y'
        elif i == '[*':
            decrypted_message = decrypted_message + 'Z'
        else:
            decrypted_message = decrypted_message + str(i)[0]
    return decrypted_message

# end of program
