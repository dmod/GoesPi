import time
import subprocess
from board import SCL, SDA, D4
import busio
import re
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305

oled_reset = digitalio.DigitalInOut(D4)

i2c = busio.I2C(SCL, SDA)

disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, reset=oled_reset)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = 'sudo journalctl -u startgoesrecv.service --quiet --lines 1'
    GoesOutput = subprocess.check_output(cmd, shell=True).decode("utf-8")

    result = re.search(r"vit\(avg\):[ ]+(\d+)", GoesOutput)
    vit = result.group(1)
    print(vit)

    cmd = '/usr/bin/vcgencmd measure_temp'
    TempOutput = subprocess.check_output(cmd, shell=True).decode("utf-8")

    print(TempOutput)

    draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
    draw.text((x, top + 8), CPU, font=font, fill=255)
    draw.text((x, top + 16), TempOutput, font=font, fill=255)
    draw.text((x, top + 25), vit, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)