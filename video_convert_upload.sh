basePath='download/' #没有考虑子文件夹, 默认文件夹下都是视频
convPath='conv/'
list=`ls -m $basePath` #以逗号作为分隔符
addname=$(date +%Y%m%d%H%M)
IFS=","
isStart=1
for item in ${list[@]}
do
    if [[ isStart -eq 1 ]];then
        it=$item
        isStart=0
    else
        it=${item:1} # ls -m 出来的文件名有个\t, 需要移除首字符
    fi
    echo "${basePath}${it}" "${it%.*}.mp4"
    ffmpeg -i "${basePath}${it}" -c:v copy -c:a copy "${convPath}${it%.*}.mp4"
    rm -rf ${basePath}${it}
done
ls $convPath > filelist-${addname}.txt
cd conv
rclone move -P . XX:
cd ../
