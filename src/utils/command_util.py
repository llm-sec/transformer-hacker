import platform

mac_open_calc = 'open /System/Applications/Calculator.app'

windows_open_calc = 'calc'


def get_open_calc_command() -> str:
    """
    根据不同的操作系统获取对应的打开计算器的命令，仅用于无危害的证明此漏洞的存在
    :return:
    """
    os_name = platform.system()
    if os_name == "Windows":
        return windows_open_calc
    elif os_name == "Darwin":
        return mac_open_calc
    elif os_name in ["Linux", "FreeBSD", "OpenBSD"]:
        return "touch ~/hacked-by-cc11001100.txt"
    else:
        return "Other OS"
