<div align="center">

# 🚀 ROS 2 for Control: DC Motor System
### Instrumentation, Parametric Identification, and Closed-Loop Control Platform with ESP32 (micro-ROS)

[![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble_Hawksbill-22314E?logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Ubuntu 22.04](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/22.04/)
[![ESP32 PlatformIO](https://img.shields.io/badge/ESP32-PlatformIO-orange?logo=espressif&logoColor=white)](https://platformio.org/)
[![micro-ROS Serial](https://img.shields.io/badge/micro--ROS-Serial_115200-green)](https://micro.ros.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

<p align="center">
Comprehensive repository of <b>ROS 2 (Humble)</b> and <b>ESP32 firmware (micro-ROS)</b> focused on the <b>design, instrumentation, experimental parametric identification, and closed-loop speed control</b> of a DC motor plant through automated step response tests.
</p>

</div>

---

## 📑 Table of Contents

1. [🗺️ Methodological Roadmap by Stages](#️-methodological-roadmap-by-stages)
2. [📥 Step 1: Download and Build the ROS 2 Workspace on PC](#-step-1-download-and-build-the-ros-2-workspace-on-pc)
3. [🔌 Step 2: Hardware and Firmware Setup on ESP32](#-step-2-hardware-and-firmware-setup-on-esp32)
4. [🤖 Step 3: Serial Connection with micro-ROS Agent](#-step-3-serial-connection-with-micro-ros-agent)
5. [🚀 Step 4: Experimental Execution by Stages](#-step-4-experimental-execution-by-stages)
6. [⏱️ Step Response Temporal Profile (Stage 02)](#️-step-response-temporal-profile-stage-02)
7. [⚙️ Software Architecture, Nodes, and Topics](#️-software-architecture-nodes-and-topics)
8. [📊 Data Format (CSV) and Mathematical Modeling (FOP / FOPDT)](#-data-format-csv-and-mathematical-modeling-fop--fopdt)
9. [📁 Repository Structure](#-repository-structure)
10. [🔧 Troubleshooting](#-troubleshooting)
11. [👥 Authors and License](#-authors-and-license)

---

## 🗺️ Methodological Roadmap by Stages

The project is organized following an incremental and modular control engineering methodology:

| Stage | Status | Title | Key Question | Deliverables / Files |
| :---: | :---: | :--- | :--- | :--- |
| **00** | <img src="https://img.shields.io/badge/Completed-brightgreen?style=flat-square" alt="Completed"> | **System Design** | *How to structure the distributed system?* | [Guide 0](docs/guides/Inteligente_guia0.md), architecture, and topic contract. |
| **01** | <img src="https://img.shields.io/badge/Completed-brightgreen?style=flat-square" alt="Completed"> | **Motor Instrumentation** | *Can I actuate and measure reliably?* | [Guide 1](docs/guides/Inteligente_guia1.md), encoder calibration ($N_{rev}=960$), bringup Stage 01. |
| **02** | <img src="https://img.shields.io/badge/In_Progress-orange?style=flat-square" alt="In Progress"> | **System Identification** | *What model describes the motor dynamics?* | [Guide 2](docs/guides/Inteligente_guia2.md), reaction curves ($30\\%, 45\\%, 60\\%$), FOP and FOPDT models. |
| **03** | <img src="https://img.shields.io/badge/Pending-lightgrey?style=flat-square" alt="Pending"> | **Model Validation** | *Does the model predict unseen data?* | RMSE/MAE metrics, percentage FIT, and nominal model selection. |
| **04** | <img src="https://img.shields.io/badge/Pending-lightgrey?style=flat-square" alt="Pending"> | **Controller Design** | *What controller fulfills the requirements?* | PI/PID/Intelligent design and dynamic simulation. |
| **05** | <img src="https://img.shields.io/badge/Pending-lightgrey?style=flat-square" alt="Pending"> | **Closed-Loop Control** | *Does the physical closed-loop system track references?* | Real-time experimental validation and disturbance rejection. |

---

## 📥 Step 1: Download and Build the ROS 2 Workspace on PC

Follow these steps in your Ubuntu / Pop!_OS terminal to clone and build the workspace:

### 1.1. Clone the repository
```bash
git clone https://github.com/d3im3r/ros2-for-control-dc-motor-system.git
cd ros2-for-control-dc-motor-system
```

### 1.2. Install system dependencies
```bash
sudo apt update
sudo apt install -y python3-matplotlib python3-pip python3-numpy python3-scipy python3-colcon-common-extensions ros-humble-micro-ros-agent
```

### 1.3. Build ROS 2 packages
```bash
cd ros2_ws
colcon build --symlink-install
```

### 1.4. Source the environment
```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

> 💡 **Tip:** To automatically source the workspace in every new terminal:
> ```bash
> echo "source /home/$USER/ros2-for-control-dc-motor-system/ros2_ws/install/setup.bash" >> ~/.bashrc
> ```

---

## 🔌 Step 2: Hardware and Firmware Setup on ESP32

The micro-ROS firmware runs on the ESP32 microcontroller and handles direct hardware interaction via hardware interrupts, timers, and LEDC modulation.

### 2.1. Hardware Connections and Pinout

| Component | Function | ESP32 Pin | Description |
| :--- | :--- | :---: | :--- |
| **Encoder Channel A** | Pulse input A | `GPIO 32` | Hardware interrupt (`CHANGE`) |
| **Encoder Channel B** | Pulse input B | `GPIO 33` | Direction sensing |
| **L298N H-Bridge** | PWM Channel B (`ENB`) | `GPIO 25` | LEDC modulation ($500\text{ Hz}$, $8\text{ bits}$, $0-255$) |
| **L298N H-Bridge** | Direction (`IN3`) | `GPIO 27` | Direction logic level |
| **L298N H-Bridge** | Direction (`IN4`) | `GPIO 26` | Direction logic level |
| **OLED SH1106 Display** | $I^2C$ SDA | `GPIO 21` | OLED data line ($128\times 64$) |
| **OLED SH1106 Display** | $I^2C$ SCL | `GPIO 22` | OLED clock line |

> ⚙️ **Experimental Encoder Calibration:** $N_{\mathrm{rev}} = 960\ \text{ticks/rev}$.

### 2.2. PlatformIO Workflow (VS Code Extension)

Firmware files are organized in the [`firmware/esp32_motor_step/`](firmware/esp32_motor_step) directory:

* [`firmware/esp32_motor_step/platformio.ini`](firmware/esp32_motor_step/platformio.ini): Environment configuration for ESP32, Arduino framework, micro-ROS, and OLED libraries.
* [`firmware/esp32_motor_step/src/main.cpp`](firmware/esp32_motor_step/src/main.cpp): Complete firmware with hardware encoder interrupts, LEDC H-Bridge PWM control, SH1106 OLED display, and micro-ROS publishers/subscribers.

#### Instructions to Build and Flash with VS Code:

1. **Install the Extension:**
   * In VS Code, go to the **Extensions** tab (`Ctrl+Shift+X`), search for **PlatformIO IDE**, and install it.

2. **Recommended Option — Open the firmware folder directly:**
   * In VS Code: *File* > *Open Folder...* and select `ros2-for-control-dc-motor-system/firmware/esp32_motor_step`.

3. **Alternative Option — Create a new project and replace files:**
   * Open **PlatformIO Home** (`Ant icon` > `PIOHome` > `Open`).
   * Click on **+ New Project**.
   * Name: `esp32_motor_step`.
   * Board: `Espressif ESP32 Dev Module` (or `esp32dev`).
   * Framework: `Arduino`.
   * Once created:
     * Copy and **replace** [`platformio.ini`](firmware/esp32_motor_step/platformio.ini) at the root of your PlatformIO project.
     * Copy and **replace** [`src/main.cpp`](firmware/esp32_motor_step/src/main.cpp) inside the `src/` folder.

4. **Build and Upload to ESP32:**
   * Connect your ESP32 board to the PC via USB.
   * On the bottom status bar (or PlatformIO side menu):
     * Click **Build** (`✔`) to compile (PlatformIO will automatically download and integrate micro-ROS and Adafruit libraries).
     * Click **Upload** (`→`) to flash the firmware to the ESP32.

### 2.3. PlatformIO Configuration (`platformio.ini`)

```ini
[env:esp32dev]
platform = espressif32@6.5.0
board = esp32dev
framework = arduino

monitor_speed = 115200

board_microros_distro = humble
board_microros_transport = serial

lib_deps =
    https://github.com/micro-ROS/micro_ros_platformio
    adafruit/Adafruit GFX Library
    adafruit/Adafruit SH110X

build_flags =
    -DCORE_DEBUG_LEVEL=0
```

---

## 🤖 Step 3: Serial Connection with micro-ROS Agent

Once the firmware is flashed and the ESP32 is connected via USB:

### 3.1. Set serial port permissions
```bash
sudo chmod 666 /dev/ttyUSB0
# or add your user to the dialout group:
sudo usermod -a -G dialout $USER
```
*(If your device shows up as `/dev/ttyACM0`, use that port instead).*

### 3.2. Launch the micro-ROS Agent over Serial (115200 baud)
```bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200
```

### 3.3. Verify Communication
In another terminal, check that the node and topics are active:
```bash
ros2 node list
# Expected output: /motor_step_node

ros2 topic list
# Expected output: /pwm_input, /vel_rad_s, /vel_rpm

ros2 topic hz /vel_rad_s
# Expected rate: stable ~10 Hz (Ts = 0.1 s)
```

---

## 🚀 Step 4: Experimental Execution by Stages

### 4.1. Stage 01: Motor Instrumentation and Bringup

Verify motor response and topic consistency:
```bash
ros2 launch dc_motor_bringup stage_01_instrumentation.launch.py
```

### 4.2. Stage 02: Automated Step Response Experiments (Identification)

Stage 02 launch starts concurrently: the temporal profile generator, the CSV data logger, and the interactive Matplotlib real-time monitor:

```bash
# Experiment 1: 30 % PWM Step
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=30.0

# Experiment 2: 45 % PWM Step
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=45.0

# Experiment 3: 60 % PWM Step
ros2 launch dc_motor_bringup stage_02_identification.launch.py step:=60.0
```

> **Configurable Launch Arguments:**
> - `step`: Step amplitude in percentage `[-100.0, 100.0]`. Default: `0.0`.
> - `total_time`: Total experiment duration in seconds. Default: `40.0`.

---

## ⏱️ Step Response Temporal Profile (Stage 02)

The standard test cycle is configured for a total acquisition of **40.0 seconds (400 samples at 10 Hz)**:

| Phase | Time Interval | PWM (\%) | Purpose |
| :--- | :---: | :---: | :--- |
| **1. Initial Rest** | `0.0 s` to `1.0 s` | `0.0 %` | Record initial condition and validate steady-state rest ($\omega_0$). |
| **2. Active Step** | `1.0 s` to `36.0 s` | `step %` | **35.0 s effective** to capture complete transient and steady-state ($\omega_{ss}$). |
| **3. Final Rest** | `36.0 s` to `40.0 s` | `0.0 %` | Deceleration and safe motor shutdown. |

```text
  PWM (%)
     ^
     |              +-----------------------------------+
step |              |                                   |
     |              |           Step (35.0 s)           |
     |              |                                   |
  0% +--------------+                                   +---------------> Time (s)
     0             1.0                                 36.0           40.0
        (Rest 1s)                                        (Rest end 4s)
```

---

## ⚙️ Software Architecture, Nodes, and Topics

```text
                   +---------------------+
                   |  step_profile_node  | (dc_motor_experiments)
                   +----------+----------+
                              | /pwm_input (Float32, %)
                              v
                   +---------------------+
                   |   motor_step_node   | (ESP32 / micro-ROS)
                   +----------+----------+
                              | /vel_rad_s (Float32, rad/s)
               +--------------+--------------+
               |                             |
               v                             v
    +--------------------+       +------------------------+
    |  step_response_db  |       |  step_response_graph   |
    |     (CSV Logger)   |       |  (Real-Time Plotter)   |
    +--------------------+       +------------------------+
```

### Topic Contract

* `/pwm_input` (`std_msgs/msg/Float32`): H-Bridge control command ($-100.0$ to $100.0\,\%$).
* `/vel_rad_s` (`std_msgs/msg/Float32`): Angular velocity estimated by encoder in $\text{rad/s}$ ($T_s = 0.1\text{ s}$).
* `/vel_rpm` (`std_msgs/msg/Float32`): Angular velocity in $\text{rpm}$ for local and remote visualization.

---

## 📊 Data Format (CSV) and Mathematical Modeling (FOP / FOPDT)

Each run of `data_logger` generates a timestamped file:

`motor_step_response_YYYYMMDD_HHMMSS.csv`

```csv
Time (s),Angular Velocity (rad/s),PWM (%)
0.100,0.000000,0.000
0.200,0.000000,0.000
...
1.100,2.152431,45.000
...
36.100,45.892100,0.000
```

### Mathematical Modeling

From experimental data, transfer functions are identified:

$$G_{\text{FOP}}(s) = \frac{K}{\tau s + 1} \qquad \text{or} \qquad G_{\text{FOPDT}}(s) = \frac{K e^{-\theta s}}{\tau s + 1}$$

where:

* **Static Gain:** $K = \frac{\omega_{ss} - \omega_0}{u_{ss} - u_0}\quad [\text{rad/s / } \\%\text{PWM}]$
* **Time Constant:** $\tau = t_{63.2\\%} - t_0$ (criterion of $63.2\\,\\%$ of total response).
* **Apparent Delay:** $\theta \approx t_{\text{start}} - t_0$.

### Offline Parametric Fitting Scripts

```bash
cd stage_02_system_identification/analysis

# First-Order Identification (FOP)
python3 identify_fop.py ../data/raw/pwm_45/motor_step_response.csv

# Identification with Delay (FOPDT)
python3 identify_fopdt.py ../data/raw/pwm_45/motor_step_response.csv

# Compare Operating Points (30%, 45%, 60%)
python3 compare_operating_points.py ../data/raw/pwm_30/*.csv ../data/raw/pwm_45/*.csv ../data/raw/pwm_60/*.csv
```

---

## 📁 Repository Structure

```text
ros2-for-control-dc-motor-system/
├── README.md                            # Main presentation and documentation
├── LICENSE                              # Apache-2.0 License
├── .gitignore                           # Git ignore rules
│
├── docs/                                # Academic documentation and guides
│   ├── guides/                          # Markdown guides (Guía 0, 1, 2)
│   ├── diagrams/                        # Architecture diagrams
│   └── images/                          # Visual resources
│
├── firmware/                            # micro-ROS firmware for ESP32 (PlatformIO)
│   └── esp32_motor_step/                # Acquisition and motor control project
│       ├── platformio.ini               # Platform, library, and micro-ROS config
│       └── src/
│           └── main.cpp                 # C++ firmware (encoder, PWM, OLED, micro-ROS)
│
├── ros2_ws/                             # ROS 2 Workspace (Executable Software)
│   └── src/
│       ├── dc_motor_bringup/            # Launch files and orchestration package
│       │   └── launch/
│       │       ├── motor_system.launch.py
│       │       ├── stage_01_instrumentation.launch.py
│       │       ├── stage_02_identification.launch.py
│       │       ├── stage_03_validation.launch.py
│       │       ├── stage_04_control.launch.py
│       │       └── stage_05_closed_loop.launch.py
│       │
│       ├── dc_motor_experiments/        # Acquisition and plotting package
│       │   └── dc_motor_experiments/
│       │       ├── step_response.py     # Step profile generator
│       │       ├── data_logger.py       # CSV data logger
│       │       └── velocity_monitor.py  # Real-time graphical monitor
│       │
│       └── dc_motor_control/            # Controllers package (PI, PID, etc.)
│           └── dc_motor_control/
│               ├── pi_controller.py
│               └── pid_controller.py
│
├── stage_00_system_design/              # System architecture and specifications
├── stage_01_motor_instrumentation/      # Encoder calibration (960 ticks/rev)
├── stage_02_system_identification/      # CSV data (raw/processed) and FOP/FOPDT analysis
│   ├── data/raw/                        # 30%, 45%, and 60% test runs
│   ├── analysis/                        # Mathematical identification scripts
│   └── models/                          # Identified K, tau, and theta parameters
├── stage_03_model_validation/           # Model validation metrics
├── stage_04_controller_design/          # Controller design and simulations
└── stage_05_closed_loop_control/        # Closed-loop experimental tests
```

---

## 🔧 Troubleshooting

| Issue | Probable Cause | Solution |
| :--- | :--- | :--- |
| `Package 'dc_motor_bringup' not found` | Workspace environment not sourced | Run `source ~/ros2-for-control-dc-motor-system/ros2_ws/install/setup.bash` in the terminal. |
| `No module named 'matplotlib'` | Missing Python libraries in Ubuntu | Run `sudo apt install -y python3-matplotlib python3-scipy python3-numpy`. |
| Error opening `/dev/ttyUSB0` | Insufficient serial port permissions | Run `sudo chmod 666 /dev/ttyUSB0` or add user to dialout: `sudo usermod -a -G dialout $USER`. |
| Real-time plot receives no data | micro-ROS Agent is not running | Start the agent: `ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200`. |
| Motor does not spin during launch | Default argument is `step:=0.0` | Specify step percentage in the command: `step:=45.0`. |

---

## 👥 Authors and License

* **Deimer Miranda Montoya, MSc.(c)** — `demiranda@unal.edu.co` / `deimer_miranda91162@elpoli.edu.co`
* **Institution:** [Politécnico Colombiano Jaime Isaza Cadavid](https://www.politecnicojic.edu.co/) — Faculty of Engineering
* **Course:** Intelligent Control (`ING01343-ING278`)
* **License:** [Apache License 2.0](LICENSE)
