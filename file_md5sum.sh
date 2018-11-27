#!/bin/bash
#
# 变量首先声明才能使用
shopt -s -o nounset
 
# 声明
 
# 建立日期
 
Date=$(date +'%Y%m%d%H%M%S')
 
# 加入审核的目录         #
 
Dirs="/"
 
# 临时文件               #
 
TMP_file=$(mktemp /tmp/check.XXXXXX)
	 
# 文件checksum存储文件
FP="$(pwd)/fp.$Date.chksum"
	 
# 使用哪种checksum工具
Checker="/usr/bin/md5sum"
Find="/usr/bin/find"
	 
# 函数区                #
	 
scan_file() {
	local f
	for f in $Dirs
		do
			$Find $f -type f >> $TMP_file
		done
	}
 
# 读取文件建立每个文件的checksum值
cr_checksum_list() {
	local f
	if [ -f $TMP_file ]; then
		for f in $(cat $TMP_file);
			do
               $Checker $f >> $FP
            done
    fi
}
rmTMP() {
    [ -f $TMP_file ] && rm -rf $TMP_file
}
 
 
# 主程序区
 
 
# 扫描列表
scan_file
 
# 建立文件的checksum值
cr_checksum_list
 
# 清理临时文件
rmTMP
