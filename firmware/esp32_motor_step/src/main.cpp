#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <Arduino.h>
#include <Wire.h>
#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rclc/executor.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/float32.h>

#include <math.h>

#define ENCA 32
#define ENCB 33
const float COUNTS_PER_REV = 960.0f;

#define ENB 25
#define IN3 27
#define IN4 26

const int canal_pwm = 0;
const int frecuencia_pwm = 500;
const int resolucion_pwm = 8;

#define SDA_OLED 21
#define SCL_OLED 22
#define OLED_ADDRESS 0x3C
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
bool oled_ok = false;

volatile int32_t encoder_count = 0;
int32_t previous_count = 0;
unsigned long previous_time_ms = 0;

float pwm_ref = 0.0f;
float velocity_rad_s = 0.0f;
float velocity_rpm = 0.0f;

rcl_allocator_t allocator;
rclc_support_t support;
rcl_node_t node;
rcl_subscription_t sub_pwm_input;
rcl_publisher_t pub_vel_rad_s;
rcl_publisher_t pub_vel_rpm;
rcl_timer_t timer;
rclc_executor_t executor;

std_msgs__msg__Float32 pwm_input_msg;
std_msgs__msg__Float32 vel_rad_s_msg;
std_msgs__msg__Float32 vel_rpm_msg;

void IRAM_ATTR encoderISR() {
  bool A = digitalRead(ENCA);
  bool B = digitalRead(ENCB);

  if (A != B)
    encoder_count--;
  else
    encoder_count++;
}

void detenerMotor() {
  ledcWrite(canal_pwm, 0);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void aplicarPWM(float pwm_percent) {
  pwm_percent = constrain(pwm_percent, -100.0f, 100.0f);
  pwm_ref = pwm_percent;

  int pwm_value = (int)(fabsf(pwm_percent) * 255.0f / 100.0f);

  if (pwm_percent > 0.0f) {
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    ledcWrite(canal_pwm, pwm_value);
  } else if (pwm_percent < 0.0f) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    ledcWrite(canal_pwm, pwm_value);
  } else {
    detenerMotor();
  }
}

void actualizarOLED() {
  if (!oled_ok)
    return;

  display.clearDisplay();
  display.setTextColor(SH110X_WHITE);
  display.setTextSize(1);

  display.setCursor(0, 0);
  display.println("--- MOTOR STEP ---");

  display.setCursor(0, 18);
  display.print("PWM Ref: ");
  display.print(pwm_ref, 1);
  display.println(" %");

  display.setCursor(0, 34);
  display.print("RPM:     ");
  display.println(velocity_rpm, 1);

  display.setCursor(0, 50);
  display.print("Vel:     ");
  display.print(velocity_rad_s, 2);
  display.println(" rad/s");

  display.display();
}

void pwm_callback(const void *msgin) {
  const std_msgs__msg__Float32 *msg = (const std_msgs__msg__Float32 *)msgin;

  aplicarPWM(msg->data);
}

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)timer;
  (void)last_call_time;

  unsigned long current_time_ms = millis();
  float dt = (current_time_ms - previous_time_ms) * 0.001f;
  previous_time_ms = current_time_ms;

  if (dt <= 0.0f)
    return;

  noInterrupts();
  int32_t current_count = encoder_count;
  interrupts();

  int32_t delta_count = current_count - previous_count;
  previous_count = current_count;

  velocity_rad_s = (2.0f * PI * (float)delta_count) / (COUNTS_PER_REV * dt);

  velocity_rpm = (60.0f * (float)delta_count) / (COUNTS_PER_REV * dt);

  vel_rad_s_msg.data = velocity_rad_s;
  vel_rpm_msg.data = velocity_rpm;

  rcl_publish(&pub_vel_rad_s, &vel_rad_s_msg, NULL);
  rcl_publish(&pub_vel_rpm, &vel_rpm_msg, NULL);

  actualizarOLED();
}

void setup() {
  pinMode(ENCA, INPUT_PULLUP);
  pinMode(ENCB, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENCA), encoderISR, CHANGE);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  ledcSetup(canal_pwm, frecuencia_pwm, resolucion_pwm);
  ledcAttachPin(ENB, canal_pwm);
  detenerMotor();

  Wire.begin(SDA_OLED, SCL_OLED);
  oled_ok = display.begin(OLED_ADDRESS, true);

  if (oled_ok) {
    display.clearDisplay();
    display.setTextColor(SH110X_WHITE);
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("motor_step_node");
    display.println("960 ticks/rev");
    display.println("Inicializando...");
    display.display();
  }

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);

  rclc_node_init_default(&node, "motor_step_node", "", &support);

  rclc_subscription_init_default(
      &sub_pwm_input, &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32), "pwm_input");

  rclc_publisher_init_default(
      &pub_vel_rad_s, &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32), "vel_rad_s");

  rclc_publisher_init_default(
      &pub_vel_rpm, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
      "vel_rpm");

  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(100), timer_callback);

  rclc_executor_init(&executor, &support.context, 2, &allocator);

  rclc_executor_add_subscription(&executor, &sub_pwm_input, &pwm_input_msg,
                                 &pwm_callback, ON_NEW_DATA);

  rclc_executor_add_timer(&executor, &timer);

  noInterrupts();
  previous_count = encoder_count;
  interrupts();

  previous_time_ms = millis();
}

void loop() { rclc_executor_spin_some(&executor, RCL_MS_TO_NS(20)); }