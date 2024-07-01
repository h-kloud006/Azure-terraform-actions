resource "azurerm_virtual_network" "vnet" {
  name                = "backend-net"
  location            = "eastus"
  resource_group_name = "test-rg"
  address_space       = ["172.16.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "backend-containers"
  resource_group_name = azurerm_virtual_network.vnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["172.16.0.0/20"]
  service_endpoints    = ["Microsoft.Storage"]

  delegation {
    name = "delegation"

    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action", "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action"]
    }
  }
}

resource "azurerm_subnet" "subnet-services" {
  name                 = "backend-services"
  resource_group_name  = azurerm_virtual_network.vnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["172.16.64.0/24"]
  service_endpoints    = ["Microsoft.CognitiveServices"]
}

resource "azurerm_subnet" "appgw" {
  name                 = "appgw"
  resource_group_name  = azurerm_virtual_network.vnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["172.16.128.0/24"]
  service_endpoints    = ["Microsoft.Storage"]
}

resource "azurerm_private_dns_zone" "openai" {
  name                = "openai.azure.com"
  resource_group_name = azurerm_virtual_network.vnet.resource_group_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "openai" {
  name                  = "openai-link"
  resource_group_name   = azurerm_virtual_network.vnet.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.openai.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}

resource "azurerm_private_dns_zone" "hktype" {
  name                = "latest.hktype.com"
  resource_group_name = azurerm_virtual_network.vnet.resource_group_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "hktype" {
  name                  = "hktype-link"
  resource_group_name   = azurerm_virtual_network.vnet.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.hktype.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}
