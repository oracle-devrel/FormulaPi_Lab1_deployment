variable "password" {
  type = string
  sensitive = true
  default = ""
  validation {
    condition = length(var.password) >= 0
    error_message = "Password must be set with an appropriate length."
  }
}
variable "length" {
  default = 16
}
variable "special_chars_enabled" {
  default = true
  type = bool
}
variable "override_special" {
  default = "!#$%&*()-_=+[]{}<>:?"
  type = string
}
