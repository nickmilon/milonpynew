'''
Created on Oct 21, 2010

@author: milon
'''
#!/usr/bin/env python
# -*- coding: utf-8  

def IPNumToQuad(n,pad=3):
    "convert long int to dotted quad string paded with pad 0s"
    d = 256 * 256 * 256
    q = []
    while d > 0:
        m,n = divmod(n,d)
        q.append(str(m).rjust(pad,'0'))
        d = d/256
    return '.'.join(q)
    
def IPQuadToNum(ip):
    "convert decimal dotted quad string to long integer works with any number of padded 0s"
    hexn = ''.join(["%02X" % long(i) for i in ip.split('.')])
    return long(hexn, 16)

def IPencode(ip_address): # around 10% faster than IPQuadToNum
    return reduce((lambda ip, part: (ip << 8) | int(part)), ip_address.split('.'), 0)

def IPdecode(addr):
    return '.'.join(map(lambda (bits, ip): str((ip >> bits) & 255), [(i*8, addr) for i in range(4)])[::-1])