morse_code = {'A':'.-', 'B':'-...','C':'-.-.','D':'-..','E':'.',
              'F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
              'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.',
              'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-',
              'W':'.--' ,'X':'-..-','Y':'-.--','Z':'--..', ' ':' '}
def turnToMorse(string):
    string_morse = ''
    for i in range(len(string)):
        string_morse += (morse_code[string[i].upper()])
    return string_morse

def turnToString(string):
    string_normal = ""
    code = string.split(";")
    for i in range(len(code)):
        for key,value in morse_code.items():
            if code[i] == value:
                string_normal += key
    return string_normal