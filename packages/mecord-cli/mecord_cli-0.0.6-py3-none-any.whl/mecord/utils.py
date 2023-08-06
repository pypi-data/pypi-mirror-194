import uuid
import platform
import subprocess
import qrcode
import qrcode_terminal
import os
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask, SolidFillColorMask

def get_mac_address():
    if platform.system() == 'Windows':
        cmd = "ipconfig /all"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('gbk')
        pos = output_str.find('Physical Address')
        if pos == -1:
            pos = output_str.find('物理地址')
        mac = (output_str[pos:pos+100].split(':')[1]).strip().replace('-', '')
    elif platform.system() == 'Linux':
        cmd = "ifconfig"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('utf-8')
        mac = output_str[output_str.index('ether') + 6:output_str.index('ether') + 23].replace(':', '')
    else:
        mac = None
    return mac

def get_cpu_serial():
    cpu_serial = ""
    if platform.system() == 'Windows':
        cmd = "wmic cpu get ProcessorId"
        output = subprocess.check_output(cmd, shell=True)
        output_str = output.decode('gbk')
        pos = output_str.index("\n")
        cpu_serial = output_str[pos:].strip()
    elif platform.system() == 'Linux':
        with open('/proc/cpuinfo') as f:
            
            for line in f:
                print(line)
                print ("----------- \n")
                if line[0:6] == 'Serial':
                    return "1"
                if line.strip().startswith('serial'):
                    cpu_serial = line.split(":")[1].strip()
                    break
        if not cpu_serial:
            cpu_serial = None
    else:
        cpu_serial = None
    return cpu_serial

def generate_unique_id():
    mac = get_mac_address()
    cpu_serial = get_cpu_serial()
    if platform.system() == 'Windows':
        if mac and cpu_serial:
            unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac + cpu_serial)
            return str(unique_id).replace('-', '')
    
    elif platform.system() == 'Linux':
        if mac :
            unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac)
            return str(unique_id).replace('-', '')
    else:
        if mac :
            unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, mac)
            return str(unique_id).replace('-', '')

def displayQrcode(s):
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
        )
    qr.add_data(s)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage, 
        module_drawer=CircleModuleDrawer(),
        color_mask=SolidFillColorMask(),
        fill_color=(0, 0, 0),
        back_color=(255,255,255))
    
    cache_qrcode_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_qrcode.png")
    img.save(cache_qrcode_file)
    os.system(f"start " + cache_qrcode_file + " &")

def displayQRcodeOnTerminal(s):
    qrcode_terminal.draw(s)
