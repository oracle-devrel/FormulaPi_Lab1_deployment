output "content" {
  value = length(var.password) > 0 ? var.password : random_password.passwd.result
  sensitive = true
}
