
resource "azurerm_container_registry" "backend_registry" {
  name                = "hrbackend"
  resource_group_name = "test-rg"
  location            = "eastus"
  sku                 = "Standard"  
  admin_enabled       = true  
}
