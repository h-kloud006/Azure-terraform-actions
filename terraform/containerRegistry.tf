
resource "azurerm_container_registry" "backend_registry" {
  name                = "backend"
  resource_group_name = "test-rg"
  location            = "eastus"
  sku                 = "Standard"  
  admin_enabled       = true  
}
