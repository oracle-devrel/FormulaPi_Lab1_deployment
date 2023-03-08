variable "db_id" {}
variable "wallet_password" {
  sensitive = true
}
variable "wallet_install_dir" {
  type = string
  default = ".local"
}
