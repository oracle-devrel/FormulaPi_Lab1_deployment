resource "random_password" "passwd" {
  length           = var.length
  special          = var.special_chars_enabled
  override_special = var.override_special
  min_numeric      = 1
  min_special = 1
  min_upper = 1
  min_lower = 1

  count = length(var.password) >= var.length == true ? 0 : 1
}
