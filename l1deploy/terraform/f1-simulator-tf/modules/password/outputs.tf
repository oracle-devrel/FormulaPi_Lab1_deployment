output "content" {
  value = length(var.password) > 0 ? var.password : random_password.passwd[0].result
  sensitive = true
}
