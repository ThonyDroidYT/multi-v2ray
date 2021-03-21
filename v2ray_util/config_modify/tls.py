#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import os

from ..util_core.v2ray import restart, V2ray
from ..util_core.writer import GroupWriter
from ..util_core.group import Mtproto, SS
from ..util_core.selector import GroupSelector
from ..util_core.utils import get_ip, gen_cert, readchar, is_ipv4

class TLSModifier:
    def __init__(self, group_tag, group_index, domain='', alpn=None, xtls=False):
        self.domain = domain
        self.alpn = alpn
        self.xtls = xtls
        self.writer = GroupWriter(group_tag, group_index)
    
    @restart(True)
    def turn_on(self, need_restart=True):
        print("")
        print(_("1. Certificado Let's Encrypt (creación automática, por favor prepare el dominio)"))
        print(_("2. Certificado personalizado (prepare rutas de archivo de certificado)"))
        print("")
        choice = readchar(_("Por favor seleccione: 》"))
        input_domain = self.domain
        if choice == "1":
            if not input_domain:
                local_ip = get_ip()
                input_domain = input(_("Por favor ingrese su dominio vps: 》"))
                try:
                    if is_ipv4(local_ip):
                        socket.gethostbyname(input_domain)
                    else:
                        socket.getaddrinfo(input_domain, None, socket.AF_INET6)[0][4][0]
                except Exception:
                    print(_("error de verificación de dominio!!!"))
                    print("")
                    return

            print("")
            print(_("generando automáticamente el certificado SSL, espere ..."))
            V2ray.stop()
            gen_cert(input_domain)
            crt_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/fullchain.cer"
            key_file = "/root/.acme.sh/" + input_domain +"_ecc"+ "/"+ input_domain +".key"

            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain, alpn=self.alpn, xtls=self.xtls)

        elif choice == "2":
            crt_file = input(_("por favor ingrese la ruta del archivo del certificado cert: 》"))
            key_file = input(_("por favor ingrese la ruta del archivo del certificado key: 》"))
            if not os.path.exists(crt_file) or not os.path.exists(key_file):
                print(_("certificado cert o clave no existe!"))
                return
            if not input_domain:
                input_domain = input(_("Por favor ingrese el certificado, el dominio del archivo cert: 》"))
                if not input_domain:
                    print(_("el dominio es nulo!"))
                    return
            self.writer.write_tls(True, crt_file=crt_file, key_file=key_file, domain=input_domain, alpn=self.alpn, xtls=self.xtls)
        else:
            print(_("input error!"))
            return
        return need_restart

    @restart()
    def turn_off(self):
        self.writer.write_tls(False)
        return True

def modify():
    gs = GroupSelector(_('modify tls'))
    group = gs.group

    if group == None:
        pass
    else:
        if type(group.node_list[0]) == Mtproto or type(group.node_list[0]) == SS:
            print(_("MTProto/Shadowsocks el protocolo no es compatible con https!!!"))
            print("")
            return
        tm = TLSModifier(group.tag, group.index)
        tls_status = 'abierto' if group.tls == 'tls' else 'cerrado'
        print("{}: {}\n".format(_("Estado del grupo tls"), tls_status))
        print("")
        print(_("1.Abrir TLS"))
        print(_("2.Cerrar TLS"))
        choice = readchar(_("Por favor seleccione: 》"))
        if not choice:
            return
        if not choice in ("1", "2"):
            print(_("error de entrada, por favor ingrese nuevamente"))
            return

        if choice == '1':
            tm.turn_on()
        elif choice == '2':
            tm.turn_off()
