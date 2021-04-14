#!/usr/bin/env python3
barra="\033[1;34m=========================================================\033[0m"
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

from v2ray_util import run_type
from .util_core.v2ray import V2ray
from .util_core.utils import ColorStr, open_port, loop_input_choice_number
from .global_setting import stats_ctr, iptables_ctr, ban_bt, update_timer
from .config_modify import base, multiple, ss, stream, tls, cdn

def help():
    exec_name = sys.argv[0]
    from .util_core.config import Config
    lang = Config().get_data('lang')
    if lang == 'zh':
        print("""
{0} [-h|help] [options]
    -h, help             查看帮助
    -v, version          查看版本号
    start                启动 {bin}
    stop                 停止 {bin}
    restart              重启 {bin}
    status               查看 {bin} 运行状态
    new                  重建新的{bin} json配置文件
    update               更新 {bin} 到最新Release版本
    update [version]     更新 {bin} 到指定版本
    update.sh            更新 multi-v2ray 到最新版本
    add                  新增端口组
    add [protocol]       新增一种协议的组, 端口随机, 如 {bin} add utp 为新增utp协议
    del                  删除端口组
    info                 查看配置
    port                 修改端口
    tls                  修改tls
    tfo                  修改tcpFastOpen
    stream               修改传输协议
    cdn                  走cdn
    stats                {bin}流量统计
    iptables             iptables流量统计
    clean                清理日志
    log                  查看日志
    rm                   卸载{bin}
        """.format(exec_name[exec_name.rfind("/") + 1:], bin=run_type))
    else:
        print("""
{0} [-h|help] [options]
    v2ray -h, help                        Consiguir ayuda
    v2ray -v, version                   Obtener version
    v2ray start                             Iniciar {bin}
    v2ray stop                             Detener {bin}
    v2ray restart                         Reiniciar {bin}
    v2ray status                          Comprobar el estado de {bin}
    v2ray new                              Crear un nuevo perfil json
    v2ray update                         Actualizar {bin} a la última
    v2ray update [version]        Actualizar {bin} a una versión especial
    v2ray update.sh                    Actualizar multi-v2ray a la última versión
    v2ray add                               Agregar nuevo grupo
    v2ray add [protocol]            Crear un protocolo especial, nuevo puerto aleatorio
    v2ray del                                Eliminar grupo de puertos
    v2ray info                              Comprobar perfiles de {bin}
    v2ray port                              Modificar puerto
    v2ray tls                                 Modificar tls
    v2ray tfo                                Modificar tcpFastOpen
    v2ray stream                         Modificar protocolo
    v2ray cdn                               Modo cdn
    v2ray stats                             Estadísticas de tráfico de {bin}
    v2ray iptables                        Estadísticas de tráfico de iptables
    v2ray clean                             Limpiar el registro de {bin}
    v2ray log                                Comprobar el registro de {bin}
    v2ray rm                                 Desinstalar {bin}
        """.format(exec_name[exec_name.rfind("/") + 1:], bin=run_type))

def updateSh():
    if os.path.exists("/.dockerenv"):
        subprocess.Popen("pip install -U v2ray_util", shell=True).wait()
    else:
        #subprocess.Popen("curl -Ls https://multi.netlify.app/v2ray.sh -o temp.sh", shell=True).wait()
        subprocess.Popen("curl -Ls https://v2ray.admplus.tk/v2ray.sh -o temp.sh", shell=True).wait()
        subprocess.Popen("bash temp.sh -k && rm -f temp.sh", shell=True).wait()

def parse_arg():
    if len(sys.argv) == 1:
        return
    elif len(sys.argv) == 2:
        if sys.argv[1] == "start":
            V2ray.start()
        elif sys.argv[1] == "stop":
            V2ray.stop()
        elif sys.argv[1] == "restart":
            V2ray.restart()
        elif sys.argv[1] in ("-h", "help"):
            help()
        elif sys.argv[1] in ("-v", "version"):
            V2ray.version()
        elif sys.argv[1] == "status":
            V2ray.status()
        elif sys.argv[1] == "info":
            V2ray.info()
        elif sys.argv[1] == "port":
            base.port()
        elif sys.argv[1] == "tls":
            tls.modify()
        elif sys.argv[1] == "tfo":
            base.tfo()
        elif sys.argv[1] == "stream":
            stream.modify()
        elif sys.argv[1] == "stats":
            stats_ctr.manage()
        elif sys.argv[1] == "iptables":
            iptables_ctr.manage()
        elif sys.argv[1] == "clean":
            V2ray.cleanLog()
        elif sys.argv[1] == "del":
            multiple.del_port()
        elif sys.argv[1] == "add":
            multiple.new_port()
        elif sys.argv[1] == "update":
            V2ray.update()
        elif sys.argv[1] == "update.sh":
            updateSh()
        elif sys.argv[1] == "new":
            V2ray.new()
        elif sys.argv[1] == "log":
            V2ray.log()
        elif sys.argv[1] == "cdn":
            cdn.modify()
        elif sys.argv[1] == "rm":
            V2ray.remove()
    else:
        if sys.argv[1] == "add":
            multiple.new_port(sys.argv[2])
        elif sys.argv[1] == "update":
            V2ray.update(sys.argv[2])
        elif sys.argv[1] == "log":
            if sys.argv[2] in ("error", "e"):
                V2ray.log(True)
            elif sys.argv[2] in ("access", "a"):
                V2ray.log()
    sys.exit(0)

