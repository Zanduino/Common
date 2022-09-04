import sys
import glob
import time
import os
import shutil
from distutils.dir_util import copy_tree
import subprocess
import collections

# optional wall option cause build failed if has warnings
BUILD_WALL = False
BUILD_WARN = True
if "--wall" in sys.argv:
    BUILD_WALL = True
    sys.argv.remove("--wall")

if "--no_warn" in sys.argv:
    BUILD_WARN = False
    sys.argv.remove("--no_warn")

# add user bin to path!
BUILD_DIR = ''
# add user bin to path!
try:
											  
				
									 
	
    # If we're on actions
    BUILD_DIR = os.environ["GITHUB_WORKSPACE"]
except KeyError:
    try:
        # If we're on travis
        BUILD_DIR = os.environ["TRAVIS_BUILD_DIR"]
    except KeyError:
        # If we're running on local machine
        BUILD_DIR = os.path.abspath(".")
        pass

os.environ["PATH"] += os.pathsep + BUILD_DIR + "/bin"
print("build dir:", BUILD_DIR)

IS_LEARNING_SYS = False
if "Adafruit_Learning_System_Guides" in BUILD_DIR:
    print("Found learning system repo")
    IS_LEARNING_SYS = True
    os.remove(BUILD_DIR + "/ci/examples/Blink/Blink.ino")
    os.rmdir(BUILD_DIR + "/ci/examples/Blink")
elif "METROX-Examples-and-Project-Sketches" in BUILD_DIR:
    print("Found MetroX Examples Repo")
    IS_LEARNING_SYS = True

#os.system('pwd')
#os.system('ls -lA')

CROSS = u'\N{cross mark}'
CHECK = u'\N{check mark}'

