# Stage 00: System Design

## 🎯 Guiding Question
> **How should the system be architected to actuate the motor and observe its dynamic behavior reliably?**

---

## 📌 Objectives
1. Define the distributed architecture between the microcontroller (ESP32) and the host control computer (ROS 2).
2. Establish the formal communication contract (topics, message types, ranges, and engineering units).
3. Allocate specific responsibilities to physical hardware modules and software components.

---

## 📐 Topic Contract and Interfaces

| Topic | Relative to ESP32 | ROS 2 Message | Units | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `/pwm_input` | Input | `std_msgs/msg/Float32` | % ($-100.0$ to $+100.0$) | Control action applied to H-Bridge driver |
| `/vel_rad_s` | Output | `std_msgs/msg/Float32` | rad/s | Estimated shaft angular velocity for control |
| `/vel_rpm` | Output | `std_msgs/msg/Float32` | rpm | Shaft angular velocity for monitoring |

---

## 🔌 Hardware Pinout Allocation

| ESP32 GPIO | Signal | Component | Description |
| :---: | :---: | :---: | :--- |
| **32** | ENCA | Encoder | Channel A hardware interrupt input (`CHANGE`) |
| **33** | ENCB | Encoder | Channel B direction sensing input |
| **25** | ENB | L298N H-Bridge | PWM input Channel B (LEDC, 500 Hz, 8 bits) |
| **27** | IN3 | L298N H-Bridge | Direction logic level |
| **26** | IN4 | L298N H-Bridge | Direction logic level |
| **21** | SDA | OLED Display | $I^2C$ Data line |
| **22** | SCL | OLED Display | $I^2C$ Clock line |
