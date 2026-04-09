cmake_minimum_required(VERSION 3.8)
project(modbus_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencias
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generar interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ReadRegister.srv"
  "srv/WriteRegister.srv"
)

# Instalar módulos Python
ament_python_install_package(${PROJECT_NAME})

# Instalar ejecutables Python
install(PROGRAMS
  modbus_demo/modbus_provider.py
  modbus_demo/modbus_client.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
