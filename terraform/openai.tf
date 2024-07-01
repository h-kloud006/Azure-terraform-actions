
# resource "azurerm_cognitive_account" "openai" {
#   name                = "OpenAI"
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
#   kind                = "OpenAI"
#   custom_subdomain_name = "openai-dtcom"
#   outbound_network_access_restricted = true
#   public_network_access_enabled = false

#   sku_name = "S0"
# }

# resource "azurerm_cognitive_deployment" "embeddings" {
#   cognitive_account_id = azurerm_cognitive_account.openai.id
#   name    = "gpt4-turbo"

#   model {
#     format  = "OpenAI"
#     name    = "gpt-4"
#     version = "1106-Preview"
#   }
#   scale {
#     type     = "Standard"
#   }
# }

# resource "azurerm_cognitive_deployment" "chatcompletion" {
#   cognitive_account_id = azurerm_cognitive_account.openai.id
#   name    = "text-embedding-ada-002"

#   model {
#     format  = "OpenAI"
#     name    = "text-embedding-ada-002"
#     version = "2"
#   }
#   scale {
#     type     = "Standard"
#   }
# }