ALL_PLATFORMS={
    # classic Arduino AVR
    "uno" : ["arduino:avr:uno", None],
    "leonardo" : ["arduino:avr:leonardo", None],
    "mega2560" : ["arduino:avr:mega:cpu=atmega2560", None],
    # Arduino SAMD
    "zero" : ["arduino:samd:arduino_zero_native", "0x68ed2b88"],
    "cpx" : ["arduino:samd:adafruit_circuitplayground_m0", "0x68ed2b88"],
    # Espressif
    "esp8266" : ["esp8266:esp8266:huzzah:eesz=4M3M,xtal=80", None],
    "esp32" : ["esp32:esp32:featheresp32:FlashFreq=80", None],
    "magtag" : ["esp32:esp32:adafruit_magtag29_esp32s2", "0xbfdd4eee"],
    "funhouse" : ["esp32:esp32:adafruit_funhouse_esp32s2", "0xbfdd4eee"],
    "metroesp32s2" : ["esp32:esp32:adafruit_metro_esp32s2", "0xbfdd4eee"],
    # Adafruit AVR
    "trinket_3v" : ["adafruit:avr:trinket3", None],
    "trinket_5v" : ["adafruit:avr:trinket5", None],
    "protrinket_3v" : ["adafruit:avr:protrinket3", None],
    "protrinket_5v" : ["adafruit:avr:protrinket5", None],
    "gemma" : ["adafruit:avr:gemma", None],
    "flora" : ["adafruit:avr:flora8", None],
    "feather32u4" : ["adafruit:avr:feather32u4", None],
    "cpc" : ["arduino:avr:circuitplay32u4cat", None],
    # Adafruit SAMD
    "gemma_m0" : ["adafruit:samd:adafruit_gemma_m0", "0x68ed2b88"],
    "trinket_m0" : ["adafruit:samd:adafruit_trinket_m0", "0x68ed2b88"],
    "feather_m0_express" : ["adafruit:samd:adafruit_feather_m0_express", "0x68ed2b88"],
    "feather_m4_express" : ["adafruit:samd:adafruit_feather_m4:speed=120", "0x68ed2b88"],
    "feather_m4_express_tinyusb" : ["adafruit:samd:adafruit_feather_m4_express:speed=120,usbstack=tinyusb", "0x68ed2b88"],
    "feather_m4_can" : ["adafruit:samd:adafruit_feather_m4_can:speed=120", "0x68ed2b88"],
    "feather_m4_can_tinyusb" : ["adafruit:samd:adafruit_feather_m4_can:speed=120,usbstack=tinyusb", "0x68ed2b88"],
    "metro_m0" : ["adafruit:samd:adafruit_metro_m0", "0x68ed2b88"],
    "metro_m0_tinyusb" : ["adafruit:samd:adafruit_metro_m0:usbstack=tinyusb", "0x68ed2b88"],
    "metro_m4" : ["adafruit:samd:adafruit_metro_m4:speed=120", "0x55114460"],
    "metro_m4_tinyusb" : ["adafruit:samd:adafruit_metro_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "metro_m4_airliftlite" : ["adafruit:samd:adafruit_metro_m4_airliftlite:speed=120", "0x55114460"],
    "metro_m4_airliftlite_tinyusb" : ["adafruit:samd:adafruit_metro_m4_airliftlite:speed=120,usbstack=tinyusb", "0x55114460"],
    "pybadge" : ["adafruit:samd:adafruit_pybadge_m4:speed=120", "0x55114460"],
    "pybadge_tinyusb" : ["adafruit:samd:adafruit_pybadge_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "pygamer" : ["adafruit:samd:adafruit_pygamer_m4:speed=120", "0x55114460"],
    "pygamer_tinyusb" : ["adafruit:samd:adafruit_pygamer_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "hallowing_m0" : ["adafruit:samd:adafruit_hallowing", "0x68ed2b88"],
    "hallowing_m4" : ["adafruit:samd:adafruit_hallowing_m4:speed=120", "0x55114460"],
    "hallowing_m4_tinyusb" : ["adafruit:samd:adafruit_hallowing_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "neotrellis_m4" : ["adafruit:samd:adafruit_trellis_m4:speed=120", "0x55114460"],
    "monster_m4sk" : ["adafruit:samd:adafruit_monster_m4sk:speed=120", "0x55114460"],
    "monster_m4sk_tinyusb" : ["adafruit:samd:adafruit_monster_m4sk:speed=120,usbstack=tinyusb", "0x55114460"],
    "pyportal" : ["adafruit:samd:adafruit_pyportal_m4:speed=120", "0x55114460"],
    "pyportal_tinyusb" : ["adafruit:samd:adafruit_pyportal_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "pyportal_titano" : ["adafruit:samd:adafruit_pyportal_m4_titano:speed=120", "0x55114460"],
    "pyportal_titano_tinyusb" : ["adafruit:samd:adafruit_pyportal_m4_titano:speed=120,usbstack=tinyusb", "0x55114460"],
    "cpx_ada" : ["adafruit:samd:adafruit_circuitplayground_m0", "0x68ed2b88"],
    "grand_central" : ["adafruit:samd:adafruit_grandcentral_m4:speed=120", "0x55114460"],
    "grand_central_tinyusb" : ["adafruit:samd:adafruit_grandcentral_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "matrixportal" : ["adafruit:samd:adafruit_matrixportal_m4:speed=120", "0x55114460"],
    "matrixportal_tinyusb" : ["adafruit:samd:adafruit_matrixportal_m4:speed=120,usbstack=tinyusb", "0x55114460"],
    "neotrinkey_m0" : ["adafruit:samd:adafruit_neotrinkey_m0", "0x68ed2b88"],
    "rotarytrinkey_m0" : ["adafruit:samd:adafruit_rotarytrinkey_m0", "0x68ed2b88"],
    "neokeytrinkey_m0" : ["adafruit:samd:adafruit_neokeytrinkey_m0", "0x68ed2b88"],
    "slidetrinkey_m0" : ["adafruit:samd:adafruit_slidetrinkey_m0", "0x68ed2b88"],
    "proxlighttrinkey_m0" : ["adafruit:samd:adafruit_proxlighttrinkey_m0", "0x68ed2b88"],
    "qtpy_m0" : ["adafruit:samd:adafruit_qtpy_m0", "0x68ed2b88"],
    "qtpy_m0_tinyusb" : ["adafruit:samd:adafruit_qtpy_m0:usbstack=tinyusb", "0x68ed2b88"],
    # Arduino nRF
    "microbit" : ["sandeepmistry:nRF5:BBCmicrobit:softdevice=s110", None],
    # Adafruit nRF
    "nrf52832" : ["adafruit:nrf52:feather52832:softdevice=s132v6,debug=l0", None],
    "nrf52840" : ["adafruit:nrf52:feather52840:softdevice=s140v6,debug=l0", "0xada52840"],
    "cpb" : ["adafruit:nrf52:cplaynrf52840:softdevice=s140v6,debug=l0", "0xada52840"],
    "clue" : ["adafruit:nrf52:cluenrf52840:softdevice=s140v6,debug=l0", "0xada52840"],
    "ledglasses_nrf52840" : ["adafruit:nrf52:ledglasses_nrf52840:softdevice=s140v6,debug=l0", "0xada52840"],
    # RP2040 (Philhower)
    "pico_rp2040" : ["rp2040:rp2040:rpipico:freq=125,flash=2097152_0", "0xe48bff56"],
    "pico_rp2040_tinyusb" : ["rp2040:rp2040:rpipico:flash=2097152_0,freq=125,dbgport=Disabled,dbglvl=None,usbstack=tinyusb", "0xe48bff56"],
    "feather_rp2040" : ["rp2040:rp2040:adafruit_feather:freq=125,flash=8388608_0", "0xe48bff56"],
    "feather_rp2040_tinyusb" : ["rp2040:rp2040:adafruit_feather:flash=8388608_0,freq=125,dbgport=Disabled,dbglvl=None,usbstack=tinyusb", "0xe48bff56"],
    "qt2040_trinkey" : ["rp2040:rp2040:adafruit_trinkeyrp2040qt:freq=125,flash=8388608_0", "0xe48bff56"],
    "qt2040_trinkey_tinyusb" : ["rp2040:rp2040:adafruit_trinkeyrp2040qt:flash=8388608_0,freq=125,dbgport=Disabled,dbglvl=None,usbstack=tinyusb", "0xe48bff56"],
    # Attiny8xy, 16xy, 32xy (SpenceKonde)
    "attiny3217" : ["megaTinyCore:megaavr:atxy7:chip=3217", None],
    "attiny3216" : ["megaTinyCore:megaavr:atxy6:chip=3216", None],
    "attiny1617" : ["megaTinyCore:megaavr:atxy7:chip=1617", None],
    "attiny1616" : ["megaTinyCore:megaavr:atxy6:chip=1616", None],
    "attiny1607" : ["megaTinyCore:megaavr:atxy7:chip=1607", None],
    "attiny1606" : ["megaTinyCore:megaavr:atxy6:chip=1606", None],
    "attiny817" : ["megaTinyCore:megaavr:atxy7:chip=817", None],
    "attiny816" : ["megaTinyCore:megaavr:atxy6:chip=816", None],
    "attiny807" : ["megaTinyCore:megaavr:atxy7:chip=807", None],
    "attiny806" : ["megaTinyCore:megaavr:atxy6:chip=806", None],
    # groupings
    "main_platforms" : ("uno", "leonardo", "mega2560", "zero", "qtpy_m0",
                        "esp8266", "esp32", "metro_m4", "trinket_m0"),
    "arcada_platforms" : ("pybadge", "pygamer", "hallowing_m4",
                          "cpb", "cpx_ada"),
    "wippersnapper_platforms" : ("metro_m4_airliftlite_tinyusb", "pyportal_tinyusb"),
    "rp2040_platforms" : ("pico_rp2040", "feather_rp2040"),
    "zanshin_platforms" : ("uno", "leonardo", "mega2560", "zero", "cpx",
                          "esp8266", "esp32", "metro_m4",  "protrinket_5v",
                          "flora", "feather32u4", "metro_m0", "metro_m4")
}

BSP_URLS = "https://adafruit.github.io/arduino-board-index/package_adafruit_index.json,http://arduino.esp8266.com/stable/package_esp8266com_index.json,https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_dev_index.json,https://sandeepmistry.github.io/arduino-nRF5/package_nRF5_boards_index.json,https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json,http://drazzy.com/package_drazzy.com_index.json"

class ColorPrint:

    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stdout.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stdout.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)


def install_platform(platform):
    print("Installing", platform, end=" ")
    if platform == "adafruit:avr":   # we have a platform dep
        install_platform("arduino:avr")
    if os.system("arduino-cli core install "+platform+" --additional-urls "+BSP_URLS+" > /dev/null") != 0:
        ColorPrint.print_fail("FAILED to install "+platform)
        exit(-1)
    ColorPrint.print_pass(CHECK)
    # print installed core version
    print(os.popen('arduino-cli core list | grep {}'.format(platform)).read(), end='')

def run_or_die(cmd, error):
    print(cmd)
    attempt = 0
    while attempt < 3:
        if os.system(cmd) == 0:
            return
        attempt += 1
        print('attempt {} failed, {} retry left'.format(attempt, 3-attempt))
        time.sleep(5)
    ColorPrint.print_fail(error)
    exit(-1)

################################ Install Arduino IDE
print()
ColorPrint.print_info('#'*40)
print("INSTALLING ARDUINO BOARDS")
ColorPrint.print_info('#'*40)

run_or_die("arduino-cli core update-index --additional-urls "+BSP_URLS+
           " > /dev/null", "FAILED to update core indecies")
print()

														  
					   
		
																							
						   
			

################################ Install dependancies
our_name=None
try:
    if IS_LEARNING_SYS:
        libprop = open(BUILD_DIR+'/library.deps')
    else:
        libprop = open(BUILD_DIR+'/library.properties')
    for line in libprop:
        if line.startswith("name="):
            our_name = line.replace("name=", "").strip()
            if our_name.endswith("_Zanduino"):
                our_name = our_name[:-9]										  
        if line.startswith("depends="):
            deps = line.replace("depends=", "").split(",")
            for dep in deps:
                dep = dep.strip()
                print("Installing "+dep)
                run_or_die('arduino-cli lib install "'+dep+'" > /dev/null',
                           "FAILED to install dependancy "+dep)
except OSError:
    print("No library dep or properties found!")
    pass  # no library properties

# Delete the existing library if we somehow downloaded
# due to dependancies
if our_name:
    run_or_die("arduino-cli lib uninstall \""+our_name+"\"", "Could not uninstall")

print("Libraries installed: ", glob.glob(os.environ['HOME']+'/Arduino/libraries/*'))

# link our library folder to the arduino libraries folder
if not IS_LEARNING_SYS:
    try:
        os.symlink(BUILD_DIR, os.environ['HOME']+'/Arduino/libraries/' + os.path.basename(BUILD_DIR))
    except FileExistsError:
        pass

################################ UF2 Utils.

def glob1(pattern):
    result = glob.glob(pattern)
    if len(result) != 1:
        raise RuntimeError(f"Required pattern {pattern} to match exactly 1 file, got {result}")
    return result[0]

def download_uf2_utils():
    """Downloads uf2conv tools if we don't already have them
    """
    cmd = "wget -nc --no-check-certificate http://raw.githubusercontent.com/microsoft/uf2/master/utils/uf2families.json https://raw.githubusercontent.com/microsoft/uf2/master/utils/uf2conv.py"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    r = proc.wait(timeout=60)
    out = proc.stdout.read()
    err = proc.stderr.read()
    if r != 0:
        ColorPrint.print_fail("Failed to download UF2 Utils!")
        ColorPrint.print_fail(out.decode("utf-8"))
        ColorPrint.print_fail(err.decode("utf-8"))
        return False
    return True

def generate_uf2(example_path):
    """Generates a .uf2 file from a .bin or .hex file.
    :param str example_path: A path to the compiled .bin or .hex file.

    """
    if not download_uf2_utils():
        return None
    cli_build_path = "build/*.*." + fqbn.split(':')[2] + "/*.hex"
    input_file = glob1(os.path.join(example_path, cli_build_path))
    output_file = os.path.splitext(input_file)[0] + ".uf2"
    family_id = ALL_PLATFORMS[platform][1]
    cmd = ['python3', 'uf2conv.py', input_file, '-c', '-f', family_id, '-o', output_file]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = proc.wait(timeout=60)
    out = proc.stdout.read()
    err = proc.stderr.read()
    if r == 0 and not err:
        ColorPrint.print_pass(CHECK)
        ColorPrint.print_info(out.decode("utf-8"))
    else:
        ColorPrint.print_fail(CROSS)
        ColorPrint.print_fail(out.decode("utf-8"))
        ColorPrint.print_fail(err.decode("utf-8"))
        return None
    return output_file

################################ Test platforms
platforms = []
success = 0

# expand groups:
for arg in sys.argv[1:]:
    platform = ALL_PLATFORMS.get(arg, None)
    if isinstance(platform, list):
        platforms.append(arg)
    elif isinstance(platform, tuple):
        for p in platform:
            platforms.append(p)
    else:
        print("Unknown platform: ", arg)
        exit(-1)

def test_examples_in_folder(folderpath):
    global success
    for example in sorted(os.listdir(folderpath)):
        examplepath = folderpath+"/"+example
        if os.path.isdir(examplepath):
            test_examples_in_folder(examplepath)
            continue
        if not examplepath.endswith(".ino"):
            continue

        print('\t'+example, end=' ')
        # check if we should SKIP
        skipfilename = folderpath+"/."+platform+".test.skip"
        onlyfilename = folderpath+"/."+platform+".test.only"
        # check if we should GENERATE UF2
        gen_file_name = folderpath+"/."+platform+".generate"
        if os.path.exists(skipfilename):
            ColorPrint.print_warn("skipping")
            continue
        if glob.glob(folderpath+"/.*.test.only"):
            platformname = glob.glob(folderpath+"/.*.test.only")[0].split('.')[1]
            if platformname != "none" and not platformname in ALL_PLATFORMS:
                # uh oh, this isnt a valid testonly!
                ColorPrint.print_fail(CROSS)
                ColorPrint.print_fail("This example does not have a valid .platform.test.only file")
                success = 1
                continue
            if not os.path.exists(onlyfilename):
                ColorPrint.print_warn("skipping")
                continue
        if os.path.exists(gen_file_name):
            ColorPrint.print_info("generating")

        if BUILD_WARN:
            if os.path.exists(gen_file_name):
                cmd = ['arduino-cli', 'compile', '--warnings', 'all', '--fqbn', fqbn, '-e', folderpath]
            else:
                cmd = ['arduino-cli', 'compile', '--warnings', 'all', '--fqbn', fqbn, folderpath]
        else:
            ColorPrint.print_fail("Compiling with warnings")
            cmd = ['arduino-cli', 'compile', '--warnings', 'none', '--export-binaries', '--fqbn', fqbn, folderpath]
			
																					  
											 
					

																	 
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(timeout=60)
            r = proc.returncode
        except:
            proc.kill()
            out, err = proc.communicate()
            r = 1

        if r == 0 and not (err and BUILD_WALL == True):
            ColorPrint.print_pass(CHECK)
            if err:
                # also print out warning message
                ColorPrint.print_fail(err.decode("utf-8"))
            if os.path.exists(gen_file_name):
                if ALL_PLATFORMS[platform][1] == None:
                    ColorPrint.print_info("Platform does not support UF2 files, skipping...")
                else:
                    ColorPrint.print_info("Generating UF2...")
                    filename = generate_uf2(folderpath)
                    if filename is None:
                        success = 1  # failure
                    if IS_LEARNING_SYS:
                        fqbnpath, uf2file = filename.split("/")[-2:]
                        os.makedirs(BUILD_DIR+"/build", exist_ok=True)
                        os.makedirs(BUILD_DIR+"/build/"+fqbnpath, exist_ok=True)
                        shutil.copy(filename, BUILD_DIR+"/build/"+fqbnpath+"-"+uf2file)
                        os.system("ls -lR "+BUILD_DIR+"/build")
        else:
            ColorPrint.print_fail(CROSS)
            ColorPrint.print_fail(out.decode("utf-8"))
            ColorPrint.print_fail(err.decode("utf-8"))
            success = 1

def test_examples_in_learningrepo(folderpath):
    global success
    for project in os.listdir(folderpath):
        projectpath = folderpath+"/"+project
        if os.path.isdir(learningrepo):
            test_examples_in_learningrepo(projectpath)
            continue
        if not projectpath.endswith(".ino"):
            continue
	    # found an INO!
        print('\t'+projectpath, end=' ', flush=True)
        # check if we should SKIP
        skipfilename = folderpath+"/."+platform+".test.skip"
        onlyfilename = folderpath+"/."+platform+".test.only"
        if os.path.exists(skipfilename):
            ColorPrint.print_warn("skipping")
            continue
        elif glob.glob(folderpath+"/.*.test.only") and not os.path.exists(onlyfilename):
            ColorPrint.print_warn("skipping")
            continue

        cmd = ['arduino-cli', 'compile', '--warnings', 'all', '--fqbn', fqbn, projectpath]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        r = proc.wait()
        out = proc.stdout.read()
        err = proc.stderr.read()
        if r == 0:
            ColorPrint.print_pass(CHECK)
            if err:
                # also print out warning message
                ColorPrint.print_fail(err.decode("utf-8"))
        else:
            ColorPrint.print_fail(CROSS)
            ColorPrint.print_fail(out.decode("utf-8"))
            ColorPrint.print_fail(err.decode("utf-8"))
            success = 1


for platform in platforms:
    fqbn = ALL_PLATFORMS[platform][0]
    print('#'*80)
    ColorPrint.print_info("SWITCHING TO "+fqbn)
    install_platform(":".join(fqbn.split(':', 2)[0:2])) # take only first two elements
    print('#'*80)
    if not IS_LEARNING_SYS:
        test_examples_in_folder(BUILD_DIR+"/examples")
    else:
        test_examples_in_folder(BUILD_DIR)
exit(success)
