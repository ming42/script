<?php
// 目标链接
$targetUrl = '目标链接';

// 创建 cURL 资源
$ch = curl_init($targetUrl);

// 设置 cURL 选项
curl_setopt_array($ch, [
    CURLOPT_USERAGENT      => $_SERVER['HTTP_USER_AGENT'],
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_RETURNTRANSFER => true,
]);

// 执行 cURL 请求并获取返回的数据
$response = curl_exec($ch);

// 检查是否有 cURL 错误
if (curl_errno($ch)) {
    echo 'cURL Error: ' . curl_error($ch);
    exit;
}

// 获取 cURL 请求的 HTTP 状态码
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

// 关闭 cURL 资源
curl_close($ch);

if ($httpCode === 200) {
    // 获取图片类型
    $contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);

    // 禁用输出缓冲
    ob_end_clean();

    // 设置响应头为图片类型
    header('Content-Type: ' . $contentType);

    // 禁止缓存
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Cache-Control: post-check=0, pre-check=0', false);
    header('Pragma: no-cache');

    // 输出获取的图片数据
    echo $response;
} else {
    echo 'Failed to fetch image.';
}
?>
