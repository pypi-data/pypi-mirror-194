# coding=utf-8
import os
import glob
import platform
import logging
# 本类只适用x64_Env/x64_Lib(Debug/Release/LinuxDebug/LinuxRelease)规则


def is_win():
    return ("Windows" in platform.platform())


def GetBaseDir():
    # 定位工程父目录:包含x64_Env的目录
    l = []
    b = os.path.abspath(os.getcwd())

    base_dir = os.path.join(b, "x64_Env")
    if os.path.isdir(base_dir):
        return os.path.join(base_dir, '..')
    l.append(base_dir)

    base_dir = os.path.join(b, "../x64_Env")
    if os.path.isdir(base_dir):
        return os.path.join(base_dir, '..')
    l.append(base_dir)

    base_dir = os.path.join(b, "../../x64_Env")
    if os.path.isdir(base_dir):
        return os.path.join(base_dir, '..')
    l.append(base_dir)

    base_dir = os.path.join(b, "../../../x64_Env")
    if os.path.isdir(base_dir):
        return os.path.join(base_dir, '..')
    l.append(base_dir)

    base_dir = os.path.join(b, "../../../src/x64_Env")
    if os.path.isdir(base_dir):
        return os.path.join(base_dir, '..')
    l.append(base_dir)

    str = '%s\n is not detected' % '\n'.join(l)
    raise Exception(str)
    return ''


def GetBinDir(BuildType):
    # BuildType=Release/Debug
    strDirPre = ""
    if not is_win():
        strDirPre = "Linux"
    baseDir = GetBaseDir()
    strDst = os.path.join(baseDir, "x64_Env",
                          strDirPre+str(BuildType))
    check_file = os.path.join(strDst, 'SvrBasic.ini')
    if (not os.path.isfile(check_file)):
        raise Exception('%s不存在' % check_file)
    return strDst


def GetToolDir(BuildType):
    # x64_Env/tool
    strDst = GetBinDir(BuildType)
    strDst = os.path.abspath(os.path.join(strDst, ".."))
    if not os.path.isdir(strDst):
        raise Exception('%s目录不存在' % strDst)
    strDirPre = ""
    if not is_win():
        strDirPre = "Linux"
    strDst = os.path.join(strDst, '%stool' % strDirPre)
    if not os.path.isdir(strDst):
        os.mkdir(strDst)
    return strDst


def GetLogDir(BuildType):
    # x64_Env/LinxDebug/SYSLOG
    strDst = GetBinDir(BuildType)
    strDst = os.path.join(strDst, "SYSLOG")
    return strDst


def GetLibDir(BuildType):
    # BuildType=Release/Debug
    strDirPre = ""
    if not is_win():
        strDirPre = "Linux"
    strDst = os.path.join(GetBaseDir(), "x64_Lib",
                          strDirPre+str(BuildType))
    return strDst


def ClearDll():
    # 清除所有dll和exe
    for build_type in ['Debug', 'Release']:
        dir = GetBinDir(build_type)
        lst = glob.glob(os.path.join(dir, '*.dll'))
        lst = lst + glob.glob(os.path.join(dir, '*.exe'))
        lst = lst + glob.glob(os.path.join(dir, '*.pdb'))
        lst = lst + glob.glob(os.path.join(dir, '*.so'))
        for f in lst:
            os.remove(f)


def ConvertSharedFileName(f, BuildType):
    # Entity.dll==>Entity-d.so
    name = os.path.splitext(f)[0]
    if BuildType == 'Debug':
        name += '-d'
    if is_win():
        name += '.dll'
    else:
        name += '.so'
    return name


def IsBinBuildSuc(BuildType):
    # BuildType=Release/Debug
    dir = GetBinDir(BuildType)
    if not os.path.exists(dir):
        logging.error("dir[%s] not exist" % dir)
        return False

    lstFile = ['Entity.dll', 'Net.dll']
    for f in lstFile:
        f = ConvertSharedFileName(f, BuildType)
        f = os.path.join(dir, f)
        if not os.path.exists(f):
            c = "file[%s] not exist" % f
            logging.error(c)
            raise Exception(c)
            return False
    return True
