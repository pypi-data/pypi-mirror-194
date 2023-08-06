# -*- coding: utf-8 -*-

'''
Date: 2022-05-18
Description: 
LastEditTime: 2023-03-01
'''
# coding=utf-8
import os
from xDev import xFrame
from conans import ConanFile, tools, CMake
from conans.errors import ConanException

# 本类只适用x64_Env/x64_Lib(Debug/Release/LinuxDebug/LinuxRelease)规则


# def conan_export_pkg(ver):
#     lst = ['Utility/DB', 'Utility/Net', 'Framework']
#     for prj in lst:
#         os.system(
#             "conan export-pkg %s %s@hgame/release -s os=Windows -s build_type=Release -f" % (prj, ver))
#         os.system(
#             "conan export-pkg %s %s@hgame/release -s os=Windows -s build_type=Debug -f" % (prj, ver))
#     print("等待上传")
#     print("conan upload */%s@hgame/release --confirm --no-overwrite  --all" % ver)
# conan install Pkg/Common -s os=Linux -s compiler=clang -s compiler.version=15 --build=missing


class xConan(ConanFile):
    # 本类只适用x64_Env/x64_Lib(Debug/Release/LinuxDebug/LinuxRelease)规则
    generators = "cmake_multi"
    settings = "os", "compiler", "build_type", "arch"
    # libs #继承类必须定义libs
    url = 'x'
    license = 'x'
    description = 'x'

    def _get_libs(self):
        libs = self.libs
        if (str(self.settings.build_type) == "Debug"):
            for i in range(len(libs)):
                if self.settings.os == "Windows":
                    libs[i] = libs[i]+'-d'
                else:
                    libs[i] = 'lib' + libs[i]+'-d'
        else:
            for i in range(len(libs)):
                if self.settings.os != "Windows":
                    libs[i] = 'lib' + libs[i]
        return libs

    def _get_base_dir(self):
        # 定位工程父目录:包含x64_Env的目录
        base_dir = os.path.abspath(os.getcwd())
        if os.path.isdir(os.path.join(base_dir, 'x64_Env')):
            return base_dir
        base_dir = os.path.abspath(os.path.join(base_dir, ".."))
        if os.path.isdir(os.path.join(base_dir, 'x64_Env')):
            return base_dir
        base_dir = os.path.abspath(os.path.join(base_dir, ".."))
        if os.path.isdir(os.path.join(base_dir, 'x64_Env')):
            return base_dir
        self.output.info(base_dir)
        raise ConanException('找不到x64_Env目录')
        return ''

    def build(self):
        # 会失败
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        strDstBin = xFrame.GetBinDir(self.settings.build_type)
        strDstLib = xFrame.GetLibDir(self.settings.build_type)
        self.copy("*.h", dst="include", src="include")
        self.copy("*.inl", dst="include", src="include")
        self.copy("*.hpp", dst="include", src="include")

        libs = self._get_libs()

        for _, lib in enumerate(libs):
            self.copy(lib+".lib",
                      dst="lib", src=strDstLib, keep_path=False)
            self.copy(lib+".dll",
                      dst="bin", src=strDstBin, keep_path=False)
            self.copy(lib+".exe",
                      dst="bin", src=strDstBin, keep_path=False)
            self.copy(lib+".so", dst="lib",
                      src=strDstBin, keep_path=False)
            self.copy(lib+".pdb", dst="bin",
                      src=strDstBin, keep_path=False)
            self.copy(lib+".a", dst="lib",
                      src=strDstLib,  keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
