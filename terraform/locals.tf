locals {
  openai_endpoint_fqdn = "${azurerm_private_endpoint.openai_private_endpoint.name}.${azurerm_resource_group.rg.location}.azurewebsites.net"
}