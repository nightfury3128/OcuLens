import pystray
import subprocess
import threading
import webbrowser
import socket
import time
import os
import sys
from PIL import Image, ImageDraw
from contextlib import closing

class iPhoneWebcamTray:
    def __init__(self):
        self.server_process = None
        self.server_port = None
        self.server_url = None
        self.icon = None
        
    def get_local_ip(self):
        """Get the local IP address"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    def read_server_port(self):
        """Read the server port from file"""
        try:
            # Look for server_port.txt in the project root
            port_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'server_port.txt')
            if os.path.exists(port_file):
                with open(port_file, 'r') as f:
                    port = int(f.read().strip())
                    self.server_port = port
                    local_ip = self.get_local_ip()
                    self.server_url = f"https://{local_ip}:{port}"
                    return True
        except Exception as e:
            print(f"Error reading server port: {e}")
        return False
    
    def create_icon_image(self):
        """Create a simple camera icon"""
        # Create a 64x64 image with a camera icon
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw camera body (rectangle)
        draw.rectangle([10, 20, 54, 44], fill='black', outline='black')
        
        # Draw lens (circle)
        draw.ellipse([25, 25, 39, 39], fill='gray', outline='black')
        draw.ellipse([28, 28, 36, 36], fill='black')
        
        # Draw flash
        draw.rectangle([45, 15, 50, 20], fill='yellow', outline='black')
        
        return image
    
    def start_server(self):
        """Start the iPhone webcam server"""
        try:
            if self.server_process and self.server_process.poll() is None:
                print("Server is already running")
                return
            
            print("Starting iPhone webcam server...")
            main_script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src', 'core', 'main.py')
            self.server_process = subprocess.Popen([sys.executable, main_script], 
                                                 cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                                 creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            # Wait a moment for the server to start and write the port file
            time.sleep(3)
            self.read_server_port()
            
            if self.server_url:
                self.icon.notify(f"Server started!\nAccess at: {self.server_url}", "iPhone Webcam")
            
        except Exception as e:
            self.icon.notify(f"Failed to start server: {e}", "Error")
    
    def stop_server(self):
        """Stop the iPhone webcam server"""
        try:
            if self.server_process and self.server_process.poll() is None:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("Server stopped")
                self.icon.notify("Server stopped", "iPhone Webcam")
            else:
                print("Server is not running")
        except Exception as e:
            print(f"Error stopping server: {e}")
            self.icon.notify(f"Error stopping server: {e}", "Error")
    
    def open_browser(self):
        """Open the webcam interface in browser"""
        if not self.server_url:
            self.read_server_port()
        
        if self.server_url:
            try:
                webbrowser.open(f"https://localhost:{self.server_port}")
                self.icon.notify("Browser opened", "iPhone Webcam")
            except Exception as e:
                self.icon.notify(f"Failed to open browser: {e}", "Error")
        else:
            self.icon.notify("Server not running", "iPhone Webcam")
    
    def copy_url_to_clipboard(self):
        """Copy the server URL to clipboard"""
        if not self.server_url:
            self.read_server_port()
        
        if self.server_url:
            try:
                import pyperclip
                pyperclip.copy(self.server_url)
                self.icon.notify(f"URL copied to clipboard:\n{self.server_url}", "iPhone Webcam")
            except ImportError:
                # Fallback for Windows
                try:
                    import subprocess
                    subprocess.run(['clip'], input=self.server_url.encode(), check=True)
                    self.icon.notify(f"URL copied to clipboard:\n{self.server_url}", "iPhone Webcam")
                except Exception as e:
                    self.icon.notify(f"Failed to copy URL: {e}", "Error")
            except Exception as e:
                self.icon.notify(f"Failed to copy URL: {e}", "Error")
        else:
            self.icon.notify("Server not running", "iPhone Webcam")
    
    def show_qr_code(self):
        """Show QR code for mobile access"""
        if not self.server_port:
            self.read_server_port()
        
        if self.server_port:
            qr_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), f"qr_code_port_{self.server_port}.png")
            if os.path.exists(qr_file):
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(qr_file)
                    else:  # macOS/Linux
                        subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', qr_file])
                    self.icon.notify("QR code opened", "iPhone Webcam")
                except Exception as e:
                    self.icon.notify(f"Failed to open QR code: {e}", "Error")
            else:
                self.icon.notify("QR code not found. Start server first.", "iPhone Webcam")
        else:
            self.icon.notify("Server not running", "iPhone Webcam")
    
    def show_status(self):
        """Show current server status"""
        if self.server_process and self.server_process.poll() is None:
            if not self.server_url:
                self.read_server_port()
            status = f"Server: Running\nPort: {self.server_port}\nURL: {self.server_url}"
        else:
            status = "Server: Stopped"
        
        self.icon.notify(status, "iPhone Webcam Status")
    
    def quit_app(self):
        """Quit the tray application"""
        self.stop_server()
        self.icon.stop()
    
    def setup_tray_menu(self):
        """Setup the tray menu"""
        menu = pystray.Menu(
            pystray.MenuItem("🚀 Start Server", self.start_server),
            pystray.MenuItem("🛑 Stop Server", self.stop_server),
            pystray.MenuItem("🌐 Open Browser", self.open_browser),
            pystray.MenuItem("📋 Copy URL", self.copy_url_to_clipboard),
            pystray.MenuItem("📱 Show QR Code", self.show_qr_code),
            pystray.MenuItem("ℹ️ Status", self.show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("❌ Quit", self.quit_app)
        )
        return menu
    
    def run(self):
        """Run the tray application"""
        icon_image = self.create_icon_image()
        menu = self.setup_tray_menu()
        
        self.icon = pystray.Icon("iPhone Webcam", icon_image, "iPhone Webcam Server", menu)
        
        print("iPhone Webcam Tray started. Right-click the system tray icon for options.")
        self.icon.run()

if __name__ == "__main__":
    app = iPhoneWebcamTray()
    app.run()