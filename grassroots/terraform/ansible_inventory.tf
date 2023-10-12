resource "local_file" "ansible_inventory" {
  content = templatefile("${path.module}/ansible_inventory.tftpl",
    {
      web_hostnames  = oci_core_instance.compute_web.*.hostname_label
      web_public_ips = oci_core_instance.compute_web.*.public_ip
    }
  )
  filename = "${path.module}/generated/app.ini"
}