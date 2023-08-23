#!/bin/bash

# 获取脚本当前目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 配置
INPUT_FOLDER="input_folder"
OUTPUT_FOLDER="output_folder"
RCLONE_DESTINATION="remote:folder"  # 替换为实际的 rclone 目标
URLS_PER_ITERATION=5  # 每次处理的链接数量

# 确保输出文件夹存在
mkdir -p "$OUTPUT_FOLDER"

while true; do
    # 检查 url.txt 是否为空
    if [ ! -s "url.txt" ]; then
        echo "没有需要处理的链接"
        break
    fi

    # 从 url.txt 中读取下一批链接，然后用空格连接
    mapfile -t urls < <(head -n "$URLS_PER_ITERATION" url.txt)
    url_list="${urls[*]}"

    # 输出正在处理的链接
    echo "$url_list"

    # 运行命令，并将输出保存到 run.log
    python main.py videos $url_list | tee "$OUTPUT_FOLDER/run.log"

    # 删除已处理的链接
    grep -vFf <(printf "%s\n" "${urls[@]}") url.txt > url_tmp.txt
    mv url_tmp.txt url.txt

    # 使用 ffmpeg 处理每个文件，然后删除原文件
    for input_file in "$INPUT_FOLDER"/*; do
        output_file="$OUTPUT_FOLDER/$(basename "$input_file" | cut -d. -f1).mp4"
        echo "正在处理文件：$input_file"
        ffmpeg -i "$input_file" -c copy "$output_file"
        rm "$input_file"
    done

    # 生成文件列表并保存到脚本当前目录
    current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")
    filelist_name="filelist-$current_datetime.txt"
    find "$OUTPUT_FOLDER" -type f > "$SCRIPT_DIR/$filelist_name"

    # 运行 rclone 命令，将结果上传
    rclone move -P "$OUTPUT_FOLDER" "$RCLONE_DESTINATION"
done

echo "Finished"