def service_manage():
    show_text = (_("Iniciar {}".format(run_type)), _("Detener {}".format(run_type)), _("Reiniciar {}".format(run_type)), _("{} estado".format(run_type)), _("{} registro".format(run_type)))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("Por favor seleccione: 》"), len(show_text))
    if choice == 1:
        V2ray.start()
    elif choice == 2:
        V2ray.stop()
    elif choice == 3:
        V2ray.restart()
    elif choice == 4:
        V2ray.status()
    elif choice == 5:
        V2ray.log()

def user_manage():
    show_text = (_("Agregar usuario"), _("Agregar puerto"), _("Elminar usuario"), _("Eliminar puerto"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("Por favor seleccione: 》"), len(show_text))
    if not choice:
        return
    elif choice == 1:
        multiple.new_user()
    elif choice == 2:
        multiple.new_port()
        open_port()
    elif choice == 3:
        multiple.del_user()
    elif choice == 4:
        multiple.del_port()

def profile_alter():
    show_text = (_("Modificar email"), _("Modificar UUID"), _("Modificar alterID"), _("Modificar puerto"), _("Modificar protocolo"), _("Modificar tls"), 
                _("modify tcpFastOpen"), _("Modificar dyn_port"), _("Modificar método shadowsocks"), _("Modificar contraseña shadowsocks"), _("Modo CDN (necesita dominio)"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("Por favor seleccione: 》"), len(show_text))
    if not choice:
        return
    elif choice == 1:
        base.new_email()
    elif choice == 2:
        base.new_uuid()
    elif choice == 3:
        base.alterid()
    elif choice == 4:
        base.port()
    elif choice == 5:
        stream.modify()
    elif choice == 6:
        tls.modify()
    elif choice == 7:
        base.tfo()
    elif choice == 8:
        base.dyn_port()
    elif choice == 9:
        ss.modify('method')
    elif choice == 10:
        ss.modify('password')
    elif choice == 11:
        cdn.modify()

def global_setting():
    show_text = (_("{} Estadísticas de tráfico".format(run_type.capitalize())), _("Estadísticas de tráfico de Iptables"), _("Prohibir Bittorrent"), _("Programar actualización {}".format(run_type.capitalize())), _("Limpiar registro de {} ".format(run_type.capitalize())), _("Cambiar idioma"))
    print("")
    for index, text in enumerate(show_text): 
        print("{}.{}".format(index + 1, text))
    choice = loop_input_choice_number(_("Por favor seleccione: 》"), len(show_text))
    if choice == 1:
        stats_ctr.manage()
    elif choice == 2:
        iptables_ctr.manage()
    elif choice == 3:
        ban_bt.manage()
    elif choice == 4:
        update_timer.manage()
    elif choice == 5:
        V2ray.cleanLog()
    elif choice == 6:
        from .util_core.config import Config
        config = Config()
        lang = config.get_data("lang")
        config.set_data("lang", "zh" if lang == "en" else "en")
        print(ColorStr.yellow(_("Por favor inicie de nuevo para ser efectivo!")))
        sys.exit(0)

def menu():
    V2ray.check()
    parse_arg()
    while True:
        print("")
        #barr
        print(barra)
        #print(ColorStr.cyan(_("Bienvenido a {} manager".format(run_type))))
        print(ColorStr.cyan(_("Bienvenido a {} manager [NEW-ADMPlus]".format(run_type))))
        print(barra)
        #fin barra
        print("")
        show_text = (_("1.Administrar {}".format(run_type.capitalize())), _("2.Gestionar grupo"), _("3.Modificar configuración"), _(" 4.Comprobar configuración"), _("5.Configuración global"), _(" 6.Actualizar {}".format(run_type.capitalize())), _("7.Generar cliente Json"))
        for index, text in enumerate(show_text): 
            if index % 2 == 0:
                print('{:<20}'.format(text), end="")   
            else:
                print(text)
                print("")
        print("")
        choice = loop_input_choice_number(_("Por favor seleccione: 》"), len(show_text))
        if choice == 1:
            service_manage()
        elif choice == 2:
            user_manage()
        elif choice == 3:
            profile_alter()
        elif choice == 4:
            V2ray.info()
        elif choice == 5:
            global_setting()
        elif choice == 6:
            V2ray.update()
        elif choice == 7:
            from .util_core import client
            client.generate()
        else:
            break

if __name__ == "__main__":
    menu()
