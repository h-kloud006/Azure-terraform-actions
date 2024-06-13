terraform {
  required_providers {
  azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.7.0"
    }
  }
  
}

terraform {
  backend "azurerm" {
  }
}

resource "azurerm_resource_group" "rg-aks" {
  name     = var.resource_group_name
  location = var.location
}

provider "azurerm" {  
  features {}
}

