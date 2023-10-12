output "content" {
  value = oci_database_autonomous_database_wallet.wallet.content
}

output "directory" {
  value = "${var.wallet_install_dir}/wallet"
}
